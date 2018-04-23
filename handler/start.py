from handler import BaseHandler
from log import debug
from caller.taskmgr import taskmgr
from caller.event import StartEvent


class StartHandler(BaseHandler):
    def handle(self):
        acc = self.get_argument('account')
        phone = self.get_argument('phone_number')

        debug('account: {}, phone number: {}'.format(acc, phone))

        if acc != "123321123":
            self.write("cant start")
            StartEvent.new(acc, 'none', phone, False)
            return

        for i in range(0, 1):
            taskmgr.start_call(acc, phone)

        StartEvent.new(acc, 'none', phone, True)
