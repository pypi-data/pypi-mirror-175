

def DO_xrd_ping(wb, args: Union[list, None] = None) -> RET:
    global AlienSessionInfo
    if args is None: args = []
    if not args or is_help(args):
        msg = ('Command format: xrd_ping [-c count] fqdn[:port] | SE name | SE id\n'
               'It will use the XRootD connect/ping option to connect and return a RTT')
        return RET(0, msg)

    count_arg = get_arg_value(args, '-c')
    count = int(count_arg) if count_arg else 3

    sum_rez = []
    for se_name in args:
        ret_obj = DO_getSE(wb, ['-srv', se_name])
        if 'results' in ret_obj.ansdict: sum_rez.extend(ret_obj.ansdict['results'])

    # maybe user want to ping servers outside of ALICE redirectors list
    if not sum_rez:
        for arg in args: sum_rez.append({'seName': arg, 'endpointUrl': f'root://{arg}'})

    msg = f'XRootD ping(s): {count} time(s) to:'
    for se in sum_rez:
        se_name = se['seName']
        se_fqdn = urlparse(se['endpointUrl']).netloc

        results_list = []
        for _i in range(count): results_list.append(xrdfs_ping(se_fqdn))

        results = [res['ping_time_ms'] for res in results_list if res['ok']]
        if results:
            rtt_min = min(results)
            rtt_max = max(results)
            rtt_avg = statistics.mean(results)
            rtt_stddev = statistics.stdev(results) if len(results) > 1 else 0.0
            msg = f'{msg}\n{se_name : <32} rtt min/avg/max/mdev (ms) = {rtt_min:.3f}/{rtt_avg:.3f}/{rtt_max:.3f}/{rtt_stddev:.3f}'
        else:
            msg = f'{msg}\n{se_name : <32} {results_list[-1]["message"]}'

    return RET(0, msg)


def DO_xrd_config(wb, args: Union[list, None] = None) -> RET:
    global AlienSessionInfo
    if args is None: args = []
    if not args or is_help(args):
        msg = ('Command format: xrd_config [-v | -verbose] fqdn[:port] | SE name | SE id\n'
               'It will use the XRootD query config to get the current server properties\n'
               'verbose mode will print more about the server configuration')
        return RET(0, msg)
    verbose = get_arg(args, '-v') or get_arg(args, '-verbose')
    all_alice_sites = get_arg(args, '-a') or get_arg(args, '-all')

    sum_rez = []
    if all_alice_sites:
        ret_obj = DO_getSE(wb, ['-srv'])
        if 'results' in ret_obj.ansdict: sum_rez.extend(ret_obj.ansdict['results'])
    else:
        for se_name in args:
            ret_obj = DO_getSE(wb, ['-srv', se_name])
            if 'results' in ret_obj.ansdict: sum_rez.extend(ret_obj.ansdict['results'])

    # maybe user want to ping servers outside of ALICE redirectors list
    if not sum_rez:
        for arg in args: sum_rez.append({'seName': arg, 'endpointUrl': f'root://{arg}'})

    config_list = []
    msg_list = []
    for se in sum_rez:
        se_name = se['seName']
        se_fqdn = urlparse(se['endpointUrl']).netloc
        cfg = xrdfs_q_config(se_fqdn)
        if not cfg or 'sitename' not in cfg: continue
        cfg['seName'] = se_name  # xrootd 'sitename' could be undefined
        cfg['endpointUrl'] = se_fqdn
        if cfg['sitename'] == "NOT_SET" or not cfg['sitename']: cfg['sitename'] = se['seName']
        config_list.append(cfg)

        msg = f'Site/XrdVer: {cfg["sitename"] if cfg["sitename"] != "NOT_SET" or not cfg["sitename"] else cfg["seName"]}/{cfg["version"]} ; TPC status: {cfg["tpc"]} ; role: {cfg["role"]} ; CMS: {cfg["cms"]}'
        if verbose:
            msg = (f'{msg}\n'
                   f'Chksum type: {cfg["chksum"]} ; Bind max: {cfg["bind_max"]} ; PIO max: {cfg["pio_max"]} ; '
                   f'Window/WAN window: {cfg["window"]}/{cfg["wan_window"]} ; readv_{{ior,iov}}_max: {cfg["readv_ior_max"]}/{cfg["readv_iov_max"]}')

        msg_list.append(msg)

    results_dict = {'results': config_list}
    msg_all = '\n'.join(msg_list)
    return RET(0, msg_all, '', results_dict)


