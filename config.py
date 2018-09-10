"""
twilio账号配置
"""

# Your Account Sid and Auth Token can be found at
# https://www.twilio.com/console
import os

ACCOUNT_SID = os.environ['account_sid']
AUTH_TOKEN = os.environ['auth_token']
MY_PHONE = os.environ['my_phone']  # 自己的账号绑定号码，测试号码
SERVER_IP = os.environ['server_ip']

mongo = {
    'host': '127.0.0.1',
    'port': 27017,
    'max_pool_size': 10,
    'timeout': 1,
    'auth': [{
        'db_name': 'test',
        'user': 'zh',
        'passwd': '123321'
    }]
}
