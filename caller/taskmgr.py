class Taskmgr(object):
    def __init__(self):
        # 启动时的任务队列
        self.__status_callback = ''  # 回调url
        self.__tasks = []

        from queue import Queue
        self.__queue = Queue(1000)

    @property
    def tasks(self):
        return self.__tasks

    @property
    def queue(self):
        return self.__queue

    @property
    def status_callback(self):
        return self.__status_callback

    @status_callback.setter
    def status_callback(self, status):
        self.__status_callback = status

    def start(self, task_num):
        from caller.callmgr import Callmgr
        from caller.calltask import CallTask

        callmgr = Callmgr(self.status_callback)
        for i in range(0, task_num):
            task = CallTask(callmgr, self.queue)
            task.start()
            self.tasks.append(task)

    def stop(self):
        self.queue.join()

        for t in self.tasks:
            t.stop()

    def start_call(self, account, phone_number):
        """
        生成呼叫事件
        """
        self.queue.put_nowait({'start': phone_number})

    def status(self, status, call_sid, called):
        """
        状态回调
        """
        self.queue.put_nowait({'status': (status, call_sid, called)})

    def stop_call(self, phone_number):
        """
        停止呼叫号码
        """
        self.queue.put_nowait({'stop': phone_number})


taskmgr = Taskmgr()