def DO_xrd_stats(wb, args: Union[list, None] = None) -> RET:
    global AlienSessionInfo
    if args is None: args = []
    if not args or is_help(args):
        msg = ('Command format: xrd_stats [ -xml | -xmlraw | -compact  ]  fqdn[:port] | SE name | SE id\n'
               'It will use the XRootD query stats option to get the server metrics\n'
               '-xml : print xml output (native to xrootd)\n'
               '-xmlraw : print rawxml output without any indentation\n'
               '-compact : print the most compact version of the output, with minimal white space\n')
        return RET(0, msg)
    compact = get_arg(args, '-compact')
    xml_out = get_arg(args, '-xml')
    xml_raw = get_arg(args, '-xmlraw')
    if xml_raw: xml_out = True
    all_alice_sites = get_arg(args, '-a') or get_arg(args, '-all')

    sum_rez = []
    if all_alice_sites:
        ret_obj = DO_getSE(wb, ['-srv'])
        if 'results' in ret_obj.ansdict: sum_rez.extend(ret_obj.ansdict['results'])
    else:
        for se_name in args:
            ret_obj = DO_getSE(wb, ['-srv', se_name])
            if 'results' in ret_obj.ansdict: sum_rez.extend(ret_obj.ansdict['results'])

    # maybe user want to ping servers outside of ALICE redirectors list
    if not sum_rez:
        for arg in args: sum_rez.append({'seName': arg, 'endpointUrl': f'root://{arg}'})

    stats_list = []
    msg_list = []
    for se in sum_rez:
        se_name = se['seName']
        se_fqdn = urlparse(se['endpointUrl']).netloc
        stats = xrdfs_q_stats(se_fqdn, xml = xml_out, xml_raw = xml_raw, compact = compact)
        if not stats: continue

        if xml_out:
            stats_list.append('XML output only, no json content')
            msg_list.append(f'{stats}')
            continue  # if plain xml output stop processing

        stats['seName'] = se_name  # xrootd 'sitename' could be undefined
        stats['endpointUrl'] = se_fqdn
        if stats['site'] == "NOT_SET" or not stats['site']: stats['site'] = se['seName']
        stats_list.append(stats)
        indent = None if compact else '  '
        separators = (',', ':') if compact else (', ', ': ')
        msg_list.append(json.dumps(stats, indent = indent, separators = separators).replace('\\"', ''))

    results_dict = {'results': stats_list}
    msg_all = '\n'.join(msg_list)
    exitcode = 1 if not results_dict else 0
    return RET(exitcode, msg_all, '', results_dict)


def DO_pfn(wb, args: Union[list, None] = None) -> RET:
    if args is None: args = []
    if is_help(args):
        msg = 'Command format : pfn [lfn]\nIt will print only the list of associated pfns (simplified form of whereis)'
        return RET(0, msg)
    args.insert(0, '-r')
    ret_obj = SendMsg(wb, 'whereis', args, opts = 'nomsg')
    msg = '\n'.join(str(item['pfn']) for item in ret_obj.ansdict['results'] if 'pfn' in item).strip()
    return ret_obj._replace(out = msg)


def DO_pfnstatus(wb, args: Union[list, None] = None) -> RET:
    global AlienSessionInfo
    if args is None: args = []
    if not args or is_help(args):
        msg = ('Command format: pfn_status <pfn>|<lfn>\n'
               'It will return all flags reported by the xrootd server - this is direct access to server\n'
               'pfn is identified by prefix root://; if missing the argument will be taken to be a lfn')
        return RET(0, msg)
    verbose = get_arg(args, '-v') or get_arg(args, '-verbose')
    pfn_list = []
    # create a list of all pfns to be queried
    for arg in args:
        if arg.startswith('root://'):
            pfn_list.append({'lfn': '', 'pfn': arg})
        else:
            # we assume that it's a lfn
            file_path = expand_path_grid(arg)
            pfns_ret = DO_pfn(wb, [file_path])
            pfn_list_found = [{'lfn': file_path, 'pfn': str(item['pfn'])} for item in pfns_ret.ansdict['results'] if 'pfn' in item]
            pfn_list.extend(pfn_list_found)

    msg_all = None
    dict_results = {"results": []}
    for pfn in pfn_list:
        get_pfn_info = xrdstat2dict(xrdfs_stat(pfn['pfn']))
        if 'flags' in get_pfn_info:
            pfn_flags = xrdstat_flags2dict(get_pfn_info['flags'])
            get_pfn_info.pop('flags')
        else:
            pfn_flags = {}

        pfn_info = {'lfn': pfn['lfn'], 'pfn': pfn['pfn'], **get_pfn_info, **pfn_flags}
        dict_results['results'].append(pfn_info)
        msg = None
        if pfn["lfn"]: msg = f'LFN: {pfn["lfn"]}\n'
        if pfn_info['ok']:
            # ( f'{msg if msg else ""}'
            msg = f'{msg if msg else ""}{pfn["pfn"]}\t\tSize: {pfn_info["size"]}\tR/W status:{int(pfn_info["is_readable"])}/{int(pfn_info["is_writable"])}\n'
            if verbose: msg = (f'{msg}'
                               f'IS DIR/OTHER/OFFLINE: {int(pfn_info["is_dir"])}/{int(pfn_info["other"])}/{int(pfn_info["offline"])}\t'
                               f'Modified: {pfn_info["modtimestr"]}\tPOSC pending: {int(pfn_info["posc_pending"])}\t\tBACKUP: {int(pfn_info["backup_exists"])}\n')
        else:
            msg = (f'{msg if msg else ""}'
                   f'{pfn["pfn"]}\t\tMessage: {pfn_info["message"]}\tStatus/Code/ErrNo:{pfn_info["status"]}/{pfn_info["code"]}/{pfn_info["errno"]}\n')

        msg_all = f'{msg_all if msg_all else ""}{msg}'

    return RET(0, msg_all, '', dict_results)


