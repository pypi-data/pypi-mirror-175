

from wb_api import *

def AlienConnect(token_args: Union[None, list] = None, use_usercert: bool = False, localConnect: bool = False):
    """Create a websocket connection to AliEn services either directly to alice-jcentral.cern.ch or trough a local found jbox instance"""
    global __ALIEN_WB
    if not token_args: token_args = []
    jalien_server = os.getenv("ALIENPY_JCENTRAL", 'alice-jcentral.cern.ch')  # default value for JCENTRAL
    jalien_websocket_port = os.getenv("ALIENPY_JCENTRAL_PORT", '8097')  # websocket port
    jalien_websocket_path = '/websocket/json'
    jclient_env = f'{__TMPDIR}/jclient_token_{str(os.getuid())}'

    if __ALIEN_WB: wb_close(__ALIEN_WB, code = 1000, reason = 'Close previous websocket')

    # let's try to get a websocket
    wb = None
    if localConnect:
        wb = wb_create(localConnect = True)
    else:
        if not os.getenv("ALIENPY_JCENTRAL") and os.path.exists(jclient_env):  # If user defined ALIENPY_JCENTRAL the intent is to set and use the endpoint
            # lets check JBOX availability
            jalien_info = read_conf_file(jclient_env)
            if jalien_info and is_my_pid(jalien_info['JALIEN_PID']) and isReachable(jalien_info['JALIEN_HOST'], jalien_info['JALIEN_WSPORT']):
                jalien_server, jalien_websocket_port = jalien_info['JALIEN_HOST'], jalien_info['JALIEN_WSPORT']

        wb = wb_create_tryout(jalien_server, str(jalien_websocket_port), jalien_websocket_path, use_usercert)

        # if we stil do not have a socket, then try to fallback to jcentral if we did not had explicit endpoint and jcentral was not already tried
        if wb is None and not os.getenv("ALIENPY_JCENTRAL") and jalien_server != 'alice-jcentral.cern.ch':
            jalien_server, jalien_websocket_port = 'alice-jcentral.cern.ch', '8097'
            wb = wb_create_tryout(jalien_server, str(jalien_websocket_port), jalien_websocket_path, use_usercert)

    if wb is None:
        msg = f'Check the logfile: {_DEBUG_FILE}\nCould not get a websocket connection to {jalien_server}:{jalien_websocket_port}'
        logging.error(msg)
        print_err(msg)
        sys.exit(107)  # ENOTCONN - Transport endpoint is not connected

    __ALIEN_WB = wb  # Save the connection as a global variable
    return wb


def getSessionVars(wb):
    """Initialize the global session variables : cleaned up command list, user, home dir, current dir"""
    global AlienSessionInfo
    if AlienSessionInfo['user']: return  # user session variable is already set, then return
    if not wb: return
    # get the command list just once per session connection (a reconnection will skip this)
    ret_obj = SendMsg(wb, 'commandlist', [])
    # first executed commands, let's initialize the following (will re-read at each ProcessReceivedMessage)
    if not ret_obj.ansdict or 'results' not in ret_obj.ansdict:
        print_err("Start session:: could not get command list, let's exit.")
        sys.exit(1)
    regex = re.compile(r'.*_csd$')
    AlienSessionInfo['commandlist'] = [cmd["commandlist"] for cmd in ret_obj.ansdict["results"] if not regex.match(cmd["commandlist"])]
    AlienSessionInfo['commandlist'].remove('jquota')
    AlienSessionInfo['commandlist'].remove('fquota')

    # server commands, signature is : (wb, command, args, opts)
    for cmd in AlienSessionInfo['commandlist']: AlienSessionInfo['cmd2func_map_srv'][cmd] = SendMsg
    make_func_map_clean_server()

    # these are aliases, or directly interpreted
    AlienSessionInfo['commandlist'].append('ll')
    AlienSessionInfo['commandlist'].append('la')
    AlienSessionInfo['commandlist'].append('lla')
    AlienSessionInfo['commandlist'].extend(AlienSessionInfo['cmd2func_map_client'])  # add clien-side cmds to list
    AlienSessionInfo['commandlist'].extend(AlienSessionInfo['cmd2func_map_nowb'])  # add nowb cmds to list
    # AlienSessionInfo['commandlist'].sort()
    AlienSessionInfo['commandlist'] = sorted(set(AlienSessionInfo['commandlist']))

    # when starting new session prevdir is empty, if set then this is a reconnection
    if AlienSessionInfo['prevdir'] and (AlienSessionInfo['prevdir'] != AlienSessionInfo['currentdir']): cd(wb, AlienSessionInfo['prevdir'], 'log')


