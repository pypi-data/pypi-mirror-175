

_HAS_XROOTD = False
try:
    from XRootD import client as xrd_client
    _HAS_XROOTD = True
except Exception:
    print("XRootD module could not be load", file = sys.stderr, flush = True)


def _is_valid_xrootd() -> bool:
    if not _HAS_XROOTD: return False
    xrd_ver_arr = xrd_client.__version__.split(".")
    if len(xrd_ver_arr) > 1:  # noqa: PLR1705
        _XRDVER_1 = xrd_ver_arr[0][1:] if xrd_ver_arr[0].startswith('v') else xrd_ver_arr[0]  # take out the v if present
        _XRDVER_2 = xrd_ver_arr[1]
        return int(_XRDVER_1) >= 5 and int(_XRDVER_2) > 2

    # version is not of x.y.z form, this is git based form
    xrdver_git = xrd_ver_arr[0].split("-")
    _XRDVER_1 = xrdver_git[0][1:] if xrdver_git[0].startswith('v') else xrdver_git[0]  # take out the v if present
    _XRDVER_2 = xrdver_git[1]
    return int(_XRDVER_1) > 20211113


# use only 5.3 versions and up - reference point
_HAS_XROOTD = _is_valid_xrootd()
_HAS_XROOTD_GETDEFAULT = False
if _HAS_XROOTD:
    def XRD_EnvPut(key, value):  # noqa: ANN001,ANN201
        """Sets the given key in the xrootd client environment to the given value.
        Returns false if there is already a shell-imported setting for this key, true otherwise
        """
        return xrd_client.EnvPutInt(key, value) if str(value).isdigit() else xrd_client.EnvPutString(key, value)

    def XRD_EnvGet(key):  # noqa: ANN001,ANN201
        """Get the value of the key from xrootd"""
        val = xrd_client.EnvGetString(key)
        if not val:
            val = xrd_client.EnvGetInt(key)
        return val  # noqa: R504

    # Override the application name reported to the xrootd server.
    XRD_EnvPut('XRD_APPNAME', f'alien.py/{ALIENPY_VERSION_STR} xrootd/{xrd_client.__version__}')
    _HAS_XROOTD_GETDEFAULT = hasattr(xrd_client, 'EnvGetDefault')


def xrd_config_init():
    """Initialize generic XRootD client vars/timeouts"""
    if not _HAS_XROOTD: return
    # xrdcp parameters (used by ALICE tests)
    # http://xrootd.org/doc/man/xrdcp.1.html
    # https://xrootd.slac.stanford.edu/doc/xrdcl-docs/www/xrdcldocs.html#x1-100004.2
    # xrootd defaults https://github.com/xrootd/xrootd/blob/master/src/XrdCl/XrdClConstants.hh

    # Resolution for the timeout events. Ie. timeout events will be processed only every XRD_TIMEOUTRESOLUTION seconds.
    if not os.getenv('XRD_TIMEOUTRESOLUTION'): XRD_EnvPut('TimeoutResolution', int(1))  # let's check the status every 1s; default 15

    # Number of connection attempts that should be made (number of available connection windows) before declaring a permanent failure.
    if not os.getenv('XRD_CONNECTIONRETRY'): XRD_EnvPut('ConnectionRetry', int(5))  # default 5

    # A time window for the connection establishment. A connection failure is declared if the connection is not established within the time window.
    # N.B.!!. If a connection failure happens earlier then another connection attempt will only be made at the beginning of the next window
    if not os.getenv('XRD_CONNECTIONWINDOW'): XRD_EnvPut('ConnectionWindow', int(10))  # default 120

    # Default value for the time after which an error is declared if it was impossible to get a response to a request.
    # N.B.!!. This is the total time for the initialization dialogue!! see https://xrootd.slac.stanford.edu/doc/xrdcl-docs/www/xrdcldocs.html#x1-580004.3.6
    if not os.getenv('XRD_REQUESTTIMEOUT'): XRD_EnvPut('RequestTimeout', int(1200))  # default 1800

    # Default value for the time after which a connection error is declared (and a recovery attempted) if there are unfulfilled requests and there is no socket activity or a registered wait timeout.
    # N.B.!!. we actually want this timeout for failure on onverloaded/unresponsive server. see https://github.com/xrootd/xrootd/issues/1597#issuecomment-1064081574
    if not os.getenv('XRD_STREAMTIMEOUT'): XRD_EnvPut('StreamTimeout', int(20))  # default 60

    # Maximum time allowed for the copy process to initialize, ie. open the source and destination files.
    if not os.getenv('XRD_CPINITTIMEOUT'): XRD_EnvPut('CPInitTimeout', int(300))  # default 600

    # Time period after which an idle connection to a data server should be closed.
    if not os.getenv('XRD_DATASERVERTTL'): XRD_EnvPut('DataServerTTL', int(20))  # we have no reasons to keep idle connections

    # Time period after which an idle connection to a manager or a load balancer should be closed.
    if not os.getenv('XRD_LOADBALANCERTTL'): XRD_EnvPut('LoadBalancerTTL', int(30))  # we have no reasons to keep idle connections

    # If set the client tries first IPv4 address (turned off by default).
    if not os.getenv('XRD_PREFERIPV4'): XRD_EnvPut('PreferIPv4', int(1))



def xrdcp_help() -> str:
    return f'''Command format is of the form of (with the strict order of arguments):
        cp <options> src dst
        or
        cp <options> -input input_file
where src|dst are local files if prefixed with file:// or file: or grid files otherwise
and -input argument is a file with >src dst< pairs
after each src,dst can be added comma separated specifiers in the form of: @disk:N,SE1,SE2,!SE3
where disk selects the number of replicas and the following specifiers add (or remove) storage endpoints from the received list
options are the following :
-h : print help
-d | -dd | -ddd : enable XRootD log level to Info/Debug/Dump
-xrdlog : change the default filepath of XRootD logfile (default: xrdlog)
-f : replace destination file (if destination is local it will be replaced only if integrity check fails)
-cksum : check hash sum of the file; for downloads the central catalogue md5 will be verified
-S <aditional streams> : uses num additional parallel streams to do the transfer. (max = 15)
-chunks <nr chunks> : number of chunks that should be requested in parallel
-chunksz <bytes> : chunk size (bytes)
-T <nr_copy_jobs> : number of parralel copy jobs from a set (for recursive copy); defaults to 8 for downloads
-timeout <seconds> : the job will fail if did not finish in this nr of seconds
-retry <times> : retry N times the copy process if failed
-ratethreshold <bytes/s> : fail the job if the speed is lower than specified bytes/s
-noxrdzip: circumvent the XRootD mechanism of zip member copy and download the archive and locally extract the intended member.
N.B.!!! for recursive copy (all files) the same archive will be downloaded for each member.
If there are problems with native XRootD zip mechanism, download only the zip archive and locally extract the contents

For the recursive copy of directories the following options (of the find command) can be used:
-glob <globbing pattern> : this is the usual AliEn globbing format; {PrintColor(COLORS.BIGreen)}N.B. this is NOT a REGEX!!!{PrintColor(COLORS.ColorReset)} defaults to all "*"
-select <pattern> : select only these files to be copied; {PrintColor(COLORS.BIGreen)}N.B. this is a REGEX applied to full path!!!{PrintColor(COLORS.ColorReset)}
-name <pattern> : select only these files to be copied; {PrintColor(COLORS.BIGreen)}N.B. this is a REGEX applied to a directory or file name!!!{PrintColor(COLORS.ColorReset)}
-name <verb>_string : where verb = begin|contain|ends|ext and string is the text selection criteria.
verbs are aditive : -name begin_myf_contain_run1_ends_bla_ext_root
{PrintColor(COLORS.BIRed)}N.B. the text to be filtered cannont have underline <_> within!!!{PrintColor(COLORS.ColorReset)}
-parent <parent depth> : in destination use this <parent depth> to add to destination ; defaults to 0
-a : copy also the hidden files .* (for recursive copy)
-j <queue_id> : select only the files created by the job with <queue_id>  (for recursive copy)
-l <count> : copy only <count> nr of files (for recursive copy)
-o <offset> : skip first <offset> files found in the src directory (for recursive copy)

Further filtering of the files can be applied with the following options:
-mindepth/-maxdepth N : restrict results to N directories depth relative to the base/searched for directory.
                        N.B. for in directory globbing (/path1/path2/*.sh : the base directory is /path1/path2)
-minsize/-maxsize N : restrict results to at least/at most N bytes in size
-min-ctime/-max-ctime UNIX_TIME: restrict results to at least/at most this UNIX_TIME (ms, 13 decimals integer)
-user/-group string_name : restrict results to specified user/group
'''


def _xrdcp_sysproc(cmdline: str, timeout: Union[str, int, None] = None) -> RET:
    """xrdcp stanalone system command"""
    if not cmdline: return RET(1, '', '_xrdcp_sysproc :: no cmdline')
    if timeout is not None: timeout = int(timeout)
    # --nopbar --posc
    xrdcp_cmdline = f'xrdcp -N -P {cmdline}'
    return runShellCMD(xrdcp_cmdline, captureout = True, do_shell = False, timeout = timeout)


def _xrdcp_copyjob(copy_job: CopyFile, xrd_cp_args: XrdCpArgs) -> int:  # , printout: str = ''
    """xrdcp based task that process a copyfile and it's arguments"""
    if not copy_job: return int(2)
    # overwrite = xrd_cp_args.overwrite
    # batch = xrd_cp_args.batch
    # tpc = xrd_cp_args.tpc
    # hashtype = xrd_cp_args.hashtype
    # cksum = xrd_cp_args.cksum
    timeout = xrd_cp_args.timeout
    # rate = xrd_cp_args.rate
    cmdline = f'{copy_job.src} {copy_job.dst}'
    return retf_print(_xrdcp_sysproc(cmdline, timeout))


def XrdCopy_xrdcp(job_list: list, xrd_cp_args: XrdCpArgs) -> list:  # , printout: str = ''
    """XRootD copy command :: the actual XRootD copy process"""
    if not _HAS_XROOTD:
        print_err("XRootD not found or lower version thant 5.3.3")
        return []
    if not xrd_cp_args:
        print_err("cp arguments are not set, XrdCpArgs tuple missing")
        return []
    # overwrite = xrd_cp_args.overwrite
    # batch = xrd_cp_args.batch
    # makedir = xrd_cp_args.makedir

    # ctx = mp.get_context('forkserver')
    # q = ctx.JoinableQueue()
    # p = ctx.Process(target=_xrdcp_copyjob, args=(q,))
    # p.start()
    # print(q.get())
    # p.join()
    for copy_job in job_list:
        if _DEBUG: logging.debug('\nadd copy job with\nsrc: %s\ndst: %s\n', copy_job.src, copy_job.dst)
        # xrdcp_cmd = f' {copy_job.src} {copy_job.dst}'
        if _DEBUG: print_out(copy_job)
    return []


