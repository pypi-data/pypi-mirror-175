



def DO_queryML(args: Union[list, None] = None) -> RET:
    """submit: process submit commands for local jdl cases"""
    global AlienSessionInfo
    if args is None: args = []
    if is_help(args):
        msg_help = ('usage: queryML <ML node>\n'
                    'time range can be specified for a parameter:\n'
                    '/[starting time spec]/[ending time spec]/parameter\n'
                    'where the two time specs can be given in absolute epoch timestamp (in milliseconds), as positive values,\n'
                    'or relative timestamp to `now`, when they are negative.\nFor example `-60000` would be "1 minute ago" and effectively `-1` means "now".')
        return RET(0, msg_help)
    types = ('text', 'xml', 'json')
    for t in types: get_arg(args, t)
    args.append('json')
    retobj = queryML(args)
    q_dict = retobj.ansdict

    if retobj.exitcode != 0: return RET(retobj.exitcode, '', f'Error getting query: {" ".join(args)}')
    ans_list = retobj.ansdict["results"]
    if len(ans_list) == 0: return RET(retobj.exitcode, f'queryML:: Empty answer from query: {" ".join(args)}')

    if 'Timestamp' in ans_list[0]:
        for item in ans_list: item['Timestamp'] = unixtime2local(item['Timestamp'])

    # all elements will have the same key names
    # n_columns = len(ans_list[0])
    keys = ans_list[0].keys()

    # establish keys width
    max_value_size = [len(key) for key in keys]
    for row in ans_list:
        for idx, key in enumerate(keys):
            max_value_size[idx] = max(max_value_size[idx], len(str(row.get(key))))
    max_value_size[:] = [w + 3 for w in max_value_size]

    # create width specification list
    row_format_list = [f'{{: <{str(w)}}}' for w in max_value_size]
    row_format = "".join(row_format_list)

    msg = row_format.format(*keys)
    for row in ans_list:
        value_list = [row.get(key) for key in keys]
        msg = f'{msg}\n{row_format.format(*value_list)}'
    return RET(0, msg, '', q_dict)



def DO_checkAddr(args: Union[list, None] = None) -> RET:
    global AlienSessionInfo
    if is_help(args):
        msg = ('checkAddr [reference] fqdn/ip port\n'
               'defaults are: alice-jcentral.cern.ch 8097\n'
               'reference arg will check connection to google dns and www.cern.ch')
        return RET(0, msg)
    result_list = []
    if get_arg(args, 'reference'):
        result_list.extend(check_port('8.8.8.8', 53))
        result_list.extend(check_port('2001:4860:4860::8888', 53))
        result_list.extend(check_port('www.cern.ch', 80))
    addr = args[0] if args else 'alice-jcentral.cern.ch'
    port = args[1] if (args and len(args) > 1) else 8097
    result_list.extend(check_port(addr, port))
    stdout = ''
    for res in result_list:
        stdout += f'{res[0]}:{res[1]}        {PrintColor(COLORS.BIGreen) + "OK" if res[-1] else PrintColor(COLORS.BIRed) + "FAIL"}{PrintColor(COLORS.ColorReset)}\n'
    return RET(0, stdout)





def DO_prompt(args: Union[list, None] = None) -> RET:
    """Add local dir and date information to the alien.py shell prompt"""
    global AlienSessionInfo
    if args is None: args = []
    if not args or is_help(args):
        msg = "Toggle the following in the command prompt : <date> for date information and <pwd> for local directory"
        return RET(0, msg)

    if 'date' in args: AlienSessionInfo['show_date'] = (not AlienSessionInfo['show_date'])
    if 'pwd' in args: AlienSessionInfo['show_lpwd'] = (not AlienSessionInfo['show_lpwd'])
    return RET(0)




def DO_tokendestroy(args: Union[list, None] = None) -> RET:
    if args is None: args = []
    if len(args) > 0 and is_help(args): return RET(0, "Delete the token{cert,key}.pem files")
    tokencert, tokenkey = get_token_names()
    if os.path.exists(tokencert): os.remove(tokencert)
    if os.path.exists(tokenkey): os.remove(tokenkey)
    return RET(0, "Token was destroyed! Re-connect for token re-creation.")


def DO_certinfo(args: Union[list, None] = None) -> RET:
    if args is None: args = []
    cert, __ = get_files_cert()
    if len(args) > 0 and is_help(args): return RET(0, "Print user certificate information", "")
    return CertInfo(cert)


def DO_tokeninfo(args: Union[list, None] = None) -> RET:
    if not args: args = []
    if len(args) > 0 and is_help(args): return RET(0, "Print token certificate information", "")
    tokencert, __ = get_valid_tokens()
    return CertInfo(tokencert)



def DO_certverify(args: Union[list, None] = None) -> RET:
    if args is None: args = []
    cert, __ = get_files_cert()
    if len(args) > 0 and is_help(args): return RET(0, "Verify the user cert against the found CA stores (file or directory)", "")
    return CertVerify(cert)


def DO_tokenverify(args: Union[list, None] = None) -> RET:
    if not args: args = []
    if len(args) > 0 and is_help(args): return RET(0, "Print token certificate information", "")
    tokencert, __ = get_valid_tokens()
    return CertVerify(tokencert)


def DO_certkeymatch(args: Union[list, None] = None) -> RET:
    if args is None: args = []
    cert, key = get_files_cert()
    if len(args) > 0 and is_help(args): return RET(0, "Check match of user cert with key cert", "")
    return CertKeyMatch(cert, key)


def DO_tokenkeymatch(args: Union[list, None] = None) -> RET:
    if args is None: args = []
    cert, key = get_valid_tokens()
    if len(args) > 0 and is_help(args): return RET(0, "Check match of user token with key token", "")
    return CertKeyMatch(cert, key)































