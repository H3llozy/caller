from queue import Queue

from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

from log import debug
from parse_args import parse_args
from callmgr import Callmgr
from calltask import CallTask

app = Flask(__name__)
queue = Queue(1000)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with brief messages."""
    # Start out TwiML respond
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Thank you for calling! Have a great day.", voice='alice')

    return str(resp)


@app.route("/call", methods=['POST'])
def make_call():
    # debug(request.form)
    debug("call account: %s", request.form.get('account'))
    account = request.form.get("account")
    to_phone = request.form.get("phone_number")

    if account is None or to_phone is None:
        return "please enter account or phone number"

    # 向队列中添加呼叫事件
    for i in (0, 10):
        queue.put_nowait({'call': to_phone})

    return '200'


@app.route("/fail", methods=['POST'])
def fail():
    debug("failed")


@app.route("/status", methods=['GET', 'POST'])
def call_status():
    # debug(request.form)
    status = request.form.get('CallStatus')
    call_sid = request.form.get('CallSid')
    called = request.form.get('Called')

    if status is None or call_sid is None:
        return '10000'

    debug('call status: %s, call_sid: %s, called: %s',
          status, call_sid, called)

    queue.put_nowait({'status': status, 'call_sid': call_sid,
                      'called': called})

    return '200'


def main():
    debug('started!')

    args = parse_args()

    status_callback = "http://{}:{}/status".format(args.host, args.port)
    debug(status_callback)
    callmgr = Callmgr(status_callback)
    for i in range(0, 15):
        t = CallTask(callmgr, queue)
        t.start()

    app.run(host='0.0.0.0', port=args.port, debug=True)
    # app.run(host='127.0.0.1', debug=True)

    queue.join()
    t.stop()


if __name__ == "__main__":
    main()