def lfnAccessUrl(wb, lfn: str, local_file: str = '', specs: Union[None, list, str] = None, isWrite: bool = False, strictspec: bool = False, httpurl: bool = False) -> dict:
    """Query central services for the access envelope of a lfn, it will return a lfn:server answer with envelope pairs"""
    if not wb: return {}
    if not lfn: return {}
    if not specs: specs = []
    if specs and isinstance(specs, str): specs = specs_split.split(specs)
    if isWrite:
        if not local_file or not os.path.exists(local_file):
            print_err(f'lfnAccessUrl/write token:: invalid local file: {local_file}')
            return {}
        access_type = 'write'
        size = int(os.stat(local_file).st_size)
        md5sum = md5(local_file)
        files_with_default_replicas = ['.sh', '.C', '.jdl', '.xml']
        if any(lfn.endswith(ext) for ext in files_with_default_replicas) and size < 1048576 and not specs:  # we have a special lfn
            specs.append('disk:4')  # and no specs defined then default to disk:4
        get_envelope_arg_list = ['-s', size, '-m', md5sum, access_type, lfn]
        if not specs: specs.append('disk:2')  # hard default if nothing is specified
    else:
        access_type = 'read'
        get_envelope_arg_list = [access_type, lfn]

    if specs: get_envelope_arg_list.append(",".join(specs))
    if httpurl: get_envelope_arg_list.insert(0, '-u')
    if strictspec: get_envelope_arg_list.insert(0, '-f')
    ret_obj = SendMsg(wb, 'access', get_envelope_arg_list, opts = 'nomsg')
    if ret_obj.exitcode != 0 or 'results' not in ret_obj.ansdict:
        ret_obj = ret_obj._replace(err = f'No token for {lfn} :: errno {ret_obj.exitcode} -> {ret_obj.err}')
        retf_print(ret_obj, opts = 'err noprint')
        return {}
    return ret_obj.ansdict


def lfn2uri(wb, lfn: str, local_file: str = '', specs: Union[None, list, str] = None, isWrite: bool = False, strictspec: bool = False, httpurl: bool = False) -> str:
    """Return the list of access URIs for all replica of an ALICE lfn - can be used directly with xrdcp"""
    result = lfnAccessUrl(wb, lfn, local_file, specs, isWrite, strictspec, httpurl)
    if not result: return ''
    output_list = []
    for replica in result['results']:
        output_list.append(repr(f"{replica['url']}?xrd.wantprot=unix&authz={replica['envelope']}"))
    return '\n'.join(output_list)


def lfn2meta(wb, lfn: str, local_file: str = '', specs: Union[None, list, str] = None, isWrite: bool = False, strictspec: bool = False, httpurl: bool = False) -> str:
    """Create metafile for download of an ALICE lfn and return it's location - can be used directly with xrdcp"""
    if isWrite:
        print_err('Metafile creation possible only for download')
        return ''
    result = lfnAccessUrl(wb, lfn, local_file, specs, isWrite, strictspec, httpurl)
    if not result: return ''
    size_4meta = result['results'][0]['size']  # size SHOULD be the same for all replicas
    md5_4meta = result['results'][0]['md5']  # the md5 hash SHOULD be the same for all replicas
    file_in_zip = None
    url_list_4meta = []
    for replica in result['results']:
        url_components = replica['url'].rsplit('#', maxsplit = 1)
        if len(url_components) > 1: file_in_zip = url_components[1]
        # if is_pfn_readable(url_components[0]):  # it is a lot cheaper to check readability of replica than to try and fail a non-working replica
        url_list_4meta.append(f'{url_components[0]}?xrd.wantprot=unix&authz={replica["envelope"]}')

    # Create the metafile as a temporary uuid5 named file (the lfn can be retrieved from meta if needed)
    metafile = create_metafile(make_tmp_fn(lfn, '.meta4', uuid5 = True), lfn, local_file, size_4meta, md5_4meta, url_list_4meta)
    if not metafile:
        print_err(f"Could not create the download metafile for {lfn}")
        return ''
    subprocess.run(shlex.split(f'mv {metafile} {os.getcwd()}/'), check = False)  # keep it in local directory
    metafile = os.path.realpath(os.path.basename(metafile))
    return f'{metafile}?xrdcl.unzip={file_in_zip}' if (file_in_zip and 'ALIENPY_NOXRDZIP' not in os.environ) else f'{metafile}'


def lfn2fileTokens(wb, arg_lfn2file: lfn2file, specs: Union[None, list, str] = None, isWrite: bool = False, strictspec: bool = False, httpurl: bool = False) -> dict:
    """Query central services for the access envelope of a lfn, it will return a lfn:server answer with envelope pairs"""
    if not wb: return {}
    if not arg_lfn2file: return {}
    lfn = arg_lfn2file.lfn
    file = arg_lfn2file.file
    if not specs: specs = []
    if specs and isinstance(specs, str): specs = specs_split.split(specs)
    result = lfnAccessUrl(wb, lfn, file, specs, isWrite, strictspec, httpurl)
    if not result:
        return {"lfn": lfn, "answer": {}}
    qos_tags = [el for el in specs if 'ALICE::' not in el]  # for element in specs, if not ALICE:: then is qos tag
    SEs_list_specs = [el for el in specs if 'ALICE::' in el]  # explicit requests of SEs
    SEs_list_total = [replica["se"] for replica in result["results"]]
    # let's save for each replica the orginal request info
    for replica in result["results"]:
        replica["qos_specs"] = qos_tags  # qos tags from specs
        replica["SElist_specs"] = SEs_list_specs  # SE from specs
        replica["SElist"] = SEs_list_total  # list of SEs that were used
        replica["file"] = file
        replica["lfn"] = lfn
    return {"lfn": lfn, "answer": result}


def lfn2fileTokens_list(wb, input_lfn_list: list, specs: Union[None, list, str] = None, isWrite: bool = False, strictspec: bool = False, httpurl: bool = False) -> list:
    """Query central services for the access envelope of the list of lfns, it will return a list of lfn:server answer with envelope pairs"""
    if not wb: return []
    access_list = []
    if not input_lfn_list: return access_list
    if specs is None: specs = []
    for l2f in input_lfn_list: access_list.append(lfn2fileTokens(wb, l2f, specs, isWrite, strictspec, httpurl))
    return access_list



def path_grid_stat(wb, path: str) -> STAT_FILEPATH:
    """Get full information on a GRID path/lfn"""
    norm_path = expand_path_grid(path)
    ret_obj = SendMsg(wb, 'stat', [norm_path], opts = 'nomsg log')
    if ret_obj.exitcode != 0: return STAT_FILEPATH(norm_path)
    file_stat = ret_obj.ansdict["results"][0]  # stat can query and return multiple results, but we are using only one
    mtime = file_stat.get('mtime', '')
    guid = file_stat.get('guid', '')
    size = file_stat.get('size', '')
    md5hash = file_stat.get('md5', '')
    return STAT_FILEPATH(file_stat['lfn'], file_stat['type'], file_stat['perm'], file_stat['owner'], file_stat['gowner'], file_stat['ctime'],
                         mtime, guid, size, md5hash)


def path_grid_writable(file_stat: STAT_FILEPATH) -> bool:
    p_user = int(file_stat['perm'][0])
    p_group = int(file_stat['perm'][1])
    p_others = int(file_stat['perm'][2])
    writable_user = writable_group = writable_others = False
    write_perm = {2, 6, 7}
    if AlienSessionInfo['user'] == file_stat['uid'] and p_user in write_perm: writable_user = True
    if AlienSessionInfo['user'] == file_stat['gid'] and p_group in write_perm: writable_group = True
    if p_others in write_perm: writable_others = True
    return writable_user or writable_group or writable_others


def expand_path_grid(path_arg: str) -> str:
    """Given a string representing a GRID file (lfn), return a full path after interpretation of AliEn HOME location, current directory, . and .. and making sure there are only single /"""
    global AlienSessionInfo
    is_dir = path_arg.endswith('/')
    exp_path = lfn_prefix_re.sub('', path_arg)  # lets remove any prefixes
    exp_path = re.sub(r"^\/*\%ALIEN[\/\s]*", AlienSessionInfo['alienHome'], exp_path)  # replace %ALIEN token with user grid home directory
    if exp_path == '.': exp_path = AlienSessionInfo['currentdir']
    if exp_path == '~': exp_path = AlienSessionInfo['alienHome']
    if exp_path.startswith('./'): exp_path = exp_path.replace('.', AlienSessionInfo['currentdir'], 1)
    if exp_path.startswith('~/'): exp_path = exp_path.replace('~', AlienSessionInfo['alienHome'], 1)  # replace ~ for the usual meaning
    if not exp_path.startswith('/'): exp_path = f'{AlienSessionInfo["currentdir"]}/{exp_path}'  # if not full path add current directory to the referenced path
    exp_path = os.path.normpath(exp_path)
    if is_dir: exp_path = f'{exp_path}/'
    return exp_path  # noqa: R504


def pathtype_grid(wb, path: str) -> str:
    """Query if a lfn is a file or directory, return f, d or empty"""
    if not wb: return ''
    if not path: return ''
    ret_obj = SendMsg(wb, 'type', [path], opts = 'nomsg log')
    if ret_obj.exitcode != 0: return ''
    return str(ret_obj.ansdict['results'][0]["type"])[0]



def create_metafile(meta_filename: str, lfn: str, local_filename: str, size: Union[str, int], md5in: str, replica_list: Union[None, list] = None) -> str:
    """Generate a meta4 xrootd virtual redirector with the specified location and using the rest of arguments"""
    if not (meta_filename and replica_list): return ''
    try:
        with open(meta_filename, 'w', encoding="ascii", errors="replace") as f:
            published = str(datetime.datetime.now().replace(microsecond=0).isoformat())
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(' <metalink xmlns="urn:ietf:params:xml:ns:metalink">\n')
            f.write(f'   <published>{published}</published>\n')
            f.write(f'   <file name="{local_filename}">\n')
            f.write(f'     <lfn>{lfn}</lfn>\n')
            f.write(f'     <size>{size}</size>\n')
            if md5in: f.write(f'     <hash type="md5">{md5in}</hash>\n')
            for url in replica_list:
                f.write(f'     <url><![CDATA[{url}]]></url>\n')
            f.write('   </file>\n')
            f.write(' </metalink>\n')
        return meta_filename
    except Exception:
        logging.error(traceback.format_exc())
        return ''


