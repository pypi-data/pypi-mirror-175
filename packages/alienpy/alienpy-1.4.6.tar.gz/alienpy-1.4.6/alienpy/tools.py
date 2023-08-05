import re
import json
import time
import logging
from typing import Union

from data import *
from re_patt import *

ignore_comments_re = re.compile('^\\s*(#|;|//)+', re.MULTILINE)  # identifiy a range of comments
emptyline_re = re.compile('^\\s*$', re.MULTILINE)  # whitespace line

def print_out(msg: str, toLog: bool = False):
    if toLog:
        logging.log(90, msg)
    else:
        print(msg, flush = True)


def print_err(msg: str, toLog: bool = False):
    if toLog:
        logging.log(95, msg)
    else:
        print(msg, file = sys.stderr, flush = True)


def PrintDict(in_arg: Union[str, dict, list], compact: bool = False):
    """Print a dictionary in a nice format"""
    if isinstance(in_arg, str):
        try:
            in_arg = json.loads(in_arg)
        except Exception as e:
            print_err(f'PrintDict:: Could not load argument as json!\n{e!r}')
    if compact:
        print_out(json.dumps(in_arg, sort_keys = False, indent = None, separators = (',', ':')))
    else:
        print_out(json.dumps(in_arg, sort_keys = False, indent = 2))


def CreateJsonCommand(cmdline: Union[str, dict], args: Union[None, list] = None, opts: str = '', get_dict: bool = False) -> Union[str, dict]:
    """Return a json with command and argument list"""
    if args is None: args = []
    if isinstance(cmdline, dict):
        out_dict = cmdline.copy()
        if 'showmsg' in opts: opts = opts.replace('nomsg', '')
        if 'showkeys' in opts: opts = opts.replace('nokeys', '')
        if 'nomsg' in opts: out_dict["options"].insert(0, '-nomsg')
        if 'nokeys' in opts: out_dict["options"].insert(0, '-nokeys')
        return out_dict if get_dict else json.dumps(out_dict)

    if not args:
        args = shlex.split(cmdline)
        cmd = args.pop(0) if args else ''
    else:
        cmd = cmdline
    if 'nomsg' in opts: args.insert(0, '-nomsg')
    if 'nokeys' in opts: args.insert(0, '-nokeys')
    jsoncmd = {"command": cmd, "options": args}
    return jsoncmd if get_dict else json.dumps(jsoncmd)


def GetMeta(result: dict, meta: str = '') -> list:
    """Extract from input and return a list of 2nd arg selectable of cwd user error exitcode"""
    output = []
    if not result: return output
    if isinstance(result, dict) and 'metadata' in result:  # these works only for AliEn responses
        meta_opts_list = meta.split() if meta else []
        if 'cwd' in meta_opts_list or 'all' in meta_opts_list: output.append(result["metadata"]["currentdir"])
        if 'user' in meta_opts_list or 'all' in meta_opts_list: output.append(result["metadata"]["user"])
        if 'error' in meta_opts_list or 'all' in meta_opts_list: output.append(result["metadata"]["error"])
        if 'exitcode' in meta_opts_list or 'all' in meta_opts_list: output.append(result["metadata"]["exitcode"])
    return output


def PrintColor(color: str) -> str:
    """Disable color if the terminal does not have capability"""
    return color if _HAS_COLOR else ''


def cursor_vertical(lines: int = 0):
    """Move the cursor up/down N lines"""
    if lines == 0: return
    out_char = '\x1b[1A'  # UP
    if lines < 0:
        out_char = '\x1b[1B'  # DOWN
        lines = abs(lines)
    sys.stdout.write(out_char * lines)
    sys.stdout.flush()


def cursor_horizontal(lines: int = 0):
    """Move the cursor left/right N lines"""
    if lines == 0: return
    out_char = '\x1b[1C'  # RIGHT
    if lines < 0:
        out_char = '\x1b[1D'  # LEFT
        lines = abs(lines)
    sys.stdout.write(out_char * lines)
    sys.stdout.flush()



def exit_message(code: int = 0, msg = ''):
    """Exit with msg and with specied code"""
    print_out(msg if msg else 'Exit')
    sys.exit(code)


def is_guid(guid: str) -> bool:
    """Recognize a GUID format"""
    return bool(guid_regex.fullmatch(guid))  # identify if argument in an AliEn GUID


def run_function(function_name: str, *args, **kwargs):
    """Python code:: run some arbitrary function name (found in globals) with arbitrary arguments"""
    return globals()[function_name](*args, *kwargs)  # run arbitrary function


