import sys
import re
from pathlib import Path

from data import *
from re_patt import *




def expand_path_local(path_arg: str, strict: bool = False) -> str:
    """Given a string representing a local file, return a full path after interpretation of HOME location, current directory, . and .. and making sure there are only single /"""
    if not path_arg: return ''
    exp_path = None
    path_arg = lfn_prefix_re.sub('', path_arg)  # lets remove any prefixes
    try:
        exp_path = Path(path_arg).expanduser().resolve(strict).as_posix()
    except Exception:
        return ''
    if (len(exp_path) > 1 and path_arg.endswith('/')) or os.path.isdir(exp_path): exp_path = f'{exp_path}/'
    return exp_path  # noqa: R504


def check_path_perm(filepath: str, mode) -> bool:
    """Resolve a file/path and check if mode is valid"""
    filepath = expand_path_local(filepath, True)
    if not filepath: return False
    if not mode: mode = os.F_OK
    have_access = False
    try:
        have_access = os.access(filepath, mode, follow_symlinks = True)
    except Exception:
        pass
    return have_access  # noqa: R504


def path_readable(filepath: str = '') -> bool:
    """Resolve a file/path and check if it is readable"""
    return check_path_perm(filepath, os.R_OK)


def path_writable(filepath: str = '') -> bool:
    """Resolve a file/path and check if it is writable"""
    return check_path_perm(filepath, os.W_OK)


def path_writable_any(filepath: str = '') -> bool:
    """Return true if any path in hierarchy is writable (starting with the longest path)"""
    filepath = expand_path_local(filepath)  # do not use strict as the destination directory could not yet exists
    if not filepath: return False
    paths_list = [p.as_posix() for p in Path(filepath).parents]
    if Path(filepath).is_dir(): paths_list.insert(0, filepath)
    return any(path_writable(p) for p in paths_list)


def path_local_stat(path: str, do_md5: bool = False) -> STAT_FILEPATH:
    """Get full information on a local path"""
    norm_path = expand_path_local(path)
    if not os.path.exists(norm_path): return STAT_FILEPATH(norm_path)
    filetype = 'd' if os.path.isdir(norm_path) else 'f'
    statinfo = os.stat(norm_path)
    perm = oct(statinfo.st_mode)[-3:]
    uid = uid2name(statinfo.st_uid)
    gid = gid2name(statinfo.st_gid)
    ctime = str(statinfo.st_ctime)
    mtime = str(statinfo.st_mtime)
    guid = ''
    size = str(statinfo.st_size)
    md5hash = ''
    if do_md5 and filetype == 'f': md5hash = md5(norm_path)
    return STAT_FILEPATH(norm_path, filetype, perm, uid, gid, ctime, mtime, guid, size, md5hash)


def pathtype_local(path: str) -> str:
    """Query if a local path is a file or directory, return f, d or empty"""
    if not path: return ''
    p = Path(path)
    if p.is_dir(): return str('d')
    if p.is_file(): return str('f')
    return ''


def md5(filename: str) -> str:
    """Compute the md5 digest of the specified file"""
    import hashlib
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()


def fileIsValid(filename: str, size: Union[str, int], reported_md5: str, shallow_check: bool = False) -> RET:
    """Check if the file path is consistent with the size and md5 argument. N.B.! the local file will be deleted with size,md5 not match"""
    global AlienSessionInfo
    if os.path.isfile(filename):  # first check
        if int(os.stat(filename).st_size) != int(size):
            os.remove(filename)
            return RET(9, '', f'{filename} : Removed (invalid size)')
        if shallow_check:
            return RET(0, f'{filename} --> TARGET VALID (size match)')
        if md5(filename) != reported_md5:
            os.remove(filename)
            return RET(9, '', f'{filename} : Removed (invalid md5)')
        return RET(0, f'{filename} --> TARGET VALID (md5 match)')
    return RET(2, '', f'{filename} : No such file')  # ENOENT



def file_set_atime(path: str):
    """Set atime of file to now"""
    if not os.path.isfile(path): return
    file_stat = os.stat(path)
    os.utime(path, (datetime.datetime.now().timestamp(), file_stat.st_mtime))