def format_dst_fn(src_dir, src_file, dst, parent):
    """Return the destination filename given the source dir/name, destination directory and number of parents to keep"""
    # let's get destination file name (relative path with parent value)
    if src_dir != src_file:  # recursive operation
        total_relative_path = src_file.replace(src_dir, '', 1)
        src_dir_path = Path(src_dir)
        src_dir_parts = src_dir_path.parts
        if not src_dir.endswith('/'): src_dir_parts = src_dir_parts[:-1]
        src_dir = '/'.join(map(lambda x: str(x or ''), src_dir_parts))
        src_dir = src_dir.replace('//', '/')
        components_list = src_dir.split('/')
        components_list[0] = '/'  # first slash is lost in split
        file_components = len(components_list)  # it's directory'
        parent = min(parent, file_components)  # make sure maximum parent var point to first dir in path
        parent_selection = components_list[(file_components - parent):]
        rootdir_src_dir = '/'.join(parent_selection)
        file_relative_name = f'{rootdir_src_dir}/{total_relative_path}'
    else:
        src_file_path = Path(src_file)
        file_components = len(src_file_path.parts) - 1 - 1  # without the file and up to slash
        parent = min(parent, file_components)  # make sure maximum parent var point to first dir in path
        rootdir_src_file = src_file_path.parents[parent].as_posix()
        file_relative_name = src_file.replace(rootdir_src_file, '', 1)

    dst_file = f'{dst}/{file_relative_name}' if dst.endswith('/') else dst
    return os.path.normpath(dst_file)


def setDst(file: str = '', parent: int = 0) -> str:
    """For a given file path return the file path keeping the <parent> number of components"""
    p = Path(file)
    path_components = len(p.parts)
    if parent >= (path_components - 1): parent = path_components - 1 - 1  # IF parent >= number of components without filename THEN make parent = number of component without / and filename
    basedir = p.parents[parent].as_posix()
    if basedir == '/': return file
    return p.as_posix().replace(basedir, '', 1)


def name2regex(pattern_regex: str = '') -> str:
    if not pattern_regex: return ''
    translated_pattern_regex = ''
    re_all = '.*'
    re_all_end = '[^/]*'
    verbs = ('begin', 'contain', 'ends', 'ext')
    pattern_list = pattern_regex.split('_')
    if any(verb in pattern_regex for verb in verbs):
        if pattern_list.count('begin') > 1 or pattern_list.count('end') > 1 or pattern_list.count('ext') > 1:
            print_out('<begin>, <end>, <ext> verbs cannot appear more than once in the name selection')
            return ''

        list_begin = []
        list_contain = []
        list_ends = []
        list_ext = []
        for idx, tokenstr in enumerate(pattern_list):
            if tokenstr == 'begin': list_begin.append(KV(tokenstr, pattern_list[idx + 1]))
            if tokenstr == 'contain': list_contain.append(KV(tokenstr, pattern_list[idx + 1]))
            if tokenstr == 'ends': list_ends.append(KV(tokenstr, pattern_list[idx + 1]))
            if tokenstr == 'ext': list_ext.append(KV(tokenstr, pattern_list[idx + 1]))

        if list_begin:
            translated_pattern_regex = re_all + '/' + f'{list_begin[0].val}{re_all_end}'  # first string after the last slash (last match exclude /)
        for patt in list_contain:
            if not list_begin: translated_pattern_regex = f'{re_all}'
            translated_pattern_regex = f'{translated_pattern_regex}{patt.val}{re_all_end}'
        if list_ends:
            translated_pattern_regex = f'{translated_pattern_regex}{list_ends[0].val}{re_all_end}'
        if list_ext:
            translated_pattern_regex = translated_pattern_regex + "\\." + list_ext[0].val
        if translated_pattern_regex:
            if list_ext:
                translated_pattern_regex = f'{translated_pattern_regex}' + '$'
            else:
                translated_pattern_regex = f'{translated_pattern_regex}{re_all_end}' + '$'
    return translated_pattern_regex  # noqa: R504


def extract_glob_pattern(path_arg: str) -> tuple:
    """Extract glob pattern from a path"""
    if not path_arg: return None, None
    base_path = pattern = None
    if '*' in path_arg:  # we have globbing in src path
        path_components = path_arg.split("/")
        base_path_arr = []  # let's establish the base path
        for el in path_components:
            if '*' not in el: base_path_arr.append(el)
            else: break

        for el in base_path_arr: path_components.remove(el)  # remove the base path components (those without *) from full path components
        base_path = f'{"/".join(base_path_arr)}{"/" if base_path_arr else ""}'  # rewrite the source path without the globbing part
        pattern = '/'.join(path_components)  # the globbing part is the rest of element that contain *
    else:
        base_path = path_arg
    return (base_path, pattern)


def path_type(path_arg: str) -> tuple:
    """Check if path is local or grid; default is grid and local must have file: prefix"""
    location = 'local' if path_arg.startswith('file:') else 'grid'
    return (path_arg, location)


def commit(wb, tokenstr: str, size: int, lfn: str, perm: str, expire: str, pfn: str, se: str, guid: str, md5sum: str) -> RET:
    """Upon succesful xrootd upload to server, commit the guid name into central catalogue"""
    if not wb: return RET()
    return SendMsg(wb, 'commit', [tokenstr, int(size), lfn, perm, expire, pfn, se, guid, md5sum], opts = 'log')


def commitFile(wb, lfnInfo: CommitInfo) -> RET:
    """Upon succesful xrootd upload to server, commit the guid name into central catalogue"""
    if not wb or not lfnInfo: return RET()
    return SendMsg(wb, 'commit', [lfnInfo.envelope, int(lfnInfo.size), lfnInfo.lfn, lfnInfo.perm, lfnInfo.expire, lfnInfo.pfn, lfnInfo.se, lfnInfo.guid, lfnInfo.md5], opts = 'log')


def commitFileList(wb, lfnInfo_list: list) -> list:  # returns list of RET
    """Upon succesful xrootd upload to server, commit the guid name into central catalogue for a list of pfns"""
    if not wb or not lfnInfo_list: return []
    batch_size = 30
    batches_list = [lfnInfo_list[x: x + batch_size] for x in range(0, len(lfnInfo_list), batch_size)]
    commit_results = []
    for batch in batches_list:
        commit_list = []
        for file_commit in batch:
            jsoncmd = CreateJsonCommand('commit', [file_commit.envelope, int(file_commit.size), file_commit.lfn,
                                                   file_commit.perm, file_commit.expire, file_commit.pfn, file_commit.se,
                                                   file_commit.guid, file_commit.md5],
                                        'nokeys')
            commit_list.append(jsoncmd)
        commit_results.extend(SendMsgMulti(wb, commit_list, 'log'))
    return commit_results


def list_files_grid(wb, search_dir: str, pattern: Union[None, REGEX_PATTERN_TYPE, str] = None, is_regex: bool = False, find_args: Union[str, list, None] = None) -> RET:
    """Return a list of files(lfn/grid files) that match pattern found in dir
    Returns a RET object (from find), and takes: wb, directory, pattern, is_regex, find_args
    """
    if not search_dir: return RET(-1, "", "No search directory specified")

    if find_args is None: find_args = []
    find_args_list = find_args.split() if isinstance(find_args, str) else find_args.copy()

    # lets process the pattern: extract it from src if is in the path globbing form
    is_single_file = False  # dir actually point to a file

    dir_arg_list = search_dir.split()
    if len(dir_arg_list) > 1:  # dir is actually a list of arguments
        if not pattern: pattern = dir_arg_list.pop(-1)
        search_dir = dir_arg_list.pop(-1)
        if dir_arg_list: find_args = ' '.join(dir_arg_list)

    if '*' in search_dir:  # we have globbing in src path
        is_regex = False
        src_arr = search_dir.split("/")
        base_path_arr = []  # let's establish the base path
        for el in src_arr:
            if '*' not in el:
                base_path_arr.append(el)
            else:
                break
        for el in base_path_arr: src_arr.remove(el)  # remove the base path
        search_dir = '/'.join(base_path_arr) + '/'  # rewrite the source path without the globbing part
        pattern = '/'.join(src_arr)  # the globbing part is the rest of element that contain *
    else:  # pattern is specified by argument
        if pattern is None:
            if not search_dir.endswith('/'):  # this is a single file
                is_single_file = True
            else:
                pattern = '*'  # prefer globbing as default
        elif type(pattern) is REGEX_PATTERN_TYPE:  # unlikely but supported to match signatures # noqa: PIE789,PLC0123
            pattern = pattern.pattern  # We pass the regex pattern into command as string
            is_regex = True

        # it was explictly requested that pattern is regex
        if is_regex and isinstance(pattern, str) and valid_regex(pattern) is None:
            msg = f'list_files_grid:: {pattern} failed to re.compile'
            logging.error(msg)
            return RET(-1, '', msg)

    # remove default from additional args
    filter_args_list = []
    get_arg(find_args_list, '-a')
    get_arg(find_args_list, '-s')
    get_arg(find_args_list, '-f')
    get_arg(find_args_list, '-d')
    get_arg(find_args_list, '-w')
    get_arg(find_args_list, '-wh')

    exclude_string = get_arg_value(find_args_list, '-exclude')
    if exclude_string:
        filter_args_list.extend(['-exclude', exclude_string])

    exclude_regex = get_arg_value(find_args_list, '-exclude_re')
    if exclude_regex:
        filter_args_list.extend(['-exclude_re', exclude_regex])

    min_depth = get_arg_value(find_args_list, '-mindepth')
    if min_depth:
        if not min_depth.isdigit() or min_depth.startswith("-"):
            print_err(f'list_files_grid::mindepth arg not recognized: {" ".join(find_args_list)}')
        else:
            filter_args_list.extend(['-mindepth', min_depth])

    max_depth = get_arg_value(find_args_list, '-maxdepth')
    if max_depth:
        if not max_depth.isdigit() or max_depth.startswith("-"):
            print_err(f'list_files_grid::maxdepth arg not recognized: {" ".join(find_args_list)}')
        else:
            filter_args_list.extend(['-maxdepth', max_depth])

    min_size = get_arg_value(find_args_list, '-minsize')
    if min_size:
        if not min_size.isdigit() or min_size.startswith("-"):
            print_err(f'list_files_grid::minsize arg not recognized: {" ".join(find_args_list)}')
        else:
            filter_args_list.extend(['-minsize', min_size])

    max_size = get_arg_value(find_args_list, '-maxsize')
    if max_size:
        if not max_size.isdigit() or max_size.startswith("-"):
            print_err(f'list_files_grid::maxsize arg not recognized: {" ".join(find_args_list)}')
        else:
            filter_args_list.extend(['-maxsize', max_size])

    min_ctime = get_arg_value(find_args_list, '-min-ctime')
    if min_ctime:
        if min_ctime.startswith("-"):
            print_err(f'list_files_grid::min-ctime arg not recognized: {" ".join(find_args_list)}')
        else:
            filter_args_list.extend(['-min-ctime', min_ctime])

    max_ctime = get_arg_value(find_args_list, '-max-ctime')
    if max_ctime:
        if max_ctime.startswith("-"):
            print_err(f'list_files_grid::max-ctime arg not recognized: {" ".join(find_args_list)}')
        else:
            filter_args_list.extend(['-max-ctime', max_ctime])

    jobid = get_arg_value(find_args_list, '-jobid')
    if jobid:
        if not jobid.isdigit() or jobid.startswith("-"):
            print_err(f'list_files_grid::jobid arg not recognized: {" ".join(find_args_list)}')
        else:
            filter_args_list.extend(['-jobid', jobid])

    user = get_arg_value(find_args_list, '-user')
    if user:
        if not user.isalpha() or user.startswith("-"):
            print_err(f'list_files_grid::user arg not recognized: {" ".join(find_args_list)}')
        else:
            filter_args_list.extend(['-user', user])

    group = get_arg_value(find_args_list, '-group')
    if group:
        if not group.isalpha() or group.startswith("-"):
            print_err(f'list_files_grid::group arg not recognized: {" ".join(find_args_list)}')
        else:
            filter_args_list.extend(['-group', group])

    # create and return the list object just for a single file
    if is_single_file:
        send_opts = 'nomsg' if not _DEBUG else ''
        ret_obj = SendMsg(wb, 'stat', [search_dir], opts = send_opts)
    else:
        find_args_default = ['-f', '-a', '-s']
        if is_regex: find_args_default.insert(0, '-r')
        if find_args_list: find_args_default.extend(find_args_list)  # insert any other additional find arguments
        find_args_default.append(search_dir)
        find_args_default.append(pattern)
        send_opts = 'nomsg' if not _DEBUG else ''
        ret_obj = SendMsg(wb, 'find', find_args_default, opts = send_opts)

    if ret_obj.exitcode != 0:
        logging.error('list_files_grid error:: %s %s %s', search_dir, pattern, find_args)
        return ret_obj
    if 'results' not in ret_obj.ansdict or not ret_obj.ansdict["results"]:
        logging.error('list_files_grid exitcode==0 but no results(!!!):: %s /pattern: %s /find_args: %s', search_dir, pattern, find_args)
        return RET(2, '', f'No files found in :: {search_dir} /pattern: {pattern} /find_args: {find_args}')

    exitcode = ret_obj.exitcode
    stderr = ret_obj.err
    results_list = ret_obj.ansdict["results"]
    results_list_filtered = []
    # items that pass the conditions are the actual/final results

    compiled_regex = None
    if exclude_regex: compiled_regex = re.compile(exclude_regex)   # precompile the regex for exclusion

    for found_lfn_dict in results_list:  # parse results to apply filters
        if not filter_file_prop(found_lfn_dict, search_dir, filter_args_list, compiled_regex): continue
        results_list_filtered.append(found_lfn_dict)  # at this point all filters were passed

    if not results_list_filtered:
        return RET(2, "", f"No files passed the filters :: {search_dir} /pattern: {pattern} /find_args: {find_args}")

    ansdict = {"results": results_list_filtered}
    lfn_list = [get_lfn_key(lfn_obj) for lfn_obj in results_list_filtered]
    stdout = '\n'.join(lfn_list)
    return RET(exitcode, stdout, stderr, ansdict)