def DO_getSE(wb, args: list = None) -> RET:
    if not wb: return []
    if not args: args = []
    if is_help(args):
        msg = 'Command format: getSE <-id | -name | -srv> identifier_string\nReturn the specified property for the SE specified label'
        return RET(0, msg)

    ret_obj = SendMsg(wb, 'listSEs', [], 'nomsg')
    if ret_obj.exitcode != 0: return ret_obj

    arg_select = ''  # default return
    if get_arg(args, '-name'): arg_select = 'name'
    if get_arg(args, '-id'): arg_select = 'id'
    if get_arg(args, '-srv'): arg_select = 'srv'

    if not args:
        se_list = [f"{se['seNumber'] : <6}{se['seName'] : <32}{urlparse(se['endpointUrl']).netloc.strip()}" for se in ret_obj.ansdict["results"]]
        return RET(0, '\n'.join(se_list), '', ret_obj.ansdict)

    def match_name(se: Union[dict, None] = None, name: str = '') -> bool:
        if se is None or not name: return False
        if name.isdecimal(): return name in se['seNumber']
        return name.casefold() in se['seName'].casefold() or name.casefold() in se['seNumber'].casefold() or name.casefold() in se['endpointUrl'].casefold()

    se_name = args[-1].casefold()
    rez_list = []
    se_list = [se for se in ret_obj.ansdict["results"] if match_name(se, se_name)]
    if not se_list: return RET(1, '', f">{args[-1]}< label(s) not found in SE list")

    for se_info in se_list:
        srv_name = urlparse(se_info["endpointUrl"]).netloc.strip()
        if arg_select == 'name':
            rez_list.append(se_info['seName'])
        elif arg_select == 'srv':
            rez_list.append(srv_name)
        elif arg_select == 'id':
            rez_list.append(se_info['seNumber'])
        else:
            if se_name.isdecimal():
                rez_list.append(f"{se_info['seName'] : <32}{srv_name}")
            else:
                rez_list.append(f"{se_info['seNumber'] : <6}{se_info['seName'] : <32}{srv_name}")

    if not rez_list: return RET(1, '', f"Empty result when searching for: {args[-1]}")
    return RET(0, '\n'.join(rez_list), '', {'results': se_list})


def DO_SEqos(wb, args: list = None) -> RET:
    if not wb: return RET()
    if not args or is_help(args):
        msg = 'Command format: SEqos <SE name>\nReturn the QOS tags for the specified SE (ALICE:: can be ommited and capitalization does not matter)'
        return RET(0, msg)
    sum_rez = []
    for se_name in args:
        ret_obj = DO_getSE(wb, [se_name])
        if 'results' in ret_obj.ansdict: sum_rez.extend(ret_obj.ansdict['results'])
    if not sum_rez: return RET(1, '', f'No SE information found! -> {" ".join(args)}')
    msg = None
    for se in sum_rez:
        msg = f'{msg if msg else ""}{se["seName"] : <32}{se["qos"]}\n'
    return RET(0, msg, '', {'results': sum_rez})


