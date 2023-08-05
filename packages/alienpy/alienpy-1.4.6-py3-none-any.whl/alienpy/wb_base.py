import sys
import asyncio
import threading
import socket

if not os.getenv('ALIENPY_NO_STAGGER'):
    try:
        import async_stagger
    except Exception:
        print("async_stagger module could not be load", file = sys.stderr, flush = True)
        sys.exit(1)

try:
    import websockets.client as wb_client
    import websockets.exceptions as wb_exceptions
    import websockets.version as wb_version
    from websockets.extensions import permessage_deflate as _wb_permessage_deflate
except Exception:
    print("websockets module could not be load", file = sys.stderr, flush = True)
    sys.exit(1)

from ssl_tools import *

#########################
#   ASYNCIO MECHANICS
#########################
def start_asyncio():
    """Initialization of main thread that will keep the asyncio loop"""
    ready = threading.Event()

    def _cancel_all_tasks(loop_to_cancel):
        to_cancel = None
        if sys.version_info[1] < 7:
            to_cancel = asyncio.Task.all_tasks(loop_to_cancel)
        else:
            to_cancel = asyncio.all_tasks(loop_to_cancel)
        if not to_cancel: return
        for task in to_cancel: task.cancel()
        loop_to_cancel.run_until_complete(asyncio.tasks.gather(*to_cancel, loop = loop_to_cancel, return_exceptions = True))

        for task in to_cancel:
            if task.cancelled(): continue
            if task.exception() is not None:
                loop_to_cancel.call_exception_handler({'message': 'unhandled exception during asyncio.run() shutdown', 'exception': task.exception(), 'task': task})

    def run(mainasync, *, debug = False):
        global _alienpy_global_asyncio_loop
        if asyncio.events._get_running_loop() is not None: raise RuntimeError('asyncio.run() cannot be called from a running event loop')  # pylint: disable=protected-access
        if not asyncio.coroutines.iscoroutine(mainasync): raise ValueError(f'a coroutine was expected, got {mainasync!r}')

        _alienpy_global_asyncio_loop = asyncio.events.new_event_loop()
        try:
            asyncio.events.set_event_loop(_alienpy_global_asyncio_loop)
            _alienpy_global_asyncio_loop.set_debug(debug)
            return _alienpy_global_asyncio_loop.run_until_complete(mainasync)
        finally:
            try:
                _cancel_all_tasks(_alienpy_global_asyncio_loop)
                _alienpy_global_asyncio_loop.run_until_complete(_alienpy_global_asyncio_loop.shutdown_asyncgens())
            finally:
                asyncio.events.set_event_loop(None)
                _alienpy_global_asyncio_loop.close()

    async def wait_forever():
        global _alienpy_global_asyncio_loop
        _alienpy_global_asyncio_loop = asyncio.get_event_loop()
        ready.set()
        await _alienpy_global_asyncio_loop.create_future()

    threading.Thread(daemon = True, target = run, args = (wait_forever(),)).start()
    ready.wait()


def syncify(fn):
    """DECORATOR FOR SYNCIFY FUNCTIONS:: the magic for un-async functions"""
    def syncfn(*args, **kwds):
        # submit the original coroutine to the event loop and wait for the result
        conc_future = asyncio.run_coroutine_threadsafe(fn(*args, **kwds), _alienpy_global_asyncio_loop)
        return conc_future.result()
    syncfn.as_async = fn
    return syncfn


@syncify
async def IsWbConnected(wb) -> bool:
    """Check if websocket is connected with the protocol ping/pong"""
    time_begin = time.perf_counter() if _DEBUG_TIMING else None
    if _DEBUG:
        logging.info('Called from: %s', sys._getframe().f_back.f_code.co_name)  # pylint: disable=protected-access
    try:
        pong_waiter = await wb.ping()
        await pong_waiter
    except Exception:
        logging.exception('WB ping/pong failed!!!')
        return False
    if time_begin: logging.error('>>>IsWbConnected time = %s ms', deltat_ms_perf(time_begin))
    return True


@syncify
async def wb_close(wb, code, reason):
    """Send close to websocket"""
    try:
        await wb.close(code = code, reason = reason)
    except Exception:
        pass