def makelist_lfn(wb, arg_source, arg_target, find_args: list, parent: int, overwrite: bool, pattern: Union[None, REGEX_PATTERN_TYPE, str], is_regex: bool, copy_list: list, strictspec: bool = False, httpurl: bool = False) -> RET:  # pylint: disable=unused-argument
    """Process a source and destination copy arguments and make a list of individual lfns to be copied"""
    isSrcDir = isSrcLocal = isDownload = specs = None  # make sure we set these to valid values later

    # lets extract the specs from both src and dst if any (to clean up the file-paths) and record specifications like disk=3,SE1,!SE2
    src_specs_remotes = specs_split.split(arg_source, maxsplit = 1)  # NO comma allowed in names (hopefully)
    arg_src = src_specs_remotes.pop(0)  # first item is the file path, let's remove it; it remains disk specifications
    src_specs = src_specs_remotes.pop(0) if src_specs_remotes else None  # whatever remains is the specifications

    dst_specs_remotes = specs_split.split(arg_target, maxsplit = 1)
    arg_dst = dst_specs_remotes.pop(0)
    dst_specs = dst_specs_remotes.pop(0) if dst_specs_remotes else None

    # lets process the pattern: extract it from src if is in the path globbing form
    src_glob = False
    if '*' in arg_src:  # we have globbing in src path
        src_glob = True
        arg_src, pattern = extract_glob_pattern(arg_src)
    else:  # pattern is specified by argument
        if type(pattern) is REGEX_PATTERN_TYPE:  # unlikely but supported to match signatures
            pattern = pattern.pattern  # We pass the regex pattern into command as string
            is_regex = True

        # it was explictly requested that pattern is regex
        if is_regex and type(pattern) is str and valid_regex(pattern) is None:
            msg = f"makelist_lfn:: {pattern} failed to re.compile"
            logging.error(msg)
            return RET(64, '', msg)  # EX_USAGE /* command line usage error */

    slashend_src = arg_src.endswith('/')  # after extracting the globbing if present we record the slash
    # N.B.!!! the check will be wrong when the same relative path is present local and on grid
    # first let's check only prefixes
    src, src_type = path_type(arg_src)
    dst, dst_type = path_type(arg_dst)

    if src_type == dst_type == 'grid':
        return RET(1, '', 'grid to grid copy is WIP; for the moment use two steps: download file and upload it; local src,dst should be ALWAYS prefixed with file:')
    if src_type == dst_type == 'local':
        return RET(1, '', 'for local copy use system command; within interactiv shell start a system command with "!"')

    isSrcLocal = (src_type == 'local')
    isDownload = not isSrcLocal
    if isSrcLocal:  # UPLOAD
        src_stat = path_local_stat(src)
        dst_stat = path_grid_stat(wb, dst)
    else:           # DOWNLOAD
        src_stat = path_grid_stat(wb, src)
        dst_stat = path_local_stat(dst)
        if not path_writable_any(dst_stat.path):
            return RET(2, '', f'no write permission/or missing in any component of {dst_stat.path}')

    if not src_stat.type: return RET(2, '', f'Specified source {src_stat.path} not found!')

    src = src_stat.path
    dst = dst_stat.path

    if not src: return RET(2, '', f'{arg_src} => {src} does not exist (or not accessible) on {src_type}')  # ENOENT /* No such file or directory */

    if slashend_src:
        if not src.endswith('/'): src = f"{src}/"  # recover the slash if lost
        if not dst.endswith('/'): dst = f"{dst}/"  # if src is dir, dst must be dir

    isSrcDir = (src_stat.type == 'd')
    if isSrcDir and not src_glob and not slashend_src: parent = parent + 1  # cp/rsync convention: with / copy the contents, without it copy the actual dir

    # prepare destination locations
    if isDownload:
        try:  # we can try anyway, this is like mkdir -p
            mk_path = Path(dst) if dst.endswith('/') else Path(dst).parent  # if destination is file create it dir parent
            mk_path.mkdir(parents=True, exist_ok=True)
        except Exception:
            logging.error(traceback.format_exc())
            msg = f"Could not create local destination directory: {mk_path.as_posix()}\ncheck log file {_DEBUG_FILE}"
            return RET(42, '', msg)  # ENOMSG /* No message of desired type */
    else:  # this is upload to GRID
        mk_path = dst if dst.endswith('/') else Path(dst).parent.as_posix()
        if not dst_stat.type:  # dst does not exists
            ret_obj = SendMsg(wb, 'mkdir', ['-p', mk_path], opts = 'nomsg')  # do it anyway, there is not point in checking before
            if retf_print(ret_obj, opts = 'noprint err') != 0: return ret_obj  # just return the mkdir result  # noqa: R504

    specs = src_specs if isDownload else dst_specs  # only the grid path can have specs
    specs_list = specs_split.split(specs) if specs else []

    if strictspec: print_out("Strict specifications were enabled!! Command may fail!!")
    if httpurl and isSrcLocal:
        print_out("httpurl option is ignored for uploads")
        httpurl = False

    error_msg = ''  # container which accumulates the error messages
    isWrite = not isDownload
    if isDownload:  # pylint: disable=too-many-nested-blocks  # src is GRID, we are DOWNLOADING from GRID location
        # to reduce the remote calls we treat files and directory on separate code-paths
        if src_stat.type == 'f':  # single file
            dst_filename = format_dst_fn(src, src, dst, parent)
            # if overwrite the file validity checking will do md5
            skip_file = (retf_print(fileIsValid(dst_filename, src_stat.size, src_stat.md5, shallow_check = not overwrite), opts = 'noerr') == 0)

            if not skip_file:
                tokens = lfn2fileTokens(wb, lfn2file(src, dst_filename), specs_list, isWrite, strictspec, httpurl)
                if tokens and 'answer' in tokens:
                    copy_list.append(CopyFile(src, dst_filename, isWrite, tokens['answer'], src))
        else:  # directory to be listed
            results_list = list_files_grid(wb, src, pattern, is_regex, " ".join(find_args))
            if "results" not in results_list.ansdict or len(results_list.ansdict["results"]) < 1:
                msg = f"No files found with: find {' '.join(find_args) if find_args else ''}{' -r ' if is_regex else ''}-a -s {src} {pattern}"
                return RET(42, '', msg)  # ENOMSG /* No message of desired type */

            for lfn_obj in results_list.ansdict["results"]:  # make CopyFile objs for each lfn
                lfn = get_lfn_key(lfn_obj)
                dst_filename = format_dst_fn(src, lfn, dst, parent)
                # if overwrite the file validity checking will do md5
                skip_file = (retf_print(fileIsValid(dst_filename, lfn_obj['size'], lfn_obj['md5'], shallow_check = not overwrite), opts = 'noerr') == 0)
                if skip_file: continue  # destination exists and is valid, no point to re-download
                
                tokens = lfn2fileTokens(wb, lfn2file(lfn, dst_filename), specs_list, isWrite, strictspec, httpurl)
                if not tokens or 'answer' not in tokens: continue
                copy_list.append(CopyFile(lfn, dst_filename, isWrite, tokens['answer'], lfn))

    else:  # src is LOCAL, we are UPLOADING
        results_list = list_files_local(src, pattern, is_regex, " ".join(find_args))
        if "results" not in results_list.ansdict or len(results_list.ansdict["results"]) < 1:
            msg = f"No files found in: {src} /pattern: {pattern} /find_args: {' '.join(find_args)}"
            return RET(42, '', msg)  # ENOMSG /* No message of desired type */

        for file in results_list.ansdict["results"]:
            file_path = get_lfn_key(file)
            print(file_path)
            lfn = format_dst_fn(src, file_path, dst, parent)
            lfn_dst_stat = path_grid_stat(wb, lfn)  # check each destination lfn
            if lfn_dst_stat.type == 'f':  # lfn exists
                if not overwrite:
                    print_out(f'{lfn} exists, skipping..')
                    continue
                md5sum = md5(file_path)
                if md5sum == lfn_dst_stat.md5:
                    print_out(f'{lfn} exists and md5 match, skipping..')
                    continue
                print_out(f'{lfn} exists and md5 does not match, deleting..')  # we want to overwrite so clear up the destination lfn
                ret_obj = SendMsg(wb, 'rm', ['-f', lfn], opts = 'nomsg')

            tokens = lfn2fileTokens(wb, lfn2file(lfn, file_path), specs_list, isWrite, strictspec)
            if not tokens or 'answer' not in tokens: continue
            copy_list.append(CopyFile(file_path, lfn, isWrite, tokens['answer'], lfn))
    return RET(1, '', error_msg) if error_msg else RET(0)


