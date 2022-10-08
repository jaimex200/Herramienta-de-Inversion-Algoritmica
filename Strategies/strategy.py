from abc import ABC, abstractmethod
import yfinance as yf
import uuid

# Abstract class of all strategies
class Strategy(ABC):
    def __init__(self, name, ticker, interval):
        self.name = name
        self.ticker = ticker
        self.interval = int(int(interval) * 86400)
        self.id = uuid.uuid4()

    # Use yahoo finance to take the actual price
    def get_actual_price(selfd, ticker):
        tickerData = yf.Ticker(ticker)
        ## confirm that ticker exist on yf
        if tickerData.info['regularMarketPrice'] is None:
            raise NameError(ticker)
        return tickerData.info['regularMarketPrice']

    @abstractmethod
    def strategy(self):
        pass