@syncify
async def msg_proxy(websocket, use_usercert = False):
    """Proxy messages from a connection point to another"""
    wb_jalien = AlienConnect(None, use_usercert)
    local_query = await websocket.recv()
    jalien_answer = SendMsg(wb_jalien, local_query)
    await websocket.send(jalien_answer.ansdict)


@syncify
async def __sendmsg(wb, jsonmsg: str) -> str:
    """The low level async function for send/receive"""
    time_begin = None
    if _DEBUG_TIMING: time_begin = time.perf_counter()
    await wb.send(jsonmsg)
    result = await wb.recv()
    if time_begin: logging.debug('>>>__sendmsg time = %s ms', deltat_ms_perf(time_begin))
    return result  # noqa: R504


@syncify
async def __sendmsg_multi(wb, jsonmsg_list: list) -> list:
    """The low level async function for send/receive multiple messages once"""
    if not jsonmsg_list: return []
    time_begin = None
    if _DEBUG_TIMING: time_begin = time.perf_counter()
    for msg in jsonmsg_list: await wb.send(msg)

    result_list = []
    for _i in range(len(jsonmsg_list)):
        result = await wb.recv()
        result_list.append(result)

    if time_begin: logging.debug('>>>__sendmsg time = %s ms', deltat_ms_perf(time_begin))
    return result_list


@syncify
async def wb_create(host: str = 'localhost', port: Union[str, int] = '0', path: str = '/', use_usercert: bool = False, localConnect: bool = False):
    """Create a websocket to wss://host:port/path (it is implied a SSL context)"""
    QUEUE_SIZE = int(128)  # maximum length of the queue that holds incoming messages
    MSG_SIZE = None  # int(20 * 1024 * 1024)  # maximum size for incoming messages in bytes. The default value is 1 MiB. None disables the limit
    PING_TIMEOUT = int(os.getenv('ALIENPY_TIMEOUT', '20'))  # If the corresponding Pong frame isn’t received within ping_timeout seconds, the connection is considered unusable and is closed
    PING_INTERVAL = PING_TIMEOUT  # Ping frame is sent every ping_interval seconds
    CLOSE_TIMEOUT = int(10)  # maximum wait time in seconds for completing the closing handshake and terminating the TCP connection
    # https://websockets.readthedocs.io/en/stable/api.html#websockets.protocol.WebSocketCommonProtocol
    # we use some conservative values, higher than this might hurt the sensitivity to intreruptions

    wb = None
    ctx = None
    #  client_max_window_bits = 12,  # tomcat endpoint does not allow anything other than 15, so let's just choose a mem default towards speed
    deflateFact = _wb_permessage_deflate.ClientPerMessageDeflateFactory(compress_settings={'memLevel': 4})
    headers_list = [('User-Agent', f'alien.py/{ALIENPY_VERSION_STR} websockets/{wb_version.version}')]
    if localConnect:
        fHostWSUrl = 'ws://localhost/'
        logging.info('Request connection to : %s', fHostWSUrl)
        socket_filename = f'{__TMPDIR}/jboxpy_{str(os.getuid())}.sock'
        try:
            wb = await wb_client.unix_connect(socket_filename, fHostWSUrl,
                                              max_queue = QUEUE_SIZE, max_size = MSG_SIZE,
                                              ping_interval = PING_INTERVAL, ping_timeout = PING_TIMEOUT,
                                              close_timeout = CLOSE_TIMEOUT, extra_headers = headers_list)
        except Exception as e:
            msg = f'Could NOT establish connection (local socket) to {socket_filename}\n{e!r}'
            logging.error(msg)
            print_err(f'{msg}\nCheck the logfile: {_DEBUG_FILE}')
            return None
    else:
        fHostWSUrl = f'wss://{host}:{port}{path}'  # conection url
        ctx = create_ssl_context(use_usercert)  # will check validity of token and if invalid cert will be usercert
        logging.info('Request connection to: %s:%s%s', host, port, path)

        socket_endpoint = None
        # https://async-stagger.readthedocs.io/en/latest/reference.html#async_stagger.create_connected_sock
        # AI_* flags --> https://linux.die.net/man/3/getaddrinfo
        try:
            if _DEBUG:
                logging.debug('TRY ENDPOINT: %s:%s', host, port)
                init_begin = time.perf_counter()
            if os.getenv('ALIENPY_NO_STAGGER'):
                socket_endpoint = socket.create_connection((host, int(port)))
            else:
                socket_endpoint = await async_stagger.create_connected_sock(host, int(port), async_dns = True, delay = 0, resolution_delay = 0.050, detailed_exceptions = True)
            if _DEBUG:
                logging.debug('TCP SOCKET DELTA: %s ms', deltat_ms_perf(init_begin))
        except Exception as e:
            msg = f'Could NOT establish connection (TCP socket) to {host}:{port}\n{e!r}'
            logging.error(msg)
            print_err(f'{msg}\nCheck the logfile: {_DEBUG_FILE}')
            return None

        if socket_endpoint:
            socket_endpoint_addr = socket_endpoint.getpeername()[0]
            socket_endpoint_port = socket_endpoint.getpeername()[1]
            logging.info('GOT SOCKET TO: %s:%s', socket_endpoint_addr, socket_endpoint_port)
            try:
                if _DEBUG: init_begin = time.perf_counter()
                wb = await wb_client.connect(fHostWSUrl, sock = socket_endpoint, server_hostname = host, ssl = ctx, extensions=[deflateFact],
                                             max_queue=QUEUE_SIZE, max_size=MSG_SIZE,
                                             ping_interval=PING_INTERVAL, ping_timeout=PING_TIMEOUT,
                                             close_timeout=CLOSE_TIMEOUT, extra_headers=headers_list)

                if _DEBUG:
                    logging.debug('WEBSOCKET DELTA: %s ms', deltat_ms_perf(init_begin))

            except wb_exceptions.InvalidStatusCode as e:
                msg = f'Invalid status code {e.status_code} connecting to {socket_endpoint_addr}:{socket_endpoint_port}\n{e!r}'
                logging.error(msg)
                print_err(f'{msg}\nCheck the logfile: {_DEBUG_FILE}')
                if int(e.status_code) == 401:
                    print_err('The status code indicate that your certificate is not authorized.\nCheck the correct certificate registration into ALICE VO')
                    os._exit(129)
                return None
            except Exception as e:
                msg = f'Could NOT establish connection (WebSocket) to {socket_endpoint_addr}:{socket_endpoint_port}\n{e!r}'
                logging.error(msg)
                print_err(f'{msg}\nCheck the logfile: {_DEBUG_FILE}')
                return None
        if wb: logging.info('CONNECTED: %s:%s', wb.remote_address[0], wb.remote_address[1])
    return wb