def makelist_xrdjobs(copylist_lfns: list, copylist_xrd: list):
    """Process a list of lfns to add to XRootD copy jobs list"""
    for cpfile in copylist_lfns:
        if 'results' not in cpfile.token_request:
            print_err(f"No token info for {cpfile}\nThis message should not happen! Please contact the developer if you see this!")
            continue

        if len(cpfile.token_request['results']) < 1:
            print_err(f'Could not find working replicas for {cpfile.src}')
            continue

        if cpfile.isUpload:  # src is local, dst is lfn, request is replica(pfn)
            for replica in cpfile.token_request['results']:
                copylist_xrd.append(CopyFile(cpfile.src, f"{replica['url']}?xrd.wantprot=unix&authz={replica['envelope']}", cpfile.isUpload, replica, cpfile.dst))
        else:  # src is lfn(remote), dst is local, request is replica(pfn)
            size_4meta = cpfile.token_request['results'][0]['size']  # size SHOULD be the same for all replicas
            md5_4meta = cpfile.token_request['results'][0]['md5']  # the md5 hash SHOULD be the same for all replicas
            file_in_zip = None
            url_list_4meta = []
            for replica in cpfile.token_request['results']:
                url_components = replica['url'].rsplit('#', maxsplit = 1)
                if len(url_components) > 1: file_in_zip = url_components[1]
                # if is_pfn_readable(url_components[0]):  # it is a lot cheaper to check readability of replica than to try and fail a non-working replica
                url_list_4meta.append(f'{url_components[0]}?xrd.wantprot=unix&authz={replica["envelope"]}')

            # Create the metafile as a temporary uuid5 named file (the lfn can be retrieved from meta if needed)
            metafile = create_metafile(make_tmp_fn(cpfile.src, '.meta4', uuid5 = True), cpfile.src, cpfile.dst, size_4meta, md5_4meta, url_list_4meta)
            if not metafile:
                print_err(f"Could not create the download metafile for {cpfile.src}")
                continue
            if file_in_zip and 'ALIENPY_NOXRDZIP' not in os.environ: metafile = f'{metafile}?xrdcl.unzip={file_in_zip}'
            if _DEBUG: print_out(f'makelist_xrdjobs:: {metafile}')
            copylist_xrd.append(CopyFile(metafile, cpfile.dst, cpfile.isUpload, {}, cpfile.src))  # we do not need the tokens in job list when downloading






