from Strategies.strategy import Strategy
from order import Order


class StrategySimple(Strategy):
    def __init__(self, name, ticker, interval):
        super().__init__(name, ticker, interval)
        self.lastPrice = self.get_actual_price(self.ticker)
    
    def strategy(self):
        actualPrice = self.get_actual_price(self.ticker)
        res = actualPrice - self.lastPrice
    
        if res < 0:
            self.lastPrice = actualPrice
            return Order(0.01, self.ticker, "sell")
        else:
            self.lastPrice = actualPrice
            return Order(0.01, self.ticker, "buy")