def DO_2xml(wb, args: Union[list, None] = None) -> RET:
    if args is None: args = []
    if not args or is_help(args):
        central_help = SendMsg(wb, 'toXml', ['-h'], opts = 'nokeys')
        central_help_msg = central_help.out
        msg_local = ('\nAdditionally the client implements these options:'
                     '\n-local: specify that the target lfns are local files'
                     '\nfor -x (output file) and -l (file with lfns) the file: and alien: represent the location of file'
                     '\nthe inferred defaults are that the target files and the output files are of the same type'
                     )
        msg = f'{central_help_msg}{msg_local}'
        return RET(0, msg)

    is_local = get_arg(args, '-local')
    ignore_missing = get_arg(args, '-i')
    do_append = get_arg(args, '-a')
    output_file = get_arg_value(args, '-x')
    if do_append and output_file is None: return RET(1, '', 'Append operation need -x argument for specification of target file')

    lfn_filelist = get_arg_value(args, '-l')

    lfn_list = []
    lfn_arg_list = None

    if lfn_filelist:  # a given file with list of files/lfns was provided
        if is_local:
            if do_append: return RET(1, '', 'toXml::local usage - appending to local xml is WIP, try without -a')
            if not os.path.exists(lfn_filelist): return RET(1, '', f'filelist {lfn_filelist} could not be found!!')
            filelist_content_list = file2list(lfn_filelist)
            if not filelist_content_list: return RET(1, '', f'No files could be read from {lfn_filelist}')
            if filelist_content_list[0].startswith('alien:'):
                return RET(1, '', 'Local filelists should contain only local files (not alien: lfns)')
            xml_coll = mk_xml_local(filelist_content_list)
            if output_file:
                if output_file.startswith('alien:'):
                    return RET(1, '', 'For the moment upload the resulting file by hand in grid')
                output_file = lfn_prefix_re.sub('', output_file)
                try:
                    with open(output_file, 'w', encoding = "ascii", errors = "replace") as f: f.write(xml_coll)
                    return RET(0)
                except Exception as e:
                    logging.exception(e)
                    return RET(1, '', f'Error writing {output_file}')
            return RET(0, xml_coll)
        else:
            grid_args = []
            if ignore_missing: grid_args.append('-i')
            if do_append: grid_args.append('-a')
            if lfn_filelist: grid_args.extend(['-l', lfn_filelist])
            if output_file and not output_file.startswith("file:"): grid_args.extend(['-x', lfn_prefix_re.sub('', output_file)])
            ret_obj = SendMsg(wb, 'toXml', grid_args)
            if output_file and output_file.startswith("file:"):
                output_file = lfn_prefix_re.sub('', output_file)
                try:
                    with open(output_file, 'w', encoding = "ascii", errors = "replace") as f: f.write(ret_obj.out)
                    return RET(0)
                except Exception as e:
                    logging.exception(e)
                    return RET(1, '', f'Error writing {output_file}')
            return ret_obj
        return RET(1, '', 'Allegedly unreachable point in DO_2xml. If you see this, contact developer!')

    else:
        lfn_arg_list = args.copy()  # the rest of arguments are lfns
        if is_local:
            if do_append: return RET(1, '', 'toXml::local usage - appending to local xml is WIP, try without -a')
            lfn_list_obj_list = [file2file_dict(filepath) for filepath in lfn_arg_list]
            if not lfn_list_obj_list: return RET(1, '', f'Invalid list of files: {lfn_arg_list}')
            lfn_list = [get_lfn_key(lfn_obj) for lfn_obj in lfn_list_obj_list if get_lfn_key(lfn_obj)]
            xml_coll = mk_xml_local(lfn_list)
            if output_file:
                if output_file.startswith('alien:'):
                    return RET(1, '', 'For the moment upload the resulting file by hand in grid')
                output_file = lfn_prefix_re.sub('', output_file)
                with open(output_file, 'w', encoding = "ascii", errors = "replace") as f: f.write(xml_coll)
                return RET(0)
            return RET(0, xml_coll)
        else:
            grid_args = []
            if ignore_missing: grid_args.append('-i')
            if do_append: grid_args.append('-a')
            if output_file and not output_file.startswith("file:"): grid_args.extend(['-x', lfn_prefix_re.sub('', output_file)])
            grid_args.extend(lfn_arg_list)
            ret_obj = SendMsg(wb, 'toXml', grid_args)
            if output_file and output_file.startswith("file:"):
                output_file = lfn_prefix_re.sub('', output_file)
                try:
                    with open(output_file, 'w', encoding = "ascii", errors = "replace") as f: f.write(ret_obj.out)
                    return RET(0)
                except Exception as e:
                    logging.exception(e)
                    return RET(1, '', f'Error writing {output_file}')
            return ret_obj
        return RET(1, '', 'Allegedly unreachable point in DO_2xml. If you see this, contact the developer!')




def DO_submit(wb, args: Union[list, None] = None) -> RET:
    """submit: process submit commands for local jdl cases"""
    if not args or args is None: args = ['-h']
    if is_help(args): return get_help_srv(wb, 'submit')
    if args[0].startswith("file:"):
        msg = ("Specifications as where to upload the jdl to be submitted and with what parameters are not yet defined"
               "Upload first the jdl to a suitable location (with a safe number of replicas) and then submit")
        return RET(0, msg)
    args[0] = expand_path_grid(args[0])
    return SendMsg(wb, 'submit', args)