def DO_XrootdCp(wb, xrd_copy_command: Union[None, list] = None, printout: str = '') -> RET:
    """XRootD cp function :: process list of arguments for a xrootd copy command"""
    if not _HAS_XROOTD: return RET(1, "", 'DO_XrootdCp:: python XRootD module not found or lower than 5.3.3, the copy process cannot continue')
    if xrd_copy_command is None: xrd_copy_command = []
    global AlienSessionInfo
    if not wb: return RET(107, "", 'DO_XrootdCp:: websocket not found')  # ENOTCONN /* Transport endpoint is not connected */

    if not xrd_copy_command or len(xrd_copy_command) < 2 or is_help(xrd_copy_command):
        help_msg = xrdcp_help()
        return RET(0, help_msg)  # EX_USAGE /* command line usage error */

    xrd_config_init()  # reset XRootD preferences to cp oriented settings

    # XRootD copy parameters
    # inittimeout: copy initialization timeout(int)
    # tpctimeout: timeout for a third-party copy to finish(int)
    # coerce: ignore file usage rules, i.e. apply `FORCE` flag to open() (bool)
    # :param checksummode: checksum mode to be used #:type    checksummode: string
    # :param checksumtype: type of the checksum to be computed  #:type    checksumtype: string
    # :param checksumpreset: pre-set checksum instead of computing it #:type  checksumpreset: string
    hashtype = str('md5')
    batch = int(1)   # from a list of copy jobs, start <batch> number of downloads
    streams = int(1)  # uses num additional parallel streams to do the transfer; use defaults from XrdCl/XrdClConstants.hh
    chunks = int(4)  # number of chunks that should be requested in parallel; use defaults from XrdCl/XrdClConstants.hh
    chunksize = int(8388608)  # chunk size for remote transfers; use defaults from XrdCl/XrdClConstants.hh
    overwrite = bool(False)  # overwrite target if it exists
    cksum = bool(False)
    timeout = int(0)
    rate = int(0)

    if get_arg(xrd_copy_command, '-d'):
        if os.getenv('XRD_LOGLEVEL'): print_out('XRD_LOGLEVEL already set, it will be overwritten with Info')
        XRD_EnvPut('XRD_LOGLEVEL', 'Info')
    if get_arg(xrd_copy_command, '-dd'):
        if os.getenv('XRD_LOGLEVEL'): print_out('XRD_LOGLEVEL already set, it will be overwritten with Debug')
        XRD_EnvPut('XRD_LOGLEVEL', 'Debug')
    if get_arg(xrd_copy_command, '-ddd'):
        if os.getenv('XRD_LOGLEVEL'): print_out('XRD_LOGLEVEL already set, it will be overwritten with Dump')
        XRD_EnvPut('XRD_LOGLEVEL', 'Dump')

    XRD_LOG = 'xrdlog.txt'
    xrd_logfile_arg = get_arg_value(xrd_copy_command, '-xrdlog')
    if xrd_logfile_arg:
        if os.getenv('XRD_LOGFILE'): print_out(f'XRD_LOGFILE already set, it will be overwritten with {xrd_logfile_arg}')
        XRD_LOG = xrd_logfile_arg
    XRD_EnvPut('XRD_LOGFILE', XRD_LOG)

    streams_arg = get_arg_value(xrd_copy_command, '-S')
    if streams_arg:
        if is_int(streams_arg):
            streams = min(abs(int(streams)), 15)
            if os.getenv('XRD_SUBSTREAMSPERCHANNEL'):
                print_out(f'Warning! env var XRD_SUBSTREAMSPERCHANNEL is set and will be overwritten with value: {streams}')
            XRD_EnvPut('SubStreamsPerChannel', streams)
    else:
        if not os.getenv('XRD_SUBSTREAMSPERCHANNEL'): XRD_EnvPut('SubStreamsPerChannel', streams)  # if no env customization, then use our defaults

    chunks_arg = get_arg_value(xrd_copy_command, '-chunks')
    if chunks_arg:
        if is_int(chunks_arg):
            chunks = abs(int(chunks_arg))
            if os.getenv('XRD_CPPARALLELCHUNKS'):
                print_out(f'Warning! env var XRD_CPPARALLELCHUNKS is set and will be overwritten with value: {chunks}')
            XRD_EnvPut('CPParallelChunks', chunks)
    else:
        if not os.getenv('XRD_CPPARALLELCHUNKS'): XRD_EnvPut('CPParallelChunks', chunks)

    chunksz_arg = get_arg_value(xrd_copy_command, '-chunksz')
    if chunksz_arg:
        if is_int(chunksz_arg):
            chunksize = abs(int(chunksz_arg))
            if os.getenv('XRD_CPCHUNKSIZE'):
                print_out(f'Warning! env var XRD_CPCHUNKSIZE is set and will be overwritten with value {chunksize}')
            XRD_EnvPut('CPChunkSize', chunksize)
    else:
        if not os.getenv('XRD_CPCHUNKSIZE'): XRD_EnvPut('CPChunkSize', chunksize)

    if get_arg(xrd_copy_command, '-noxrdzip'): os.environ["ALIENPY_NOXRDZIP"] = "nozip"

    timeout_arg = get_arg_value(xrd_copy_command, '-timeout')
    if timeout_arg:
        timeout = abs(int(timeout_arg))
        XRD_EnvPut('CPTimeout', timeout)

    rate_arg = get_arg_value(xrd_copy_command, '-ratethreshold')
    if rate_arg:
        rate = abs(int(rate_arg))
        XRD_EnvPut('XRateThreshold', rate)

    XRD_EnvPut('CpRetryPolicy', 'force')
    retry_arg = get_arg_value(xrd_copy_command, '-retry')
    if rate_arg:
        retry = abs(int(retry_arg))
        XRD_EnvPut('CpRetry', retry)

    _use_system_xrdcp = get_arg(xrd_copy_command, '-xrdcp')
    overwrite = get_arg(xrd_copy_command, '-f')
    cksum = get_arg(xrd_copy_command, '-cksum')

    tpc = 'none'
    if get_arg(xrd_copy_command, '-tpc'): tpc = 'first'
    if tpc != 'none': return RET(1, "", 'DO_XrootdCp:: TPC is not allowed!!')

    y_arg_val = get_arg_value(xrd_copy_command, '-y')
    # sources = int(y_arg_val)
    if y_arg_val: print_out("Ignored option! multiple source usage is known to break the files stored in zip files, so better to be ignored")

    batch = 8  # a nice enough default
    batch_arg = get_arg_value(xrd_copy_command, '-T')
    if batch_arg: batch = int(batch_arg)

    # options for envelope request
    strictspec = get_arg(xrd_copy_command, '-strictspec')
    httpurl = get_arg(xrd_copy_command, '-http')

    # keep this many path components into destination filepath
    parent = int(0)
    parent_arg = get_arg_value(xrd_copy_command, '-parent')
    if parent_arg: parent = int(parent_arg)

    # find options for recursive copy of directories
    find_args = []
    if get_arg(xrd_copy_command, '-v'): print_out("Verbose mode not implemented, ignored; enable debugging with ALIENPY_DEBUG=1")
    if get_arg(xrd_copy_command, '-a'): print_out("-a is enabled as default")
    if get_arg(xrd_copy_command, '-s'): print_out("-s is enabled as default")
    if get_arg(xrd_copy_command, '-f'): print_out("-f API flag not usefull for copy operations")
    if get_arg(xrd_copy_command, '-w'): print_out("-w flag not usefull for copy operations")
    if get_arg(xrd_copy_command, '-wh'): print_out("-wh flag not usefull for copy operations")
    if get_arg(xrd_copy_command, '-d'): print_out("-d flag not usefull for copy operations")

    mindepth_arg = get_arg_value(xrd_copy_command, '-mindepth')
    if mindepth_arg: find_args.extend(['-mindepth', mindepth_arg])

    maxdepth_arg = get_arg_value(xrd_copy_command, '-maxdepth')
    if maxdepth_arg: find_args.extend(['-maxdepth', maxdepth_arg])

    qid = get_arg_value(xrd_copy_command, '-j')
    if qid: find_args.extend(['-j', qid])

    files_limit = get_arg_value(xrd_copy_command, '-l')
    if files_limit: find_args.extend(['-l', files_limit])

    offset = get_arg_value(xrd_copy_command, '-o')
    if offset: find_args.extend(['-o', offset])

    use_regex = False
    filtering_enabled = False
    pattern = get_arg_value(xrd_copy_command, '-glob')
    if pattern:
        use_regex = False
        filtering_enabled = True

    pattern_regex = None
    select_arg = get_arg_value(xrd_copy_command, '-select')
    if select_arg:
        if filtering_enabled:
            msg = "Only one rule of selection can be used, either -select (full path match), -name (match on file name) or -glob (globbing)"
            return RET(22, '', msg)  # EINVAL /* Invalid argument */
        pattern_regex = select_arg
        use_regex = True
        filtering_enabled = True

    name_arg = get_arg_value(xrd_copy_command, '-name')
    if name_arg:
        if filtering_enabled:
            msg = "Only one rule of selection can be used, either -select (full path match), -name (match on file name) or -glob (globbing)"
            return RET(22, '', msg)  # EINVAL /* Invalid argument */
        use_regex = True
        filtering_enabled = True
        pattern_regex = name2regex(name_arg)
        if use_regex and not pattern_regex:
            msg = ("-name :: No selection verbs were recognized!"
                   "usage format is -name <attribute>_<string> where attribute is one of: begin, contain, ends, ext"
                   f"The invalid pattern was: {pattern_regex}")
            return RET(22, '', msg)  # EINVAL /* Invalid argument */

    if use_regex: pattern = pattern_regex
    copy_lfnlist = []  # list of lfn copy tasks

    inputfile_arg = get_arg_value(xrd_copy_command, '-input')  # input file with <source, destination> pairs
    if inputfile_arg:
        cp_arg_list = fileline2list(inputfile_arg)
        if not cp_arg_list: return RET(1, '', f'Input file {inputfile_arg} not found or invalid content')
        for cp_line in cp_arg_list:
            cp_line_items = cp_line.strip().split()
            if len(cp_line_items) > 2:
                print_out(f'Line skipped, it has more than 2 arguments => f{cp_line.strip()}')
                continue
            retobj = makelist_lfn(wb, cp_line_items[0], cp_line_items[1], find_args, parent, overwrite, pattern, use_regex, copy_lfnlist, strictspec, httpurl)
            retf_print(retobj, "noout err")  # print error and continue with the other files
    else:
        retobj = makelist_lfn(wb, xrd_copy_command[-2], xrd_copy_command[-1], find_args, parent, overwrite, pattern, use_regex, copy_lfnlist, strictspec, httpurl)
        if retobj.exitcode != 0: return retobj  # if any error let's just return what we got  # noqa: R504

    if not copy_lfnlist:  # at this point if any errors, the processing was already stopped
        return RET(0)

    if _DEBUG:
        logging.debug("We are going to copy these files:")
        for file in copy_lfnlist: logging.debug(file)

    # create a list of copy jobs to be passed to XRootD mechanism
    xrdcopy_job_list = []
    makelist_xrdjobs(copy_lfnlist, xrdcopy_job_list)

    if not xrdcopy_job_list:
        msg = "No XRootD operations in list! enable the DEBUG mode for more info"
        logging.info(msg)
        return RET(2, '', msg)  # ENOENT /* No such file or directory */

    if _DEBUG:
        logging.debug("XRootD copy jobs:")
        for file in xrdcopy_job_list: logging.debug(file)

    msg1 = msg2 = msg3 = msg_sum = ''
    copy_jobs_nr = copy_jobs_nr1 = copy_jobs_nr2 = 0
    copy_jobs_failed_nr = copy_jobs_failed_nr1 = copy_jobs_failed_nr2 = 0
    copy_jobs_success_nr = copy_jobs_success_nr1 = copy_jobs_success_nr2 = 0

    my_cp_args = XrdCpArgs(overwrite, batch, tpc, hashtype, cksum, timeout, rate)
    # defer the list of url and files to xrootd processing - actual XRootD copy takes place
    copy_failed_list = XrdCopy(wb, xrdcopy_job_list, my_cp_args, printout) if not _use_system_xrdcp else XrdCopy_xrdcp(xrdcopy_job_list, my_cp_args)
    copy_jobs_nr = len(xrdcopy_job_list)
    copy_jobs_failed_nr = len(copy_failed_list)
    copy_jobs_success_nr = copy_jobs_nr - copy_jobs_failed_nr
    msg1 = f"Succesful jobs (1st try): {copy_jobs_success_nr}/{copy_jobs_nr}" if not ('quiet' in printout or 'silent' in printout) else ''

    copy_failed_list2 = []
    if copy_failed_list:
        to_recover_list_try1 = []
        failed_lfns = {copy_job.lfn for copy_job in copy_failed_list if copy_job.isUpload}  # get which lfns had problems only for uploads
        for lfn in failed_lfns:  # process failed transfers per lfn
            failed_lfn_copy_jobs = [x for x in copy_failed_list if x.lfn == lfn]  # gather all failed copy jobs for one lfn
            failed_replica_nr = len(failed_lfn_copy_jobs)
            excluded_SEs_list = []
            for job in failed_lfn_copy_jobs:
                for se in job.token_request["SElist"]:
                    excluded_SEs_list.append(f'!{se}')
            excluded_SEs = ','.join(set(excluded_SEs_list))  # exclude already used SEs
            specs_list = f'disk:{failed_replica_nr},{excluded_SEs}'  # request N replicas (in place of failed ones), and exclude anything used

            job_file = failed_lfn_copy_jobs[0].token_request['file']
            job_lfn = failed_lfn_copy_jobs[0].token_request['lfn']
            job_isWrite = failed_lfn_copy_jobs[0].isUpload
            tokens_retry1 = lfn2fileTokens(wb, lfn2file(job_lfn, job_file), specs_list, job_isWrite, strictspec, httpurl)
            if not tokens_retry1 or 'answer' not in tokens_retry1: continue
            to_recover_list_try1.append(CopyFile(job_file, job_lfn, job_isWrite, tokens_retry1['answer'], job_lfn))

        if to_recover_list_try1:
            xrdcopy_job_list_2 = []
            makelist_xrdjobs(to_recover_list_try1, xrdcopy_job_list_2)
            copy_failed_list2 = XrdCopy(wb, xrdcopy_job_list_2, my_cp_args, printout)
            copy_jobs_nr1 = len(xrdcopy_job_list_2)
            copy_jobs_failed_nr1 = len(copy_failed_list2)
            copy_jobs_success_nr1 = copy_jobs_nr1 - copy_jobs_failed_nr1
            msg2 = f"Succesful jobs (2nd try): {copy_jobs_success_nr1}/{copy_jobs_nr1}" if not ('quiet' in printout or 'silent' in printout) else ''

    copy_failed_list3 = []
    if copy_failed_list2:
        to_recover_list_try2 = []
        failed_lfns2 = {copy_job.lfn for copy_job in copy_failed_list2 if copy_job.isUpload}  # get which lfns had problems only for uploads
        for lfn in failed_lfns2:  # process failed transfers per lfn
            failed_lfn_copy_jobs2 = [x for x in copy_failed_list2 if x.lfn == lfn]  # gather all failed copy jobs for one lfn
            failed_replica_nr = len(failed_lfn_copy_jobs2)
            excluded_SEs_list = []
            for job in failed_lfn_copy_jobs2:
                for se in job.token_request["SElist"]:
                    excluded_SEs_list.append(f'!{se}')
            excluded_SEs = ','.join(set(excluded_SEs_list))  # exclude already used SEs
            specs_list = f'disk:{failed_replica_nr},{excluded_SEs}'  # request N replicas (in place of failed ones), and exclude anything used

            job_file = failed_lfn_copy_jobs2[0].token_request['file']
            job_lfn = failed_lfn_copy_jobs2[0].token_request['lfn']
            job_isWrite = failed_lfn_copy_jobs2[0].isUpload
            tokens_retry2 = lfn2fileTokens(wb, lfn2file(job_lfn, job_file), specs_list, job_isWrite, strictspec, httpurl)
            if not tokens_retry2 or 'answer' not in tokens_retry1: continue
            to_recover_list_try2.append(CopyFile(job_file, job_lfn, job_isWrite, tokens_retry2['answer'], job_lfn))

        if to_recover_list_try2:
            xrdcopy_job_list_3 = []
            makelist_xrdjobs(to_recover_list_try2, xrdcopy_job_list_3)
            copy_failed_list3 = XrdCopy(wb, xrdcopy_job_list_3, my_cp_args, printout)
            copy_jobs_nr2 = len(xrdcopy_job_list_3)
            copy_jobs_failed_nr2 = len(copy_failed_list3)
            copy_jobs_success_nr2 = copy_jobs_nr2 - copy_jobs_failed_nr2
            msg3 = f'Succesful jobs (3rd try): {copy_jobs_success_nr2}/{copy_jobs_nr2}' if not ('quiet' in printout or 'silent' in printout) else ''

    # copy_jobs_failed_total = copy_jobs_failed_nr + copy_jobs_failed_nr1 + copy_jobs_failed_nr2
    copy_jobs_nr_total = copy_jobs_nr + copy_jobs_nr1 + copy_jobs_nr2
    copy_jobs_success_nr_total = copy_jobs_success_nr + copy_jobs_success_nr1 + copy_jobs_success_nr2
    # hard to return a single exitcode for a copy process optionally spanning multiple files
    # we'll return SUCCESS if at least one lfn is confirmed, FAIL if not lfns is confirmed
    msg_list = [msg1, msg2, msg3]
    if msg2 or msg3:
        msg_sum = f"Succesful jobs (total): {copy_jobs_success_nr_total}/{copy_jobs_nr_total}" if not ('quiet' in printout or 'silent' in printout) else ''
        msg_list.append(msg_sum)
    msg_all = '\n'.join(x.strip() for x in msg_list if x.strip())
    if 'ALIENPY_NOXRDZIP' in os.environ: os.environ.pop("ALIENPY_NOXRDZIP")
    return RET(0, msg_all) if copy_jobs_success_nr_total > 0 else RET(1, '', msg_all)