def file2file_dict(fn: str) -> dict:
    """Take a string as path and retur a dict with file propreties"""
    try:
        file_path = Path(fn)
    except Exception:
        return {}
    try:
        file_name = file_path.expanduser().resolve(strict = True)
    except Exception:
        return {}
    if file_name.is_dir(): return {}

    file_dict = {"file": file_name.as_posix()}
    file_dict["lfn"] = file_name.as_posix()
    file_dict["size"] = str(file_name.stat().st_size)
    file_dict["mtime"] = str(int(file_name.stat().st_mtime * 1000))
    file_dict["md5"] = md5(file_name.as_posix())
    file_dict["owner"] = pwd.getpwuid(file_name.stat().st_uid).pw_name
    file_dict["gowner"] = gid2name(file_name.stat().st_gid)
    return file_dict




def filter_file_prop(f_obj: dict, base_dir: str, find_opts: Union[str, list, None], compiled_regex = None) -> bool:
    """Return True if an file dict object pass the conditions in find_opts"""
    if not f_obj or not base_dir: return False
    if not find_opts: return True
    opts = find_opts.split() if isinstance(find_opts, str) else find_opts.copy()
    lfn = get_lfn_key(f_obj)
    if not base_dir.endswith('/'): base_dir = f'{base_dir}/'
    relative_lfn = lfn.replace(base_dir, '')  # it will have N directories depth + 1 file components

    # string/pattern exclusion
    exclude_string = get_arg_value(opts, '-exclude')
    if exclude_string and exclude_string in relative_lfn: return False  # this is filtering out the string from relative lfn

    exclude_regex = get_arg_value(opts, '-exclude_re')
    if exclude_regex and compiled_regex and compiled_regex.match(relative_lfn): return False

    min_size = get_arg_value(opts, '-minsize')
    if min_size:
        if not min_size.isdigit() or min_size.startswith("-"):
            print_err(f'filter_file_prop::minsize arg not recognized: {" ".join(opts)}')
            return False
        if int(f_obj["size"]) < abs(int(min_size)): return False

    max_size = get_arg_value(opts, '-maxsize')
    if max_size:
        if not max_size.isdigit() or max_size.startswith("-"):
            print_err(f'filter_file_prop::maxsize arg not recognized: {" ".join(opts)}')
            return False
        if int(f_obj["size"]) > abs(int(max_size)): return False

    jobid = get_arg_value(opts, '-jobid')
    if jobid:
        if not jobid.isdigit() or jobid.startswith("-"):
            print_err(f'filter_file_prop::Missing argument in list:: {" ".join(opts)}')
            return False

        if "jobid" not in f_obj:
            print_err('filter_file_prop::jobid - could not find jobid information in file dictionary, selection failed!')
            return False
        if f_obj["jobid"] != jobid: return False

    user = get_arg_value(opts, '-user')
    if user:
        if not user.isalpha() or user.startswith("-"):
            print_err(f'filter_file_prop::Missing argument in list:: {" ".join(opts)}')
            return False
        if f_obj["owner"] != user: return False

    group = get_arg_value(opts, '-group')
    if group:
        if not group.isalpha() or group.startswith("-"):
            print_err(f'filter_file_prop::Missing argument in list:: {" ".join(opts)}')
            return False
        if f_obj["gowner"] != group: return False

    min_ctime = get_arg_value(opts, '-min-ctime')
    if min_ctime and min_ctime.startswith("-"):
        print_err(f'filter_file_prop::min-ctime arg not recognized: {" ".join(opts)}')
        return False

    max_ctime = get_arg_value(opts, '-max-ctime')
    if max_ctime and max_ctime.startswith("-"):
        print_err(f'filter_file_prop::max-ctime arg not recognized: {" ".join(opts)}')
        return False

    # the argument can be a string with a form like: '20.12.2016 09:38:42,76','%d.%m.%Y %H:%M:%S,%f'
    # see: https://docs.python.org/3.6/library/datetime.html#strftime-strptime-behavior
    if min_ctime or max_ctime:
        dict_time = f_obj.get("ctime", '')
        if not dict_time: dict_time = f_obj.get("mtime", '')
        if not dict_time or not dict_time.isdigit():
            print_err('filter_file_prop::min/max-ctime - could not find time information in file dictionary, selection failed!')
            return False
        if min_ctime:
            min_ctime = time_str2unixmili(min_ctime)
            if int(dict_time) < min_ctime: return False
        if max_ctime:
            max_ctime = time_str2unixmili(max_ctime)
            if int(dict_time) > max_ctime: return False

    min_depth = get_arg_value(opts, '-mindepth')
    if min_depth:
        if not min_depth.isdigit() or min_depth.startswith("-"):
            print_err(f'filter_file_prop::mindepth arg not recognized: {" ".join(opts)}')
            return False
        min_depth = abs(int(min_depth)) + 1  # add +1 for the always present file component of relative_lfn
        if len(relative_lfn.split('/')) < min_depth: return False

    max_depth = get_arg_value(opts, '-maxdepth')
    if max_depth:
        if not max_depth.isdigit() or max_depth.startswith("-"):
            print_err(f'filter_file_prop::maxdepth arg not recognized: {" ".join(opts)}')
            return False
        max_depth = abs(int(max_depth)) + 1  # add +1 for the always present file component of relative_lfn
        if len(relative_lfn.split('/')) > max_depth: return False

    return True


