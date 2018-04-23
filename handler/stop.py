from handler import BaseHandler
from log import debug
from caller.taskmgr import taskmgr
from caller.event import StopEvent


class StopHandler(BaseHandler):
    """
    停止呼叫
    """
    def handle(self):
        acc = self.get_argument('account')
        phone = self.get_argument('phone_number')

        msg = 'account: {}, phone: {}'.format(acc, phone)
        debug(msg)

        if acc != "123321123":
            self.write("cant stop, {}".format(msg))
            StopEvent.new(acc, 'none', phone, False)
        else:
            taskmgr.stop_call(phone)
            StopEvent.new(acc, 'none', phone, True)