if _HAS_XROOTD:
    class MyCopyProgressHandler(xrd_client.utils.CopyProgressHandler):
        """Custom ProgressHandler for XRootD copy process"""
        __slots__ = ('wb', 'copy_failed_list', 'jobs', 'job_list', 'xrdjob_list', 'succesful_writes', 'printout', 'debug')

        def __init__(self):
            self.wb = None
            self.copy_failed_list = []  # record the failed jobs
            self.jobs = int(0)
            self.job_list = []
            self.xrdjob_list = []
            self.succesful_writes = []
            self.printout = ''
            self.debug = False

        def begin(self, jobId, total, source, target):
            timestamp_begin = datetime.datetime.now().timestamp()
            if not ('quiet' in self.printout or 'silent' in self.printout):
                print_out(f'jobID: {jobId}/{total} >>> Start')
            self.jobs = int(total)
            xrdjob = self.xrdjob_list[jobId - 1]
            file_size = xrdjob.token_request['size'] if xrdjob.isUpload else get_size_meta(xrdjob.src)

            jobInfo = {'src': source, 'tgt': target, 'bytes_total': file_size, 'bytes_processed': 0, 'start': timestamp_begin}
            self.job_list.insert(jobId - 1, jobInfo)
            if self.debug: logging.debug('CopyProgressHandler.src: %s\nCopyProgressHandler.dst: %s\n', source, target)

        def end(self, jobId, results):
            if results['status'].ok:
                status = f'{PrintColor(COLORS.Green)}OK{PrintColor(COLORS.ColorReset)}'
            elif results['status'].error:
                status = f'{PrintColor(COLORS.BRed)}ERROR{PrintColor(COLORS.ColorReset)}'
            elif results['status'].fatal:
                status = f'{PrintColor(COLORS.BIRed)}FATAL{PrintColor(COLORS.ColorReset)}'
            else:
                status = f'{PrintColor(COLORS.BIRed)}UNKNOWN{PrintColor(COLORS.ColorReset)}'
            job_info = self.job_list[jobId - 1]
            xrdjob = self.xrdjob_list[jobId - 1]  # joblist initilized when starting; we use the internal index to locate the job
            replica_dict = xrdjob.token_request
            job_status_info = f"jobID: {jobId}/{self.jobs} >>> STATUS {status}"

            deltaT = datetime.datetime.now().timestamp() - float(job_info['start'])
            if os.getenv('XRD_LOGLEVEL'): logging.debug('XRD copy job time:: %s -> %s', xrdjob.lfn, deltaT)

            if results['status'].ok:
                speed = float(job_info['bytes_total']) / deltaT
                speed_str = f'{GetHumanReadable(speed)}/s'

                if xrdjob.isUpload:  # isUpload
                    perm = '644'
                    expire = '0'
                    self.succesful_writes.append(CommitInfo(replica_dict['envelope'], replica_dict['size'], xrdjob.lfn, perm, expire, replica_dict['url'], replica_dict['se'], replica_dict['guid'], replica_dict['md5']))
                else:  # isDownload
                    # NOXRDZIP was requested
                    if 'ALIENPY_NOXRDZIP' in os.environ and os.path.isfile(xrdjob.dst) and zipfile.is_zipfile(xrdjob.dst):
                        src_file_name = os.path.basename(xrdjob.lfn)
                        dst_file_name = os.path.basename(xrdjob.dst)
                        dst_file_path = os.path.dirname(xrdjob.dst)
                        zip_name = f'{xrdjob.dst}_{uuid.uuid4()}.zip'
                        os.replace(xrdjob.dst, zip_name)
                        with zipfile.ZipFile(zip_name) as myzip:
                            if src_file_name in myzip.namelist():
                                out_path = myzip.extract(src_file_name, path = dst_file_path)
                                if out_path and (src_file_name != dst_file_name): os.replace(src_file_name, dst_file_name)
                            else:  # the downloaded file is actually a zip file
                                os.replace(zip_name, xrdjob.dst)
                        if os.path.isfile(zip_name): os.remove(zip_name)

                if not ('quiet' in self.printout or 'silent' in self.printout):
                    print_out(f"{job_status_info} >>> SPEED {speed_str}")
            else:
                self.copy_failed_list.append(xrdjob)
                codes_info = f">>> ERRNO/CODE/XRDSTAT {results['status'].errno}/{results['status'].code}/{results['status'].status}"
                xrd_resp_msg = results['status'].message
                failed_after = f'Failed after {deltaT}'
                if xrdjob.isUpload:
                    msg = f"{job_status_info} : {xrdjob.token_request['file']} to {xrdjob.token_request['se']}, {xrdjob.token_request['nSEs']} replicas\n{xrd_resp_msg}"
                else:
                    msg = f"{job_status_info} : {xrdjob.lfn}\n{xrd_resp_msg}"
                if _DEBUG: msg = f'{msg}\n{failed_after}'
                logging.error('\n%s\n%s', codes_info, msg)
                print_err(msg)
                defined_reqtimeout = float(XRD_EnvGet('RequestTimeout'))
                if deltaT >= defined_reqtimeout:
                    print_err(f'Copy job duration >= RequestTimeout default setting ({defined_reqtimeout}); Contact developer for support.')

            if not xrdjob.isUpload:
                meta_path = str(xrdjob.src).partition("?")[0]
                if os.getenv('ALIENPY_KEEP_META'):
                    subprocess.run(shlex.split(f'mv {meta_path} {os.getcwd()}/'), check = False)
                else:
                    os.remove(meta_path)  # remove the created metalink

        def update(self, jobId, processed, total):
            # self.job_list[jobId - 1]['bytes_total'] = total
            # self.job_list[jobId - 1]['bytes_processed'] = processed
            pass

        @staticmethod
        def should_cancel():  # self, jobId
            return False


def XrdCopy(wb, job_list: list, xrd_cp_args: XrdCpArgs, printout: str = '') -> list:
    """XRootD copy command :: the actual XRootD copy process"""
    if not _HAS_XROOTD:
        print_err("XRootD not found or lower than 5.3.3")
        return []
    if not xrd_cp_args:
        print_err("cp arguments are not set, XrdCpArgs tuple missing")
        return []

    # MANDATORY DEFAULTS, always used
    makedir = bool(True)  # create the parent directories when creating a file
    posc = bool(True)  # persist on successful close; Files are automatically deleted should they not be successfully closed.
    sources = int(1)  # max number of download sources; we (ALICE) do not rely on parallel multi-source downloads

    # passed arguments
    overwrite = xrd_cp_args.overwrite
    batch = xrd_cp_args.batch
    tpc = xrd_cp_args.tpc
    # hashtype = xrd_cp_args.hashtype
    cksum = xrd_cp_args.cksum
    # timeout = xrd_cp_args.timeout
    # rate = xrd_cp_args.rate

    cksum_mode = 'none'  # none | source | target | end2end
    cksum_type = ''
    cksum_preset = ''
    delete_invalid_chk = False
    if cksum:  # checksumming defaults good enough also for uploads
        xrd_client.EnvPutInt('ZipMtlnCksum', 1)
        cksum_mode = 'end2end'
        cksum_type = 'auto'
        delete_invalid_chk = True

    handler = MyCopyProgressHandler()
    handler.wb = wb
    handler.xrdjob_list = job_list
    handler.printout = printout
    handler.succesful_writes = []
    if _DEBUG: handler.debug = True

    process = xrd_client.CopyProcess()
    process.parallel(int(batch))
    for copy_job in job_list:
        if _DEBUG: logging.debug('\nadd copy job with\nsrc: %s\ndst: %s\n', copy_job.src, copy_job.dst)
        if cksum:
            if copy_job.isUpload:
                # WIP: checksumming with md5 for uploading breaks, keep it on auto
                # cksum_type = 'md5'
                # cksum_preset = copy_job.token_request['md5']
                pass
            else:  # for downloads we already have the md5 value, lets use that
                cksum_type, cksum_preset = get_hash_meta(copy_job.src)
                if not cksum_type or not cksum_preset:
                    cksum_type = ''
                    cksum_preset = ''
                    cksum_mode = 'none'
        process.add_job(copy_job.src, copy_job.dst,
                        sourcelimit = sources, posc = posc, mkdir = makedir,
                        force = overwrite, thirdparty = tpc,
                        checksummode = cksum_mode, checksumtype = cksum_type, checksumpreset = cksum_preset, rmBadCksum = delete_invalid_chk)

    process.prepare()
    process.run(handler)
    if handler.succesful_writes:  # if there were succesful uploads/remote writes, let's commit them to file catalogue
        ret_list = commitFileList(wb, handler.succesful_writes)
        for ret in ret_list: retf_print(ret, 'noout err')
    return handler.copy_failed_list  # lets see what failed and try to recover


def xrdfs_q_config(fqdn_port: str) -> dict:
    """Return a dictionary of xrdfs query config"""
    if not _HAS_XROOTD:
        print_err('python XRootD module not found')
        return None
    endpoint = xrd_client.FileSystem(f'{fqdn_port}/?xrd.wantprot=unix')

    config_args_list = ['bind_max', 'chksum', 'pio_max', 'readv_ior_max', 'readv_iov_max', 'tpc', 'wan_port', 'wan_window', 'window', 'cms', 'role', 'sitename', 'version']
    config_dict = {}
    for cfg in config_args_list:
        q_status, response = endpoint.query(7, cfg, timeout = 5)  # get the config metrics
        status = xrd_response2dict(q_status)
        if status['ok']:
            response = response.decode('ascii').strip()
            val = 'NOT_SET' if cfg == response else response
            config_dict[cfg] = val
        else:
            print_err(f'Query error for {fqdn_port} : {status["message"]}')
            break
    return config_dict


