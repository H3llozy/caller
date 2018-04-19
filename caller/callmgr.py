# 管理正在呼叫的会话信息
import threading
from twilio.rest import Client

import config
from log import warning


class Callmgr(object):
    def __init__(self, status_callback):
        self.__sid_dict = {}
        self.__client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)
        self.__lock = threading.Lock()
        self.__status_callback = status_callback

    @property
    def client(self):
        return self.__client

    @property
    def sidDict(self):
        return self.__sid_dict

    def push(self, phone_number, call_sid):
        if phone_number in self.sidDict:
            lst = self.sidDict[phone_number]
            lst.append(call_sid)
        else:
            lst = self.sidDict[phone_number] = []
            lst.append(call_sid)

    def popAll(self, phone_number):
        """
        根据电话号码获取相关呼叫信息
        """
        if phone_number in self.sidDict:
            return self.sidDict[phone_number].pop(phone_number)
        else:
            return []

    def call(self, from_phone, to_phone):
        """
        给目标号码打电话
        """
        self.__lock.acquire()
        cal = None
        try:
            status_callback_event = ["initiated", "ringing", "answered",
                                     "completed"],
            cal = self.client.calls.create(
                from_=from_phone,
                to=to_phone,
                url="http://demo.twilio.com/docs/voice.xml",
                method="GET",
                status_callback=self.__status_callback,
                status_callback_method='POST',
                status_callback_event=status_callback_event)
        except Exception as e:
            warning(e)
        finally:
            self.__lock.release()

        return cal

    def hangup(self, call_sid):
        self.__lock.acquire()

        cal = self.client.calls(call_sid)
        cal.update(status='completed')

        self.__lock.release()


if __name__ == '__main__':
    status_callback = "http://{}:{}/status".format(config.SERVER_IP, 5000)
    callmgr = Callmgr(status_callback)

    to_phone = config.MY_PHONE

    cal = callmgr.call(config.FROM_PHONE, no_phone)
    status = cal.status
    callmgr.hangup(cal.sid)

    print("done")
