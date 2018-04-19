from handler import BaseHandler
from log import debug
from caller.taskmgr import taskmgr


class StatusCallbackHandler(BaseHandler):
    def handle(self):
        status = self.get_argument('CallStatus')
        call_sid = self.get_argument('CallSid')
        called = self.get_argument('Called')
        debug('status: {}, call sid: {}, called: {}'.format(
            status, call_sid, called))
        taskmgr.status(status, call_sid, called)

        self.write('200')