def list_files_local(search_dir: str, pattern: Union[None, REGEX_PATTERN_TYPE, str] = None, is_regex: bool = False, find_args: str = '') -> RET:
    """Return a list of files(local)(N.B! ONLY FILES) that match pattern found in dir"""
    if not search_dir: return RET(2, "", "No search directory specified")

    # let's process the pattern: extract it from src if is in the path globbing form
    regex = None
    is_single_file = False  # dir actually point to a file
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
    else:  # pattern is specified by argument or not specified
        if pattern is None:
            if not search_dir.endswith('/'):  # this is a single file
                is_single_file = True
            else:
                pattern = '*'  # prefer globbing as default
        elif type(pattern) is REGEX_PATTERN_TYPE:  # unlikely but supported to match signatures
            regex = pattern
            is_regex = True
        elif is_regex and isinstance(pattern, str):  # it was explictly requested that pattern is regex
            regex = valid_regex(pattern)
            if regex is None:
                msg = f'list_files_grid:: {pattern} failed to re.compile'
                logging.error(msg)
                return RET(-1, '', msg)

    directory = None  # resolve start_dir to an absolute_path
    try:
        directory = Path(search_dir).expanduser().resolve(strict = True).as_posix()
    except FileNotFoundError:
        return RET(2, '', f'{search_dir} not found')
    except RuntimeError:
        return RET(2, '', f'Loop encountered along the resolution of {search_dir}')

    filter_args_list = None
    if find_args: filter_args_list = find_args.split()  # for local files listing we have only filtering options

    file_list = None  # make a list of filepaths (that match a regex or a glob)
    if is_single_file:
        file_list = [directory]
    elif is_regex:
        file_list = [os.path.join(root, f) for (root, dirs, files) in os.walk(directory) for f in files if regex.match(os.path.join(root, f))]
    else:
        file_list = [p.expanduser().resolve(strict = True).as_posix() for p in list(Path(directory).glob(f'**/{pattern}')) if p.is_file()]

    if not file_list:
        return RET(2, '', f"No files found in :: {directory} /pattern: {pattern} /find_args: {find_args}")

    # convert the file_list to a list of file properties dictionaries
    results_list = [file2file_dict(filepath) for filepath in file_list]

    results_list_filtered = []
    # items that pass the conditions are the actual/final results
    for found_lfn_dict in results_list:  # parse results to apply filters
        if not filter_file_prop(found_lfn_dict, directory, filter_args_list, regex): continue
        # at this point all filters were passed
        results_list_filtered.append(found_lfn_dict)

    if not results_list_filtered:
        return RET(2, '', f'No files passed the filters :: {directory} /pattern: {pattern} /find_args: {find_args}')

    ansdict = {"results": results_list_filtered}
    lfn_list = [get_lfn_key(lfn_obj) for lfn_obj in results_list_filtered]
    stdout = '\n'.join(lfn_list)
    return RET(exitcode, stdout, '', ansdict)



if __name__ == '__main__':
    print('This file should not be executed!', file = sys.stderr, flush = True)
    sys.exit(95)
    
    
    