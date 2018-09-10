import threading
import queue

from log import debug, info, warning
import config
from number.number_mgr import NumberMgr


def hangup(queue, call_sid, called):
    queue.put_nowait({'hangup': call_sid})
    queue.put_nowait({'call': called})
    debug("shutdown sid: %s", call_sid)


class StoppedPhoneNumber(object):
    def __init__(self):
        self.__lock = threading.Lock()
        self.__phone_numbers = set()

    def add(self, phone_number):
        self.__lock.acquire()
        self.__phone_numbers.add(phone_number)
        self.__lock.release()

    def remove(self, phone_number):
        self.__lock.acquire()
        self.__phone_numbers.remove(phone_number)
        self.__lock.release()

    def exist(self, phone_number):
        self.__lock.acquire()
        e = phone_number in self.__phone_numbers
        self.__lock.release()
        return e

    def str(self):
        return ', '.join(self.__phone_numbers)


class CallTask(threading.Thread):
    """
    呼叫任务线程
    队列：
        1. 呼叫队列
        2. 挂机队列
    """
    # 停止呼叫的号码
    stopped_phone_numbers = StoppedPhoneNumber()

    def __init__(self, callmgr, queue):
        threading.Thread.__init__(self)

        # twilio 客户端对象
        self.__client = callmgr
        # 事件队列
        self.__queue = queue
        # 任务运行状态
        self.__running = True
        # 号码管理
        self.__number_mgr = NumberMgr()

    @property
    def callmgr(self):
        return self.__client

    @property
    def queue(self):
        return self.__queue

    @property
    def running(self):
        return self.__running

    @running.setter
    def running(self, b):
        self.__running = b

    def run(self):
        while self.running:
            try:
                event = self.queue.get(block=True, timeout=2)
                info(event)

                if 'start' in event:
                    phone_number = event['start']
                    if CallTask.stopped_phone_numbers.exist(phone_number):
                        CallTask.stopped_phone_numbers.remove(phone_number)

                    self.queue.put_nowait({'call': phone_number})
                # 呼叫事件
                elif 'call' in event:
                    phone_number = event['call']

                    warning("XXXXXXXXX, phone num: %s".format(phone_number))
                    warning(CallTask.stopped_phone_numbers.str())
                    warning("XXXXXXXXX")

                    if not CallTask.stopped_phone_numbers.exist(phone_number):
                        call = self.callmgr.call(self.__number_mgr.get(),
                                                 phone_number)
                        debug('make a call, %s', str(call))
                # 挂断事件
                elif 'hangup' in event:
                    call_sid = event['hangup']
                    self.callmgr.hangup(call_sid)
                # twilio回调状态事件
                elif 'status' in event:
                    status, call_sid, called = event['status']
                    self.__handle_status(status, call_sid, called)
                elif 'stop' in event:
                    """
                    停止呼叫事件，将停止号码加到停止号码集合，呼叫事件中检查
                    并忽略
                    """
                    phone_number = event['stop']
                    CallTask.stopped_phone_numbers.add(phone_number)

                self.queue.task_done()
            except queue.Empty:
                pass
            finally:
                pass

    def __handle_status(self, status, call_sid, called):
        if status == 'answered' or status == 'in-progress':
            self.queue.put_nowait({'hangup': call_sid})
            self.queue.put_nowait({'call': called})
        elif status == 'ringing':
            #self.callmgr.hangup(call_sid)
            timer = threading.Timer(2, hangup, [self.queue, call_sid, called])
            timer.start()
        elif status == 'failed':
            pass
        elif status == 'no-answer':
            pass
        elif status == 'initiated':
            pass

    def stop(self):
        self.running = False