def InitConnection(token_args: Union[None, list] = None, use_usercert: bool = False, localConnect: bool = False):
    """Create a session to AliEn services, including session globals and token regeneration"""
    global AlienSessionInfo
    if not token_args: token_args = []
    init_begin = time.perf_counter() if (_TIME_CONNECT or _DEBUG) else None
    wb = AlienConnect(token_args, use_usercert, localConnect)
    if init_begin:
        msg = f">>>   Time for connection: {deltat_ms_perf(init_begin)} ms"
        if _DEBUG: logging.debug(msg)
        if _TIME_CONNECT: print_out(msg)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # NO MATTER WHAT BEFORE ENYTHING ELSE SESSION MUST BE INITIALIZED
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if not AlienSessionInfo['session_started']:  # this is beggining of session, let's get session vars
        AlienSessionInfo['session_started'] = True
        session_begin = time.perf_counter() if init_begin else None
        getSessionVars(wb)  # no matter if command or interactive mode, we need alienHome, currentdir, user and commandlist
        if session_begin:
            msg = f">>>   Time for session initialization: {deltat_us_perf(session_begin)} us"
            if _DEBUG: logging.debug(msg)
            if _TIME_CONNECT: print_out(msg)

    # if usercert connection always regenerate token if connected with usercert
    if AlienSessionInfo['use_usercert'] and token(wb, token_args) != 0: print_err(f'The token could not be created! check the logfile {_DEBUG_FILE}')
    return wb


def token(wb, args: Union[None, list] = None) -> int:
    """(Re)create the tokencert and tokenkey files"""
    global AlienSessionInfo
    if not wb: return 1
    if not args: args = []
    tokencert, tokenkey = get_token_names(True)

    ret_obj = SendMsg(wb, 'token', args, opts = 'nomsg')
    if ret_obj.exitcode != 0:
        logging.error('Token request returned error')
        return retf_print(ret_obj, 'err')
    tokencert_content = ret_obj.ansdict.get('results')[0].get('tokencert', '')
    tokenkey_content = ret_obj.ansdict.get('results')[0].get('tokenkey', '')
    if not tokencert_content or not tokenkey_content:
        logging.error('Token request valid but empty fields!!')
        return int(42)  # ENOMSG

    try:
        if path_readable(tokencert):
            os.chmod(tokencert, 0o600)  # make it writeable
            os.remove(tokencert)
        with open(tokencert, "w", encoding = "ascii", errors = "replace") as tcert: print(f"{tokencert_content}", file = tcert)  # write the tokencert
        os.chmod(tokencert, 0o400)  # make it readonly
    except Exception:
        print_err(f'Error writing to file the aquired token cert; check the log file {_DEBUG_FILE}!')
        logging.debug(traceback.format_exc())
        return 5  # EIO

    try:
        if path_readable(tokenkey):
            os.chmod(tokenkey, 0o600)  # make it writeable
            os.remove(tokenkey)
        with open(tokenkey, "w", encoding = "ascii", errors = "replace") as tkey: print(f"{tokenkey_content}", file = tkey)  # write the tokenkey
        os.chmod(tokenkey, 0o400)  # make it readonly
    except Exception:
        print_err(f'Error writing to file the aquired token key; check the log file {_DEBUG_FILE}!')
        logging.debug(traceback.format_exc())
        return 5  # EIO

    return int(0)


def token_regen(wb, args: Union[None, list] = None):
    global AlienSessionInfo
    wb_usercert = None
    if not args: args = []
    if not AlienSessionInfo['use_usercert']:
        wb_close(wb, code = 1000, reason = 'Lets connect with usercert to be able to generate token')
        try:
            wb_usercert = InitConnection(args, use_usercert = True)  # we have to reconnect with the new token
        except Exception:
            logging.debug(traceback.format_exc())
            return None  # we failed usercert connection

    # now we are connected with usercert, so we can generate token
    if token(wb_usercert, args) != 0: return wb_usercert
    # we have to reconnect with the new token
    wb_close(wb_usercert, code = 1000, reason = 'Re-initialize the connection with the new token')
    AlienSessionInfo['use_usercert'] = False
    wb_token_new = None
    try:
        wb_token_new = InitConnection(args)
        __ = SendMsg(wb_token_new, 'pwd', [], opts = 'nokeys')  # just to refresh cwd
    except Exception:
        logging.exception('token_regen:: error re-initializing connection')
    return wb_token_new


