"""
twilio账号配置
"""


# Your Account Sid and Auth Token can be found at
# https://www.twilio.com/console
import os

ACCOUNT_SID = os.environ['account_sid']
AUTH_TOKEN = os.environ['auth_token']
MY_PHONE = os.environ['my_phone']
FROM_PHONE = '+48717166992'
SERVER_IP=os.environ['server_ip']

mongo = {
    'host': '127.0.0.1',
    'port': 27017,
    'max_pool_size': 10,
    'timeout': 1
}