def DO_ps(wb, args: Union[list, None] = None) -> RET:
    """ps : show and process ps output"""
    if args is None: args = []
    ret_obj = SendMsg(wb, 'ps', args)
    if '-trace' in args:
        nice_lines = [convert_time(str(msgline)) for item in ret_obj.ansdict['results'] for msgline in item['message'].split('\n')]
        return ret_obj._replace(out = '\n'.join(nice_lines))
    return ret_obj


def DO_cat(wb, args: Union[list, None] = None) -> RET:
    """cat lfn :: apply cat on a downloaded lfn as a temporary file"""
    args.insert(0, '-noout')  # keep app open, do not terminate
    args.insert(0, 'cat')
    return DO_run(wb, args, external = True)


def DO_less(wb, args: Union[list, None] = None) -> RET:
    """less lfn :: apply less on a downloaded lfn as a temporary file"""
    args.insert(0, '-noout')  # keep app open, do not terminate
    args.insert(0, 'less')
    return DO_run(wb, args, external = True)


def DO_more(wb, args: Union[list, None] = None) -> RET:
    """more lfn :: apply more on a downloaded lfn as a temporary file"""
    args.insert(0, '-noout')  # keep app open, do not terminate
    args.insert(0, 'more')
    return DO_run(wb, args, external = True)


def DO_lfn2uri(wb, args: Union[list, None] = None) -> RET:
    if args is None: args = []
    if is_help(args):
        msg = '''Command format : lfn2uri <lfn> <local_file?> [meta] [write|upload] [strict] [http]
It will print the URIs for lfn replicas
local_file : required only for write|upload URIs
meta : will write in current directory the metafile and will return the string to be used with xrdcp
write|upload : request tokens for writing/upload; incompatible with <meta> argument
strict : lfn specifications will be considered to be strict
http : URIs will be for http end-points of enabled SEs
'''
        return RET(0, msg)

    write_meta = get_arg(args, 'meta')
    strictspec = get_arg(args, 'strict')
    httpurl = get_arg(args, 'http')
    isWrite = get_arg(args, 'upload')
    if not isWrite: isWrite = get_arg(args, 'write')
    if isWrite and write_meta:
        return RET(1, '', 'meta argument is incompatible with uploading')
    if isWrite and len(args) < 2: return RET(1, '', 'for upload URIs two elements are required: lfn local_file')
    if len(args) < 1: return RET(1, '', 'at least one argument is neeeded: lfn')
    local_file = ''
    if len(args) > 1: local_file = args[1]
    lfn = args[0]
    lfn_components = specs_split.split(lfn, maxsplit = 1)  # NO comma allowed in grid names (hopefully)
    lfn = lfn_components[0]  # first item is the file path, let's remove it; it remains disk specifications
    if not isWrite: lfn = expand_path_grid(lfn)
    specs = ''
    if len(lfn_components) > 1: specs = lfn_components[1]
    if write_meta:  # noqa: IFSTMT001
        out = lfn2meta(wb, lfn, local_file, specs, isWrite, strictspec, httpurl)
    else:
        out = lfn2uri(wb, lfn, local_file, specs, isWrite, strictspec, httpurl)
    if not out:
        return RET(1, '', f'Could not not create URIs for: {lfn}')
    return RET(0, out)


def DO_token(wb, args: Union[list, None] = None) -> RET:
    if args is None: args = []
    msg = "Print only command!!! Use >token-init< for token (re)generation, see below the arguments\n"
    ret_obj = SendMsg(wb, 'token', args, opts = 'nokeys')
    return ret_obj._replace(out = f'{msg}{ret_obj.out}')


def DO_token_init(wb, args: Union[list, None] = None) -> RET:
    if args is None: args = []
    if len(args) > 0 and is_help(args):
        ret_obj = SendMsg(wb, 'token', ['-h'], opts = 'nokeys')
        return ret_obj._replace(out = ret_obj.out.replace('usage: token', 'INFO: token is automatically created, use this for token customization\nusage: token-init'))
    wb = token_regen(wb, args)
    tokencert, __ = get_token_names()
    return CertInfo(tokencert)