def wb_create_tryout(host: str = 'localhost', port: Union[str, int] = '0', path: str = '/', use_usercert: bool = False, localConnect: bool = False):
    """WebSocket creation with tryouts (configurable by env ALIENPY_CONNECT_TRIES and ALIENPY_CONNECT_TRIES_INTERVAL)"""
    wb = None
    nr_tries = 0
    init_begin = None
    if _TIME_CONNECT or _DEBUG: init_begin = time.perf_counter()
    connect_tries = int(os.getenv('ALIENPY_CONNECT_TRIES', '3'))
    connect_tries_interval = float(os.getenv('ALIENPY_CONNECT_TRIES_INTERVAL', '0.5'))

    while wb is None:
        nr_tries += 1
        try:
            wb = wb_create(host, str(port), path, use_usercert, localConnect)
        except Exception:
            logging.exception('wb_create_tryout:: exception when wb_create')
        if not wb:
            if nr_tries >= connect_tries:
                logging.error('We tried on %s:%s%s %s times', host, port, path, nr_tries)
                break
            time.sleep(connect_tries_interval)

    if init_begin:
        fail_msg = 'trials ' if not wb else ''
        msg = f'>>>   Websocket {fail_msg}connecting time: {deltat_ms_perf(init_begin)} ms'
        if _DEBUG: logging.debug(msg)
        if _TIME_CONNECT: print_out(msg)

    if wb and localConnect:
        pid_filename = f'{__TMPDIR}/jboxpy_{os.getuid()}.pid'
        writePidFile(pid_filename)
    return wb









if __name__ == '__main__':
    print('This file should not be executed!', file = sys.stderr, flush = True)
    sys.exit(95)
    
    