def xrdfs_ping(fqdn_port: str):
    """Return a dictionary of xrdfs ping, it will contain ping_time_ms key"""
    if not _HAS_XROOTD:
        print_err('python XRootD module not found')
        return None
    endpoint = xrd_client.FileSystem(f'{fqdn_port}/?xrd.wantprot=unix')
    result, _ = endpoint.ping(timeout = 2)  # ping the server 1st time to eliminate strange 1st time behaviour

    time_begin = time.perf_counter()
    result, _ = endpoint.ping(timeout = 2)  # ping the server
    ping_ms = deltat_ms_perf(time_begin)

    response_dict = xrd_response2dict(result)
    response_dict['ping_time_ms'] = float(ping_ms)
    return response_dict


def xrdfs_q_stats(fqdn_port: str, xml: bool = False, xml_raw: bool = False, compact: bool = False):
    if not _HAS_XROOTD:
        print_err('python XRootD module not found')
        return None
    endpoint = xrd_client.FileSystem(f'{fqdn_port}/?xrd.wantprot=unix')
    q_status, response = endpoint.query(1, 'a')  # get the stats (ALL)
    status = xrd_response2dict(q_status)
    if not status['ok']:
        print_err(f'xrdfs_q_stats:: query error to {fqdn_port} : {status["message"]}')
        return ''

    response = response.decode('ascii').strip().strip('\x00')
    # if xml is requested or xmltodict missing
    if xml:
        if xml_raw: return response
        # xml_stats = ET.fromstring(response)
        # return ET.dump(xml_stats)
        xml_stats = MD.parseString(response)
        indent = '  '
        newl = '\n'
        if compact: indent = newl = ''
        return xml_stats.toprettyxml(indent = indent, newl = newl).replace('&quot;', '"')

    try:
        import xmltodict
    except Exception:
        print_err('Could not import xmltodict, cannot convert the xml output to a dict view. try -xml argument')
        return None

    q_stats_dict = xmltodict.parse(response, attr_prefix = '')['statistics']
    old_stats = q_stats_dict.pop('stats')

    # it will mutate the input
    def convert_dict(input_dict: dict, head_key: str = 'id'):
        if isinstance(input_dict, dict) and head_key in input_dict:
            working_dict = dict(input_dict)
            key_name = working_dict.pop('id')
            new_dict = {key_name: working_dict}
            input_dict.clear()
            input_dict.update(new_dict)

    for id_entry in old_stats:
        convert_dict(id_entry)

    # to search for a recursive solution
    for i in old_stats:
        if 'oss' in i: convert_dict(i['oss']['paths']['stats'])

    merged_stats = {}
    for i in old_stats: merged_stats.update(i)
    q_stats_dict['stats'] = merged_stats

    return q_stats_dict


def xrd_response2dict(response_status: xrd_client.responses.XRootDStatus) -> dict:
    """Convert a XRootD response status answer to a dict"""
    if not response_status: return {}
    return {'status': response_status.status, 'code': response_status.code, 'errno': response_status.errno, 'message': response_status.message.strip(),
            'shellcode': response_status.shellcode, 'error': response_status.error, 'fatal': response_status.fatal, 'ok': response_status.ok}


def xrd_statinfo2dict(response_statinfo: xrd_client.responses.StatInfo) -> dict:
    """Convert a XRootD StatInfo answer to a dict"""
    if not response_statinfo: return {}
    return {'size': response_statinfo.size, 'flags': response_statinfo.flags, 'modtime': response_statinfo.modtime, 'modtimestr': response_statinfo.modtimestr}


def xrdstat2dict(xrdstat: tuple) -> dict:
    """Convert a XRootD status answer to a dict"""
    if not xrdstat: return {}
    xrd_stat, xrd_info = xrdstat
    xrdstat_dict = xrd_response2dict(xrd_stat)
    xrdinfo_dict = xrd_statinfo2dict(xrd_info)
    return {**xrdstat_dict, **xrdinfo_dict}


def xrdfs_stat(pfn: str):
    if not _HAS_XROOTD:
        print_err('python XRootD module not found')
        return None
    url_components = urlparse(pfn)
    endpoint = xrd_client.FileSystem(url_components.netloc)
    return endpoint.stat(f'{url_components.path}?xrd.wantprot=unix')


def xrdstat_flags2dict(flags: int) -> dict:
    """Convert the flags information of a XRootD file status to a dict"""
    return {'x_bit_set': bool(flags & xrd_client.flags.StatInfoFlags.X_BIT_SET),
            'is_dir': bool(flags & xrd_client.flags.StatInfoFlags.IS_DIR),
            'other': bool(flags & xrd_client.flags.StatInfoFlags.OTHER),
            'offline': bool(flags & xrd_client.flags.StatInfoFlags.OFFLINE),
            'is_readable': bool(flags & xrd_client.flags.StatInfoFlags.IS_READABLE),
            'is_writable': bool(flags & xrd_client.flags.StatInfoFlags.IS_WRITABLE),
            'posc_pending': bool(flags & xrd_client.flags.StatInfoFlags.POSC_PENDING),
            'backup_exists': bool(flags & xrd_client.flags.StatInfoFlags.BACKUP_EXISTS)}


def is_pfn_readable(pfn: str) -> bool:
    get_pfn_info = xrdstat2dict(xrdfs_stat(pfn))
    if 'flags' in get_pfn_info:
        pfn_flags = xrdstat_flags2dict(get_pfn_info['flags'])
        return pfn_flags['is_readable']
    return False



def get_pfn_list(wb, lfn: str) -> list:
    if not wb: return []
    if not lfn: return []
    if pathtype_grid(wb, lfn) != 'f': return []
    ret_obj = SendMsg(wb, 'whereis', [lfn], opts = 'nomsg')
    retf_print(ret_obj, 'debug')
    return [str(item['pfn']) for item in ret_obj.ansdict['results']]




def get_lfn_meta(meta_fn: str) -> str:
    if 'meta4?' in meta_fn: meta_fn = meta_fn.partition('?')[0]
    if not os.path.isfile(meta_fn): return ''
    return MD.parse(meta_fn).documentElement.getElementsByTagName('lfn')[0].firstChild.nodeValue


def get_size_meta(meta_fn: str) -> int:
    if 'meta4?' in meta_fn: meta_fn = meta_fn.partition('?')[0]
    if not os.path.isfile(meta_fn): return int(0)
    return int(MD.parse(meta_fn).documentElement.getElementsByTagName('size')[0].firstChild.nodeValue)


def get_hash_meta(meta_fn: str) -> tuple:
    if 'meta4?' in meta_fn: meta_fn = meta_fn.partition('?')[0]
    if not os.path.isfile(meta_fn): return ('', '')
    content = MD.parse(meta_fn).documentElement.getElementsByTagName('hash')[0]
    return (content.getAttribute('type'), content.firstChild.nodeValue)


def lfn2tmp_fn(lfn: str = '', uuid5: bool = False) -> str:
    """make temporary file name that can be reconstructed back to the lfn"""
    if not lfn: return str(uuid.uuid4())
    if uuid5:
        return str(uuid.uuid5(uuid.NAMESPACE_URL, lfn))
    return lfn.replace("/", '%%')


def make_tmp_fn(lfn: str = '', ext: str = '', uuid5: bool = False) -> str:
    """make temporary file path string either random or based on grid lfn string"""
    if not ext: ext = f'_{str(os.getuid())}.alienpy_tmp'
    return f'{__TMPDIR}/{lfn2tmp_fn(lfn, uuid5)}{ext}'


def get_lfn_name(tmp_name: str = '', ext: str = '') -> str:
    lfn = tmp_name.replace(ext, '') if ext else tmp_name.replace(f'_{str(os.getuid())}.alienpy_tmp', '')
    return lfn.replace(f'{__TMPDIR}/', '').replace("%%", "/")


def download_tmp(wb, lfn: str, overwrite: bool = False, verbose: bool = False) -> str:
    """Download a lfn to a temporary file, it will return the file path of temporary"""
    global AlienSessionInfo
    tmpfile = make_tmp_fn(expand_path_grid(lfn))
    if os.path.isfile(tmpfile):
        if overwrite:
            os.remove(tmpfile)
            if tmpfile in AlienSessionInfo['templist']: AlienSessionInfo['templist'].remove(tmpfile)
        else:
            if tmpfile not in AlienSessionInfo['templist']: AlienSessionInfo['templist'].append(tmpfile)
            return tmpfile

    if tmpfile in AlienSessionInfo['templist']: AlienSessionInfo['templist'].remove(tmpfile)  # just in case it is still in list
    copycmd = f"-f {lfn} file:{tmpfile}"
    ret_obj = DO_XrootdCp(wb, copycmd.split(), printout = 'silent')  # print only errors for temporary downloads
    if ret_obj.exitcode == 0 and os.path.isfile(tmpfile):
        AlienSessionInfo['templist'].append(tmpfile)
        return tmpfile
    if verbose: print_err(f'{ret_obj.err}')
    return ''


def upload_tmp(wb, temp_file_name: str, upload_specs: str = '', dated_backup: bool = False) -> str:
    """Upload a temporary file: the original lfn will be renamed and the new file will be uploaded with the original lfn"""
    lfn = get_lfn_name(temp_file_name)  # lets recover the lfn from temp file name
    lfn_backup = f'{lfn}.{now_str()}' if dated_backup else f'{lfn}~'
    if not dated_backup:
        ret_obj = SendMsg(wb, 'rm', ['-f', lfn_backup])  # remove already present old backup; useless to pre-check
    ret_obj = SendMsg(wb, 'mv', [lfn, lfn_backup])  # let's create a backup of old lfn
    if retf_print(ret_obj, 'debug') != 0: return ''
    tokens = lfn2fileTokens(wb, lfn2file(lfn, temp_file_name), [upload_specs], isWrite = True)
    access_request = tokens['answer']
    replicas = access_request["results"][0]["nSEs"]
    if "disk:" not in upload_specs: upload_specs = f'disk:{replicas}'
    if upload_specs: upload_specs = f'@{upload_specs}'
    copycmd = f'-f file:{temp_file_name} {lfn}{upload_specs}'
    ret_obj = DO_XrootdCp(wb, copycmd.split())
    if ret_obj.exitcode == 0: return lfn
    ret_obj = SendMsg(wb, 'mv', [lfn_backup, lfn])  # if the upload failed let's move back the backup to original lfn name'
    retf_print(ret_obj, 'debug')
    return ''





if __name__ == '__main__':
    print('This file should not be executed!', file = sys.stderr, flush = True)
    sys.exit(95)
    
    