def DO_edit(wb, args: Union[list, None] = None, editor: str = '') -> RET:
    """Edit a grid lfn; download a temporary, edit with the specified editor and upload the new file"""
    if not args or args is None: args = ['-h']
    if is_help(args):
        msg = """Command format: edit lfn\nAfter editor termination the file will be uploaded if md5 differs
-datebck : the backup filename will be date based
N.B. EDITOR env var must be set or fallback will be mcedit (not checking if exists)"""
        return RET(0, msg)
    if not editor:
        editor = os.getenv('EDITOR')
        if not editor:
            print_out('EDITOR env variable not set, we will fallback to mcedit (no check if exists)')
            editor = 'mcedit -u'
    versioned_backup = False
    if get_arg(args, '-datebck'): versioned_backup = True
    lfn = expand_path_grid(args[-1])  # assume that the last argument is the lfn
    # check for valid (single) specifications delimiter
    count_tokens = collections.Counter(lfn)
    if count_tokens[','] + count_tokens['@'] > 1:
        msg = f"At most one of >,< or >@< tokens used for copy specification can be present in the argument. The offender is: {''.join(count_tokens)}"
        return RET(64, '', msg)  # EX_USAGE /* command line usage error */

    specs = specs_split.split(lfn, maxsplit = 1)  # NO comma allowed in grid names (hopefully)
    lfn = specs.pop(0)  # first item is the file path, let's remove it; it remains disk specifications
    tmp = download_tmp(wb, lfn, overwrite = False, verbose = False)
    if tmp and os.path.isfile(tmp):
        md5_begin = md5(tmp)
        ret_obj = runShellCMD(f'{editor} {tmp}', captureout = False)
        if ret_obj.exitcode != 0: return ret_obj  # noqa: R504
        md5_end = md5(tmp)
        if md5_begin != md5_end:
            uploaded_file = upload_tmp(wb, tmp, ','.join(specs), dated_backup = versioned_backup)
            os.remove(tmp)  # clean up the temporary file not matter if the upload was succesful or not
            return RET(0, f'Uploaded {uploaded_file}') if uploaded_file else RET(1, '', f'Error uploading {uploaded_file}')
        return RET(0)
    return RET(1, '', f'Error downloading {lfn}, editing could not be done.')


def DO_mcedit(wb, args: Union[list, None] = None) -> RET: return DO_edit(wb, args, editor = 'mcedit')


def DO_vi(wb, args: Union[list, None] = None) -> RET: return DO_edit(wb, args, editor = 'vi')


def DO_vim(wb, args: Union[list, None] = None) -> RET: return DO_edit(wb, args, editor = 'vim')


def DO_nano(wb, args: Union[list, None] = None) -> RET: return DO_edit(wb, args, editor = 'nano')


def DO_run(wb, args: Union[list, None] = None, external: bool = False) -> RET:
    """run shell_command lfn|alien: tagged lfns :: download lfn(s) as a temporary file and run shell command on the lfn(s)"""
    if args is None: args = []
    if not args: return RET(1, '', 'No shell command specified')
    if is_help(args) or len(args) == 1:
        msg_last = ('Command format: shell_command arguments lfn\n'
                    'N.B.!! the lfn must be the last element of the command!!\n'
                    'N.B.! The output and error streams will be captured and printed at the end of execution!\n'
                    'for working within application use <edit> or -noout argument\n'
                    'additiona arguments recognized independent of the shell command:\n'
                    '-force : will re-download the lfn even if already present\n'
                    '-noout : will not capture output, the actual application can be used')

        if external:
            ret_obj = runShellCMD(f'{args[0]} -h', captureout = True, do_shell = True)
            return ret_obj._replace(out = f'{ret_obj.out}\n{msg_last}')
        msg = ('Command format: run shell_command arguments lfn\n'
               'the lfn must be the last element of the command\n'
               'N.B.! The output and error streams will be captured and printed at the end of execution!\n'
               'for working within application use <edit>\n'
               'additiona arguments recognized independent of the shell command:\n'
               '-force : will re-download the lfn even if already present\n'
               '-noout : will not capture output, the actual application can be used')
        return RET(0, msg)

    overwrite = get_arg(args, '-force')
    capture_out = get_arg(args, '-noout')

    list_of_lfns = [arg for arg in args if 'alien:' in arg]
    if not list_of_lfns: list_of_lfns = [args.pop(-1)]

    tmp_list = [download_tmp(wb, lfn, overwrite, verbose = True) for lfn in list_of_lfns]  # list of temporary downloads
    new_args = [arg for arg in args if arg not in list_of_lfns]  # command arguments without the files
    args = list(new_args)
    cmd = " ".join(args)
    files = " ".join(tmp_list)
    if tmp_list and all(os.path.isfile(tmp) for tmp in tmp_list):
        return runShellCMD(f'{cmd} {files}', capture_out, do_shell = True)
    return RET(1, '', f'There was an error downloading the following files:\n{chr(10).join(list_of_lfns)}')