def is_float(arg: Union[str, float, None]) -> bool:
    if not arg: return False
    s = str(arg).replace('.', '', 1)
    if s[0] in ('-', '+'): return s[1:].isdigit()
    return s.isdigit()


def is_int(arg: Union[str, int, float, None]) -> bool:
    if not arg: return False
    s = str(arg)
    if s[0] in ('-', '+'): return s[1:].isdigit()
    return s.isdigit()


def time_unix2simple(time_arg: Union[str, int, None]) -> str:
    if not time_arg: return ''
    return datetime.datetime.fromtimestamp(time_arg).replace(microsecond=0).isoformat().replace('T', ' ')


def time_str2unixmili(time_arg: Union[str, int, None]) -> int:  # noqa: FQ004
    if not time_arg:
        return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
    time_arg = str(time_arg)

    if time_arg.isdigit() or is_float(time_arg):
        if is_float(time_arg) and len(time_arg) == 10:
            return int(float(time_arg) * 1000)
        if time_arg.isdigit() and len(time_arg) == 13:
            return int(time_arg)
        return int(-1)

    # asume that this is a strptime arguments in the form of: time_str, format_str
    try:
        time_obj = ast.literal_eval(f'datetime.datetime.strptime({time_arg})')
        return int((time_obj - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
    except Exception:
        return int(-1)
def now_str() -> str: return str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))


def deltat_ms(t0: Union[str, float, None] = None) -> str:
    """Return delta t in ms from a time start; if no argment it return a timestamp in ms"""
    now = datetime.datetime.now().timestamp()
    return f"{(now - float(t0)) * 1000:.3f}" if t0 else f"{now * 1000:.3f}"


def deltat_us(t0: Union[str, float, None] = None) -> str:
    """Return delta t in ms from a time start; if no argment it return a timestamp in ms"""
    now = datetime.datetime.now().timestamp()
    return f"{(now - float(t0)) * 1000000:.3f}" if t0 else f"{now * 1000000:.3f}"


def deltat_ms_perf(t0: Union[str, float, None] = None) -> str:
    """Return delta t in ms from a time start; if no argment it return a timestamp in ms"""
    if not t0: return ""
    return f"{(time.perf_counter() - float(t0)) * 1000:.3f}"


def deltat_us_perf(t0: Union[str, float, None] = None) -> str:
    """Return delta t in ms from a time start; if no argment it return a timestamp in ms"""
    if not t0: return ""
    return f"{(time.perf_counter() - float(t0)) * 1000000:.3f}"


def is_help(args: Union[str, list]) -> bool:
    if not args: return False
    if isinstance(args, str): args = args.split()
    help_opts = ('-h', '--h', '-help', '--help')
    return any(opt in args for opt in help_opts)


def unquote_str(arg):
    if type(arg) is str: return ast.literal_eval(arg)
    return arg


def read_conf_file(conf_file: str) -> dict:
    """Convert a configuration file with key = value format to a dict"""
    if not conf_file or not os.path.isfile(conf_file): return {}
    DICT_INFO = {}
    try:
        with open(conf_file, encoding="ascii", errors="replace") as rel_file:
            for line in rel_file:
                line = line.partition('#')[0].rstrip()
                name, var = line.partition("=")[::2]
                var = re.sub(r"^\"", '', str(var.strip()))
                var = re.sub(r"\"$", '', var)
                DICT_INFO[name.strip()] = var
    except Exception:
        pass
    return DICT_INFO


def file2list(input_file: str) -> list:
    """Parse a file and return a list of elements"""
    if not input_file or not os.path.isfile(input_file): return []
    file_list = []
    with open(input_file, encoding="ascii", errors="replace") as filecontent:
        for line in filecontent:
            if not line or ignore_comments_re.search(line) or emptyline_re.match(line): continue
            file_list.extend(line.strip().split())
    return file_list


def fileline2list(input_file: str) -> list:
    """Parse a file and return a list of file lines"""
    if not input_file or not os.path.isfile(input_file): return []
    file_list = []
    with open(input_file, encoding="ascii", errors="replace") as filecontent:
        for line in filecontent:
            if not line or ignore_comments_re.search(line) or emptyline_re.match(line): continue
            file_list.extend([line.strip()])
    return file_list


def os_release() -> dict:
    return read_conf_file('/etc/os-release')


