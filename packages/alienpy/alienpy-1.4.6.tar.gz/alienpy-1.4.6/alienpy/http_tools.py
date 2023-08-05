

from data import *



def queryML(args: list = None) -> RET:
    """submit: process submit commands for local jdl cases"""
    alimon = 'http://alimonitor.cern.ch/rest/'
    type_json = '?Accept=application/json'
    type_xml = '?Accept=text/xml'
    type_plain = '?Accept=text/plain'
    type_default = ''
    predicate = ''

    if 'text' in args:
        type_default = type_plain
        args.remove('text')
    if 'xml' in args:
        type_default = type_xml
        args.remove('xml')
    if 'json' in args:
        type_default = type_json
        args.remove('json')

    if args: predicate = args[0]
    url = f'{alimon}{predicate}{type_default}'
    exitcode = stdout = stderr = ansdict = ansraw = None

    url_req = urlreq.Request(url)
    with urlreq.urlopen(url_req) as req:
        ansraw = req.read().decode()
        exitcode = 0 if (req.getcode() == 200) else req.getcode()

    if type_default == type_json:
        stdout = stderr = ''
        ansdict = json.loads(ansraw)
    else:
        stdout, stderr = (ansraw, '') if exitcode == 0 else ('', ansraw)
    return RET(exitcode, stdout, stderr, ansdict)



if __name__ == '__main__':
    print('This file should not be executed!', file = sys.stderr, flush = True)
    sys.exit(95)