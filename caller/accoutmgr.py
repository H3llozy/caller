"""
用户账户管理
"""
from mongorm import Document


class Accoutmgr(object):
    def __init__(self):
        pass

    def check_expire(self, acct):
        """
        检查是否到期
        """
        pass

    def add_account(self, expire_timestarmp):
        pass

    def del_account(self, acct):
        pass

    def get_account(self, acct):
        pass
