import signal
from tornado import httpserver, ioloop
from tornado.web import Application
from tornado.options import define, options

import config
from mongorm import mongoconn
from log import debug
from caller.taskmgr import taskmgr


http_server = None

# define('host', default='127.0.0.1', help='bind this address', type=str)
define('host', default=config.SERVER_IP, help='bind this address', type=str)
define('port', default=5000, help="run on the given port", type=int)


class App(Application):
    def __init__(self):
        urls = {
            ('/start', 'handler.start.StartHandler'),
            ('/stop', 'handler.stop.StopHandler'),
            ('/status', 'handler.status_callback.StatusCallbackHandler')
        }

        settings = dict(
            autoescape=None,
            xsrf_cookies=False,
            debug=True
        )

        Application.__init__(self, urls, **settings)


def shutdown():
    http_server.stop()
    ioloop.IOLoop.instance().stop()


def handle_signal(num, frame):
    taskmgr.stop()

    ioloop.IOLoop.instance().add_callback_from_signal(shutdown)

    debug('caller exit!')


def main():
    options.parse_command_line()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # 初始化mongo配置信息
    mongoconn.config = config.mongo

    status_callback = "http://{}:{}/status".format(options.host,
                                                   options.port)
    debug("status_callback: %s" % status_callback)

    taskmgr.status_callback = status_callback
    taskmgr.start(10)

    global http_server
    http_server = httpserver.HTTPServer(App(), xheaders=True)
    http_server.listen(options.port)

    debug("listen to: {}".format(options.port))

    ioloop.IOLoop.instance().start()
    debug('exit main')


if __name__ == '__main__':
    debug("caller started!")
    main()
