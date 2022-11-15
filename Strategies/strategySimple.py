from Strategies.strategy import Strategy
from order import Order


class StrategySimple(Strategy):
    def __init__(self, name, ticker, interval, qty):
        super().__init__(name, ticker, interval, qty)
        self.lastPrice = self.get_actual_price(self.ticker)
    
    def strategy(self):
        actualPrice = self.get_actual_price(self.ticker)
        res = actualPrice - self.lastPrice
    
        if res < 0:
            self.lastPrice = actualPrice
            return Order(self.qty, self.ticker, "sell")
        else:
            self.lastPrice = actualPrice
            return Order(self.qty, self.ticker, "buy")
    
    def get_info(self):
        return {"name": self.name, "ticker": self.ticker, "interval": self.interval/86400, "quantity": self.qty}
