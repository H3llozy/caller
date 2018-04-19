from tornado.web import RequestHandler
from log import warning


class BaseHandler(RequestHandler):
    def handle(self):
        raise Exception('not supported')

    def post(self):
        try:
            self.handle()
        except Exception as e:
            warning(e)
        finally:
            pass

    def get(self):
        try:
            self.handle()
        except Exception as e:
            warning(e)
        finally:
            pass
