# -*- coding: utf-8 -*-


class TradeError(Exception):
    def __init__(self, result):
        super(TradeError, self).__init__()
        self.result = result


class NotLoginError(Exception):
    def __init__(self, result=None):
        super(NotLoginError, self).__init__()
        self.result = result