def get_lfn_key(lfn_obj: dict) -> str:
    """get either lfn key or file key from a file description"""
    if not lfn_obj or not isinstance(lfn_obj, dict): return ''
    if "lfn" in lfn_obj: return lfn_obj["lfn"]
    if "file" in lfn_obj: return lfn_obj["file"]
    return ''



def pid_uid(pid: int) -> int:
    """Return username of UID of process pid"""
    uid = int(-1)
    try:
        with open(f'/proc/{pid}/status', encoding="ascii", errors="replace") as proc_status:
            for line in proc_status:
                # Uid, Gid: Real, effective, saved set, and filesystem UIDs(GIDs)
                if line.startswith('Uid:'): uid = int((line.split()[1]))
    except Exception:
        pass
    return uid  # noqa: R504


def is_my_pid(pid: int) -> bool: return bool(pid_uid(int(pid)) == os.getuid())


def writePidFile(filename: str):
    try:
        with open(filename, 'w', encoding="ascii", errors="replace") as f: f.write(str(os.getpid()))
    except Exception:
        logging.exception('Error writing the pid file: %s', filename)


def GetSessionFilename() -> str: return os.path.join(os.path.expanduser("~"), ".alienpy_session")


def unixtime2local(timestamp: Union[str, int], decimals: bool = True) -> str:
    """Convert unix time to a nice custom format"""
    timestr = str(timestamp)
    if len(timestr) < 10: return ''
    micros = None
    millis = None
    time_decimals = ''
    if len(timestr) > 10:
        time_decimals = timestr[10:]
        if len(time_decimals) <= 3:
            time_decimals = time_decimals.ljust(3, '0')
            millis = datetime.timedelta(milliseconds=int(time_decimals))
        else:
            time_decimals = time_decimals.ljust(6, '0')
            micros = datetime.timedelta(microseconds=int(time_decimals))

    unixtime = timestr[:10]
    utc_time = datetime.datetime.fromtimestamp(int(unixtime), datetime.timezone.utc)
    local_time = utc_time.astimezone()
    if decimals and millis:
        return f'{(local_time + millis).strftime("%Y-%m-%d %H:%M:%S")}.{time_decimals}{local_time.strftime("%z")}'
    if decimals and micros:
        return (local_time + micros).strftime("%Y-%m-%d %H:%M:%S.%f%z")  # (%Z)"))
    return local_time.strftime("%Y-%m-%d %H:%M:%S%z")  # (%Z)"))


def convert_time(str_line: str) -> str:
    """Convert the first 10 digit unix time like string from str argument to a nice time"""
    timestamp = re.findall(r"^(\d{10}) \[.*", str_line)
    if timestamp:
        nice_timestamp = f"{PrintColor(COLORS.BIGreen)}{unixtime2local(timestamp[0])}{PrintColor(COLORS.ColorReset)}"
        return str_line.replace(str(timestamp[0]), nice_timestamp)
    return ''


def list_remove_item(target_list: list, item_list):
    target_list[:] = [el for el in target_list if el != item_list]


def get_arg(target: list, item) -> bool:
    """Remove inplace all instances of item from list and return True if found"""
    len_begin = len(target)
    list_remove_item(target, item)
    len_end = len(target)
    return len_begin != len_end


def get_arg_value(target: list, item):
    """Remove inplace all instances of item and item+1 from list and return item+1"""
    val = None
    for x in target:
        if x == item:
            val = target.pop(target.index(x) + 1)
            target.pop(target.index(x))
    return val  # noqa: R504


def get_arg_2values(target: list, item):
    """Remove inplace all instances of item, item+1 and item+2 from list and return item+1, item+2"""
    val1 = val2 = None
    for x in target:
        if x == item:
            val2 = target.pop(target.index(x) + 2)
            val1 = target.pop(target.index(x) + 1)
            target.pop(target.index(x))
    return val1, val2


def uid2name(uid: Union[str, int]) -> str:
    """Convert numeric UID to username"""
    return pwd.getpwuid(int(uid)).pw_name


def gid2name(gid: Union[str, int]) -> str:
    """Convert numeric GUI to group name"""
    try:
        group_info = grp.getgrgid(int(gid))
        return group_info.gr_name
    except Exception:
        return str(gid)


