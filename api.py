import requests, json

class ApiMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Api(metaclass=ApiMeta):
    def __init__(self):
        file = open("app.config", "r")
        lines = file.readlines()

        data = list(map( lambda x: x.strip("\n").split("="), lines))

        self.base_url           = "https://paper-api.alpaca.markets"
        self.account_url        = self.base_url + "/v2/account"
        self.orders_url         = self.base_url + "/v2/orders"
        self.open_position_url  = self.base_url + "/v2/positions"
        self.headers            = {"APCA-API-KEY-ID": data[5][1], "APCA-API-SECRET-KEY": data[6][1]}

    def get_account(self):
        r = requests.get(self.account_url, headers=self.headers)
        return json.loads(r.content)

    def get_cash(self):
        return float(self.get_account().get('cash'))
    
    def send_order(self, order):
        data = {
            "symbol": order.ticker.replace("-", ""),
            "qty": order.quantity,
            "side": order.option,
            "type": 'market',
            "time_in_force": 'gtc'
        }
        r = requests.post(self.orders_url, json=data, headers=self.headers)
        return json.loads(r.content)