def DO_exec(wb, args: Union[list, None] = None) -> RET:
    """exec lfn :: download lfn as a temporary file and executed in the shell"""
    if args is None: args = []
    if not args or is_help(args):
        msg = ('Command format: exec lfn list_of_arguments\n'
               'N.B.! The output and error streams will be captured and printed at the end of execution!\n'
               'for working within application use <edit>')
        return RET(0, msg)

    overwrite = get_arg(args, '-force')
    capture_out = get_arg(args, '-noout')

    lfn = args.pop(0)  # the script to be executed
    opt_args = " ".join(args)
    tmp = download_tmp(wb, lfn, overwrite)
    if tmp and os.path.isfile(tmp):
        os.chmod(tmp, 0o700)
        return runShellCMD(f'{tmp} {opt_args}' if opt_args else tmp, capture_out)
    return RET(1, '', f'There was an error downloading script: {lfn}')


def DO_syscmd(wb, cmd: str = '', args: Union[None, list, str] = None) -> RET:
    """run system command with all the arguments but all alien: specifications are downloaded to temporaries"""
    global AlienSessionInfo
    if args is None: args = []
    if isinstance(args, str): args = args.split()
    if not cmd: return RET(1, '', 'No system command specified!')
    new_arg_list = [download_tmp(wb, arg) if arg.startswith('alien:') else arg for arg in args]
    new_arg_list.index(0, cmd)
    return runShellCMD(' '.join(new_arg_list), captureout = True, do_shell = True)


def DO_find2(wb, args: Union[None, list, str] = None) -> RET:
    if args is None: args = []
    if isinstance(args, str):
        args = args.split() if args else []
    if is_help(args):
        msg_client = (f'''Client-side implementation of find, it contain the following helpers.
Command formant: find2 <options> <directory>
N.B. directory to be search for must be last element of command
-glob <globbing pattern> : this is the usual AliEn globbing format; {PrintColor(COLORS.BIGreen)}N.B. this is NOT a REGEX!!!{PrintColor(COLORS.ColorReset)} defaults to all "*"
-select <pattern> : select only these files to be copied; {PrintColor(COLORS.BIGreen)}N.B. this is a REGEX applied to full path!!!{PrintColor(COLORS.ColorReset)}
-name <pattern> : select only these files to be copied; {PrintColor(COLORS.BIGreen)}N.B. this is a REGEX applied to a directory or file name!!!{PrintColor(COLORS.ColorReset)}
-name <verb>_string : where verb = begin|contain|ends|ext and string is the text selection criteria.
verbs are aditive : -name begin_myf_contain_run1_ends_bla_ext_root
{PrintColor(COLORS.BIRed)}N.B. the text to be filtered cannont have underline <_> within!!!{PrintColor(COLORS.ColorReset)}
The server options:''')
        srv_answ = get_help_srv(wb, 'find')
        msg_srv = srv_answ.out
        return RET(0, f'{msg_client}\n{msg_srv}')

    # clean up the options
    get_arg(args, '-v')
    get_arg(args, '-a')
    get_arg(args, '-s')
    get_arg(args, '-f')
    get_arg(args, '-w')
    get_arg(args, '-wh')
    get_arg(args, '-d')

    search_dir = args.pop()
    use_regex = False
    filtering_enabled = False

    pattern = None
    pattern_arg = get_arg_value(args, '-glob')
    if '*' in search_dir:  # we have globbing in path
        search_dir, pattern = extract_glob_pattern(search_dir)
        if not search_dir: search_dir = './'

    is_default_glob = False
    if not (pattern or pattern_arg):
        is_default_glob = True
        pattern = '*'  # default glob pattern
    if not pattern: pattern = pattern_arg  # if both present use pattern, otherwise pattern_arg
    filtering_enabled = not is_default_glob  # signal the filtering enabled only if explicit glob request was made

    search_dir = expand_path_grid(search_dir)

    pattern_regex = None
    select_arg = get_arg_value(args, '-select')
    if select_arg:
        if filtering_enabled:
            msg = 'Only one rule of selection can be used, either -select (full path match), -name (match on file name), -glob (globbing) or path globbing'
            return RET(22, '', msg)  # EINVAL /* Invalid argument */
        pattern_regex = select_arg
        use_regex = True
        filtering_enabled = True

    name_arg = get_arg_value(args, '-name')
    if name_arg:
        if filtering_enabled:
            msg = 'Only one rule of selection can be used, either -select (full path match), -name (match on file name), -glob (globbing) or path globbing'
            return RET(22, '', msg)  # EINVAL /* Invalid argument */
        use_regex = True
        filtering_enabled = True
        pattern_regex = name2regex(name_arg)
        if use_regex and not pattern_regex:
            msg = ("-name :: No selection verbs were recognized!"
                   "usage format is -name <attribute>_<string> where attribute is one of: begin, contain, ends, ext"
                   f"The invalid pattern was: {pattern_regex}")
            return RET(22, '', msg)  # EINVAL /* Invalid argument */

    if use_regex: pattern = pattern_regex  # -select, -name usage overwrites glob usage
    return list_files_grid(wb, search_dir, pattern, use_regex, args)


