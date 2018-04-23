from mongorm import Document
from caller.event_pb2 import StartEvent as StartEventPb
from caller.event_pb2 import StopEvent as StopEventPb


class StartEvent(Document):
    _message = StartEventPb
    _datebase = 'test'
    _collection = 'event'

    @classmethod
    def new(cls, account: str, from_: str, to: str, succ: bool):
        ev = StartEvent()
        ev.type = 'start'
        ev.account = account
        ev.from_ = from_
        ev.to = to
        ev.succ = succ
        ev.insert()


class StopEvent(Document):
    _message = StopEventPb
    _database = 'test'
    _collection = 'event'

    @classmethod
    def new(cls, account: str, from_: str, to: str, succ: bool):
        ev = StopEvent()
        ev.type = 'stop'
        ev.account = account
        ev.from_ = from_
        ev.to = to
        ev.succ = succ
        ev.insert()