def retf_result2ret(result: Union[str, dict, None]) -> RET:
    """Convert AliEn answer dictionary to RET object"""
    global AlienSessionInfo
    if not result: return RET()
    out_dict = None
    if isinstance(result, str):
        try:
            out_dict = json.loads(result)
        except Exception as e:
            msg = f'retf_result2ret:: Could not load argument as json!\n{e!r}'
            logging.error(msg)
            return RET(1, '', msg)
    else:
        out_dict = result.copy()

    if 'metadata' not in out_dict or 'results' not in out_dict:  # these works only for AliEn responses
        msg = 'retf_results2ret:: Dictionary does not have AliEn answer format'
        logging.error(msg)
        return RET(1, '', msg)

    message_list = [str(item['message']) for item in out_dict['results'] if 'message' in item]
    output = '\n'.join(message_list)
    ret_obj = RET(int(out_dict["metadata"]["exitcode"]), output.strip(), out_dict["metadata"]["error"], out_dict)

    if AlienSessionInfo:  # update global state of session
        AlienSessionInfo['user'] = out_dict["metadata"]["user"]  # always update the current user
        current_dir = out_dict["metadata"]["currentdir"]

        # if this is first connection, current dir is alien home
        if not AlienSessionInfo['alienHome']: AlienSessionInfo['alienHome'] = current_dir

        # update the current current/previous dir status
        prev_dir = AlienSessionInfo['currentdir']  # last known current dir
        if prev_dir != current_dir:
            AlienSessionInfo['currentdir'] = current_dir
            AlienSessionInfo['prevdir'] = prev_dir

        # update directory stack (pushd/popd/dirs)
        short_current_dir = current_dir.replace(AlienSessionInfo['alienHome'][:-1], '~')
        short_current_dir = short_current_dir[:-1]  # remove the last /
        if AlienSessionInfo['pathq']:
            if AlienSessionInfo['pathq'][0] != short_current_dir: AlienSessionInfo['pathq'][0] = short_current_dir
        else:
            push2stack(short_current_dir)
    return ret_obj  # noqa: R504


def retf_print(ret_obj: RET, opts: str = '') -> int:
    """Process a RET object; it will return the exitcode
    opts content will steer the logging and message printing:
     - noprint : silence all stdout/stderr printing
     - noerr/noout : silence the respective messages
     - info/warn/err/debug : will log the stderr to that facility
     - json : will print just the json (if present)
    """
    if 'json' in opts:
        if ret_obj.ansdict:
            json_out = json.dumps(ret_obj.ansdict, sort_keys = True, indent = 3)
            if _DEBUG: logging.debug(json_out)
            print_out(json_out)
        else:
            print_err('This command did not return a json dictionary')
        return ret_obj.exitcode

    if ret_obj.exitcode != 0:
        if 'info' in opts: logging.info(ret_obj.err)
        if 'warn' in opts: logging.warning(ret_obj.err)
        if 'err' in opts: logging.error(ret_obj.err)
        if 'debug' in opts: logging.debug(ret_obj.err)
        if ret_obj.err and not ('noerr' in opts or 'noprint' in opts):
            print_err(f'{ret_obj.err.strip()}')
    else:
        if ret_obj.out and not ('noout' in opts or 'noprint' in opts):
            print_out(f'{ret_obj.out.strip()}')
    return ret_obj.exitcode



