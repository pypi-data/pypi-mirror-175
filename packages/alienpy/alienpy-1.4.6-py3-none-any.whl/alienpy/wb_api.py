from wb_base import *


def SendMsg(wb, cmdline: str, args: Union[None, list] = None, opts: str = '') -> Union[RET, str]:
    """Send a json message to the specified websocket; it will return the server answer"""
    if not wb:
        msg = "SendMsg:: websocket not initialized"
        logging.info(msg)
        return '' if 'rawstr' in opts else RET(1, '', msg)
    if not args: args = []
    time_begin = time.perf_counter() if _DEBUG or _DEBUG_TIMING else None
    if _JSON_OUT_GLOBAL or _JSON_OUT or _DEBUG:  # if jsout output was requested, then make sure we get the full answer
        opts = opts.replace('nokeys', '').replace('nomsg', '')

    json_signature = ['{"command":', '"options":']
    # if already json format just use it as is; nomsg/nokeys will be passed to CreateJsonCommand
    jsonmsg = cmdline if all(x in cmdline for x in json_signature) else CreateJsonCommand(cmdline, args, opts)

    if not jsonmsg:
        logging.info("SendMsg:: json message is empty!")
        return '' if 'rawstr' in opts else RET(1, '', f"SendMsg:: empty json with args:: {cmdline} {' '.join(args)} /opts= {opts}")

    if _DEBUG:
        logging.debug(f"Called from: {sys._getframe().f_back.f_code.co_name}\n>>>   SEND COMMAND:: {jsonmsg}")  # pylint: disable=protected-access

    nr_tries = int(1)
    result = None
    while result is None:
        if nr_tries > 3: break
        nr_tries += 1
        try:
            result = __sendmsg(wb, jsonmsg)
        except Exception as e:
            logging.exception('SendMsg:: Error sending: %s\nBecause of %s', jsonmsg, e.__cause__)
            wb = InitConnection()
        if result is None: time.sleep(0.2)

    if time_begin: logging.debug('SendMsg::Result received: %s ms', deltat_ms_perf(time_begin))
    if not result:
        msg = f"SendMsg:: could not send command: {jsonmsg}\nCheck {_DEBUG_FILE}"
        print_err(msg)
        logging.error(msg)
        return RET(70, '', 'SendMsg:: Empty result received from server')  # ECOMM

    if 'rawstr' in opts: return result
    time_begin_decode = time.perf_counter() if _DEBUG or _DEBUG_TIMING else None
    ret_obj = retf_result2ret(result)
    if time_begin_decode: logging.debug('SendMsg::Result decoded: %s us', deltat_us_perf(time_begin_decode))
    return ret_obj  # noqa: R504


def SendMsgMulti(wb, cmds_list: list, opts: str = '') -> list:
    """Send a json message to the specified websocket; it will return the server answer"""
    if not wb:
        msg = "SendMsg:: websocket not initialized"
        logging.info(msg)
        return '' if 'rawstr' in opts else RET(1, '', msg)
    if not cmds_list: return []
    time_begin = time.perf_counter() if _DEBUG or _DEBUG_TIMING else None
    if _JSON_OUT_GLOBAL or _JSON_OUT or _DEBUG:  # if jsout output was requested, then make sure we get the full answer
        opts = opts.replace('nokeys', '').replace('nomsg', '')

    json_signature = ['{"command":', '"options":']
    json_cmd_list = []
    for cmd_str in cmds_list:
        # if already json format just use it as is; nomsg/nokeys will be passed to CreateJsonCommand
        jsonmsg = cmd_str if all(x in cmd_str for x in json_signature) else CreateJsonCommand(cmd_str, [], opts)
        json_cmd_list.append(jsonmsg)

    if _DEBUG:
        logging.debug(f"Called from: {sys._getframe().f_back.f_code.co_name}\nSEND COMMAND:: {chr(32).join(json_cmd_list)}")  # pylint: disable=protected-access

    nr_tries = int(1)
    result_list = None
    while result_list is None:
        if nr_tries > 3: break
        nr_tries += 1
        try:
            result_list = __sendmsg_multi(wb, json_cmd_list)
        except wb_exceptions.ConnectionClosed as e:
            logging.exception('SendMsgMulti:: failure because of %s', e.__cause__)
            try:
                wb = InitConnection()
            except Exception:
                logging.exception('SendMsgMulti:: Could not recover connection when disconnected!!')
        except Exception:
            logging.exception('SendMsgMulti:: Abnormal connection status!!!')
        if result_list is None: time.sleep(0.2)

    if time_begin: logging.debug('SendMsg::Result received: %s ms', deltat_ms(time_begin))
    if not result_list: return []
    if 'rawstr' in opts: return result_list
    time_begin_decode = time.perf_counter() if _DEBUG or _DEBUG_TIMING else None
    ret_obj_list = [retf_result2ret(result) for result in result_list]
    if time_begin_decode: logging.debug('SendMsg::Result decoded: %s ms', deltat_ms(time_begin_decode))
    return ret_obj_list  # noqa: R504



def wb_ping(wb) -> float:
    """Websocket ping function, it will return rtt in ms"""
    init_begin = time.perf_counter()
    if IsWbConnected(wb):
        return float(deltat_ms_perf(init_begin))
    return float(-1)



if __name__ == '__main__':
    print('This file should not be executed!', file = sys.stderr, flush = True)
    sys.exit(95)
    
    
    
    