def GetHumanReadable(size, precision = 2):
    """Convert bytes to higher units"""
    suffixes = ['B', 'KiB', 'MiB', 'GiB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 5:
        suffixIndex += 1  # increment the index of the suffix
        size = size / 1024.0  # apply the division
    return f'{size:.{precision}f} {suffixes[suffixIndex]}'


def valid_regex(regex_str: str) -> Union[None, REGEX_PATTERN_TYPE]:
    """Validate a regex string and return a re.Pattern if valid"""
    regex = None
    try:
        regex = re.compile(regex_str.encode('unicode-escape').decode())  # try to no hit https://docs.python.org/3.6/howto/regex.html#the-backslash-plague
    except re.error:
        logging.error('regex validation failed:: %s', regex_str)
    return regex  # noqa: R504


def file2xml_el(filepath: str) -> ALIEN_COLLECTION_EL:
    """Get a file and return an XML element structure"""
    if not filepath or not os.path.isfile(filepath): return ALIEN_COLLECTION_EL()
    p = Path(filepath).expanduser().resolve(strict = True)
    if p.is_dir(): return ALIEN_COLLECTION_EL()
    p_stat = p.stat()
    turl = f'file://{p.as_posix()}'
    return ALIEN_COLLECTION_EL(
        name = p.name, aclId = "", broken = "0", ctime = time_unix2simple(p_stat.st_ctime),
        dir = '', entryId = '', expiretime = '', gowner = p.group(), guid = '', guidtime = '', jobid = '', lfn = turl,
        md5 = md5(p.as_posix()), owner = p.owner(), perm = str(oct(p_stat.st_mode))[5:], replicated = "0",
        size = str(p_stat.st_size), turl = turl, type = 'f')


def mk_xml_local(filepath_list: list):
    xml_root = ET.Element('alien')
    collection = ET.SubElement(xml_root, 'collection', attrib={'name': 'tempCollection'})
    for idx, item in enumerate(filepath_list, start = 1):
        e = ET.SubElement(collection, 'event', attrib={'name': str(idx)})
        f = ET.SubElement(e, 'file', attrib = file2xml_el(lfn_prefix_re.sub('', item))._asdict())  # noqa:F841
    oxml = ET.tostring(xml_root, encoding = 'ascii')
    dom = MD.parseString(oxml)
    return dom.toprettyxml()


def runShellCMD(INPUT: str = '', captureout: bool = True, do_shell: bool = False, timeout: Union[str, int, None] = None) -> RET:
    """Run shell command in subprocess; if exists, print stdout and stderr"""
    if not INPUT: return RET(1, '', 'No command to be run provided')
    sh_cmd = re.sub(r'^!', '', INPUT)
    args = sh_cmd if do_shell else shlex.split(sh_cmd)
    capture_args = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE} if captureout else {}
    status = exitcode = except_msg = None
    msg_out = msg_err = ''
    try:
        status = subprocess.run(args, encoding = 'utf-8', errors = 'replace', shell = do_shell, **capture_args)  # pylint: disable=subprocess-run-check
    except subprocess.TimeoutExpired:
        print_err(f"Expired timeout: {timeout} for: {sh_cmd}")
        exitcode = int(62)
    except FileNotFoundError:
        print_err(f"Command not found: {sh_cmd}")
        exitcode = int(2)
    except Exception:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        except_msg = f'Exception:: {ex_type} -> {ex_value}\n{ex_traceback}\n'
        exitcode = int(1)

    if status:
        if status.stdout: msg_out = status.stdout.strip()
        if status.stderr: msg_err = status.stderr.strip()
        exitcode = status.returncode
    if except_msg: msg_err = f'{except_msg}\n{msg_err}'
    return RET(exitcode, msg_out, msg_err)



def check_ip_port(socket_object: tuple) -> bool:
    """Check connectivity to an address, port; adress should be the tuple given by getaddrinfo"""
    if not socket_object: return False
    is_open = False
    # socket_object = (family, type, proto, canonname, sockaddr)
    with socket.socket(socket_object[0], socket_object[1], socket_object[2]) as s:  # Create a TCP socket
        s.settimeout(2)  # timeout 2s
        try:
            s.connect(socket_object[4])
            is_open = True
        except Exception:
            pass
    return is_open  # noqa: R504


def check_port(address: str, port: Union[str, int]) -> list:
    """Check TCP connection to fqdn:port"""
    ip_list = socket.getaddrinfo(address, int(port), proto = socket.IPPROTO_TCP)
    return [(*sock_obj[-1], check_ip_port(sock_obj)) for sock_obj in ip_list]


def isReachable(address: str = 'alice-jcentral.cern.ch', port: Union[str, int] = 8097) -> bool:
    result_list = check_port(address, port)
    return any(ip[-1] for ip in result_list)


if __name__ == '__main__':
    print('This file should not be executed!', file = sys.stderr, flush = True)
    sys.exit(95)