def ProcessInput(wb, cmd: str, args: Union[list, None] = None, shellcmd: Union[str, None] = None) -> RET:
    """Process a command line within shell or from command line mode input"""
    global AlienSessionInfo
    if not cmd: return RET(1, '', 'ProcessInput:: Empty input')
    if args is None: args = []
    ret_obj = None

    # implement a time command for measurement of sent/recv delay; for the commands above we do not use timing
    time_begin = msg_timing = None
    if cmd == 'time':  # first to be processed is the time token, it will start the timing and be removed from command
        if not args or is_help(args): return RET(0, 'Command format: time command arguments')
        cmd = args.pop(0)
        time_begin = time.perf_counter()

    # early command aliases and default flags
    if cmd == 'ls': args[0:0] = ['-F']
    if cmd == 'll':
        cmd = 'ls'
        args[0:0] = ['-F', '-l']
    if cmd == 'la':
        cmd = 'ls'
        args[0:0] = ['-F', '-a']
    if cmd == 'lla':
        cmd = 'ls'
        args[0:0] = ['-F', '-l', '-a']

    if cmd in AlienSessionInfo['cmd2func_map_nowb']:  # these commands do NOT need wb connection
        return AlienSessionInfo['cmd2func_map_nowb'][cmd](args)

    opts = ''  # let's proccess special server args
    if get_arg(args, '-nokeys'): opts = f'{opts} nokeys'
    if get_arg(args, '-nomsg'): opts = f'{opts} nomsg'
    if get_arg(args, '-showkeys'): opts = f'{opts} showkeys'
    if get_arg(args, '-showmsg'): opts = f'{opts} showmsg'

    # We will not check for websocket connection as: 1. there is keep alive mechanism 2. there is recovery in SendMsg
    if cmd in AlienSessionInfo['cmd2func_map_client']:  # lookup in clien-side implementations list
        ret_obj = AlienSessionInfo['cmd2func_map_client'][cmd](wb, args)
    elif cmd in AlienSessionInfo['cmd2func_map_srv']:  # lookup in server-side list
        ret_obj = AlienSessionInfo['cmd2func_map_srv'][cmd](wb, cmd, args, opts)

    if time_begin: msg_timing = f">>>ProcessInput time: {deltat_ms_perf(time_begin)} ms"

    if cmd not in AlienSessionInfo['commandlist']:
        similar_list = difflib.get_close_matches(cmd, AlienSessionInfo['commandlist'])
        similar_cmds = None
        if similar_list: similar_cmds = ' '.join(similar_list)
        msg = f'WARNING! command >>> {cmd} <<< not in the list of known commands!'
        if similar_cmds: msg = f'{msg}\nSimilar commands: {similar_cmds}'
        print_err(msg)
    if ret_obj is None: return RET(1, '', f"NO RETURN from command: {cmd} {chr(32).join(args)}")

    if shellcmd:
        if ret_obj.exitcode != 0: return ret_obj
        if not ret_obj.out:
            return RET(1, '', f'Command >>>{cmd} {chr(32).join(args)}<<< do not have output but exitcode == 0')
        shell_run = subprocess.run(shellcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=ret_obj.out, encoding='ascii', shell=True)  # pylint: disable=subprocess-run-check # env=os.environ default is already the process env
        if msg_timing: shell_run.stdout = f'{shell_run.stdout}\n{msg_timing}'
        return RET(shell_run.returncode, shell_run.stdout, shell_run.stderr)

    if msg_timing: ret_obj = ret_obj._replace(out = f'{ret_obj.out}\n{msg_timing}')
    if ret_obj.ansdict and 'metadata' in ret_obj.ansdict and 'timing_ms' in ret_obj.ansdict['metadata']:
        ret_obj = ret_obj._replace(out = f"{ret_obj.out}\ntiming_ms = {ret_obj.ansdict['metadata']['timing_ms']}")
    return ret_obj  # noqa: R504


def ProcessCommandChain(wb = None, cmd_chain: str = '') -> int:
    global AlienSessionInfo, _JSON_OUT
    if not cmd_chain: return int(1)
    # translate aliases in place in the whole string
    if AlienSessionInfo['alias_cache']:
        for alias, alias_value in AlienSessionInfo['alias_cache'].items(): cmd_chain = cmd_chain.replace(alias, alias_value)

    cmdline_list = [str(cmd).strip() for cmd in cmds_split.split(cmd_chain)]  # split commands on ; and \n

    # for each command, save exitcode and RET of the command
    for cmdline in cmdline_list:
        if not cmdline: continue
        if _DEBUG: logging.info('>>> RUN COMMAND: %s', cmdline)
        if cmdline.startswith('!'):  # if shell command, just run it and return
            capture_out = True
            if '-noout' in cmdline:
                cmdline = cmdline.replace(' -noout', '')
                capture_out = False
            ret_obj = runShellCMD(cmdline, capture_out)
            AlienSessionInfo['exitcode'] = retf_print(ret_obj, 'debug')
            continue

        # process the input and take care of pipe to shell
        input_alien, __, pipe_to_shell_cmd = cmdline.partition('|')
        if not input_alien:
            print_out("AliEn command before the | token was not found")
            continue

        args = shlex.split(input_alien.strip())
        cmd = args.pop(0)

        # if globally enabled then enable per command OR if enabled for this command
        _JSON_OUT = _JSON_OUT_GLOBAL or get_arg(args, '-json')
        print_opts = 'debug json' if _JSON_OUT else 'debug'
        if _JSON_OUT and 'json' not in print_opts: print_opts = f'{print_opts} {json}'

        if cmd in AlienSessionInfo['cmd2func_map_nowb']:
            ret_obj = AlienSessionInfo['cmd2func_map_nowb'][cmd](args)
        else:
            if wb is None:
                # we are doing the connection recovery and exception treatment in AlienConnect()
                if cmd == 'token-init' and not is_help(args):
                    wb = InitConnection(args, use_usercert = True)
                else:
                    wb = InitConnection()
            args.append('-nokeys')  # Disable return of the keys. ProcessCommandChain is used for user-based communication so json keys are not needed
            ret_obj = ProcessInput(wb, cmd, args, pipe_to_shell_cmd)

        AlienSessionInfo['exitcode'] = retf_print(ret_obj, print_opts)  # save exitcode for easy retrieval
        if cmd == 'cd': SessionSave()
        _JSON_OUT = _JSON_OUT_GLOBAL  # reset _JSON_OUT if it's not globally enabled (env var or argument to alien.py)
    return AlienSessionInfo['exitcode']


if __name__ == '__main__':
    print('This file should not be executed!', file = sys.stderr, flush = True)
    sys.exit(95)
    
    
    
    