from handler import BaseHandler
from log import debug
from caller.taskmgr import taskmgr


class StartHandler(BaseHandler):
    def handle(self):
        acc = self.get_argument('account')
        phone = self.get_argument('phone_number')

        debug('account: {}, phone number: {}'.format(acc, phone))

        if acc != "123321123":
            self.write("cant start")
            return

        for i in range(0, 1):
            taskmgr.start_call(acc, phone)