def DO_quota(wb, args: Union[None, list] = None) -> RET:
    """quota : put togheter both job and file quota"""
    if not args: args = []
    if is_help(args):
        msg = ("Client-side implementation that make use of server\'s jquota and fquota (hidden by this implementation)\n"
               'Command format: quota [user]\n'
               'if [user] is not provided, it will be assumed the current user')
        return RET(0, msg)

    user = AlienSessionInfo['user']
    if len(args) > 0:
        if args[0] != "set":  # we asume that if 'set' is not used then the argument is a username
            user = args[0]
        else:
            msg = '>set< functionality not implemented yet'
            return RET(0, msg)

    jquota_out = SendMsg(wb, f'jquota -nomsg list {user}')
    jquota_dict = jquota_out.ansdict
    fquota_out = SendMsg(wb, f'fquota -nomsg list {user}')
    fquota_dict = fquota_out.ansdict

    username = jquota_dict['results'][0]["username"]

    running_time = float(jquota_dict['results'][0]["totalRunningTimeLast24h"]) / 3600
    running_time_max = float(jquota_dict['results'][0]["maxTotalRunningTime"]) / 3600
    running_time_perc = (running_time / running_time_max) * 100

    cpucost = float(jquota_dict['results'][0]["totalCpuCostLast24h"]) / 3600
    cpucost_max = float(jquota_dict['results'][0]["maxTotalCpuCost"]) / 3600
    cpucost_perc = (cpucost / cpucost_max) * 100

    unfinishedjobs_max = int(jquota_dict['results'][0]["maxUnfinishedJobs"])
    waiting = int(jquota_dict['results'][0]["waiting"])
    running = int(jquota_dict['results'][0]["running"])
    unfinishedjobs_perc = ((waiting + running) / unfinishedjobs_max) * 100

    pjobs_nominal = int(jquota_dict['results'][0]["nominalparallelJobs"])
    pjobs_max = int(jquota_dict['results'][0]["maxparallelJobs"])

    size = float(fquota_dict['results'][0]["totalSize"])
    size_MiB = size / (1024 * 1024)
    size_max = float(fquota_dict['results'][0]["maxTotalSize"])
    size_max_MiB = size_max / (1024 * 1024)
    size_perc = (size / size_max) * 100

    files = float(fquota_dict['results'][0]["nbFiles"])
    files_max = float(fquota_dict['results'][0]["maxNbFiles"])
    files_perc = (files / files_max) * 100

    msg = (f"""Quota report for user : {username}
Unfinished jobs(R + W / Max):\t\t{running} + {waiting} / {unfinishedjobs_max} --> {unfinishedjobs_perc:.2f}% used
Running time (last 24h) used/max:\t{running_time:.2f}/{running_time_max:.2f}(h) --> {running_time_perc:.2f}% used
CPU Cost (last 24h) used/max:\t\t{cpucost:.2f}/{cpucost_max:.2f}(h) --> {cpucost_perc:.2f}% used
ParallelJobs (nominal/max) :\t{pjobs_nominal}/{pjobs_max}
Storage size :\t\t\t{size_MiB:.2f}/{size_max_MiB:.2f} MiB --> {size_perc:.2f}%
Number of files :\t\t{files}/{files_max} --> {files_perc:.2f}%""")
    return RET(0, msg)




def DO_user(wb, args: Union[list, None] = None) -> RET:
    global AlienSessionInfo
    if args is None: args = []
    ret_obj = SendMsg(wb, 'user', args)
    if ret_obj.exitcode == 0 and 'homedir' in ret_obj.ansdict['results'][0]: AlienSessionInfo['alienHome'] = ret_obj.ansdict['results'][0]['homedir']
    return ret_obj


def DO_ping(wb, args: Union[list, None] = None) -> RET:
    """Command implementation for ping functionality"""
    if args is None: args = []
    if is_help(args): return RET(0, "ping <count>\nwhere count is integer")

    if len(args) > 0 and args[0].isdigit():
        count = int(args[0])
    elif not args:
        count = int(3)
    else:
        return RET(1, '', 'Unrecognized argument, it should be int type')

    results = []
    for _i in range(count):
        p = wb_ping(wb)
        results.append(p)

    rtt_min = min(results)
    rtt_max = max(results)
    rtt_avg = statistics.mean(results)
    rtt_stddev = statistics.stdev(results) if len(results) > 1 else 0.0
    endpoint = wb.remote_address[0]
    msg = (f'Websocket ping/pong(s) : {count} time(s) to {endpoint}\nrtt min/avg/max/mdev (ms) = {rtt_min:.3f}/{rtt_avg:.3f}/{rtt_max:.3f}/{rtt_stddev:.3f}')
    return RET(0, msg)




















