import abc
import requests
import time
import json
from easytrader.utils.misc import file2dict


class IRemoteTrader(abc.ABC):
    @abc.abstractmethod
    def prepare(
            self,
            config_path=None,
            user=None,
            password=None,
            token=None,
            address=None,
    ):
        pass

    @property
    @abc.abstractmethod
    def balance(self):
        pass

    @property
    @abc.abstractmethod
    def position(self):
        pass

    @property
    @abc.abstractmethod
    def today_trades(self):
        pass

    @property
    @abc.abstractmethod
    def today_entrusts(self):
        pass

    @abc.abstractmethod
    def buy(self, stock_id, price: float, amount: int):
        pass

    @abc.abstractmethod
    def sell(self, stock_id, price: float, amount: int):
        pass

    @abc.abstractmethod
    def cancel_entrust(self, entrust_no: str):
        pass


class PAZQRemoteTrader(IRemoteTrader):
    def _api_get(self, func_name: str):
        try:
            return requests.get(
                self.address + func_name,
                timeout=self.timeout,
                headers={'trader-token': self.token}
            ).json()
        except Exception as e:
            print(e)
            return {'status': 'fail', 'msg': 'Network error.'}

    def _api_post(self, func_name: str, params: dict):
        try:
            return requests.post(
                self.address + func_name,
                timeout=self.timeout,
                headers={'trader-token': self.token},
                params=params
            ).json()
        except Exception as e:
            return {'status': 'fail', 'msg': 'Network error.', 'info': e}

    def prepare(
            self,
            config_path=None,
            user=None,
            password=None,
            token=None,
            address=None,
            timeout=5,
    ):
        if config_path is not None:
            account = file2dict(config_path)
            token = account['token']
            #user = account['user']
            #password = account['password']
            address = account['address']
            timeout = account['timeout']
        self.token = token
        self.user = user
        self.password = password
        self.address = address
        self.timeout = timeout
        return self._api_get('prepare')

    @property
    def balance(self):
        return self._api_get("balance")

    @property
    def position(self):
        return self._api_get("position")

    @property
    def today_trades(self):
        return self._api_get("today_trades")

    @property
    def today_entrusts(self):
        return self._api_get("today_entrusts")

    def buy(self, stock_id, price: float, amount: int):
        return self._api_post("buy", {'stock_id': stock_id, 'price': price, 'amount': amount})

    def sell(self, stock_id, price: float, amount: int):
        return self._api_post("sell", {'stock_id': stock_id, 'price': price, 'amount': amount})

    def cancel_entrust(self, entrust_no: str):
        data = self._api_post("cancel_entrust", {'entrust_no': entrust_no})
        if data['status'] == 'success' and '成功' not in data['data']['message']:
            data['status'] = 'fail'
        return data
