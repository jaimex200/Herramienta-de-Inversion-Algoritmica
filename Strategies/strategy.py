from abc import ABC, abstractmethod
import yfinance as yf
import uuid

# Abstract class of all strategies
class Strategy(ABC):
    def __init__(self, name, ticker, interval, qty):
        self.name = name
        self.ticker = ticker
        self.interval = int(int(interval) * 86400)
        self.qty = qty

    # Use yahoo finance to take the actual price
    def get_actual_price(self, ticker):
        tickerData = yf.Ticker(ticker)
        ## confirm that ticker exist on yf
        if tickerData.info['regularMarketPrice'] is None:
            try:
                data = tickerData.history()
                return data['Close'].iloc[-1]
            except:
                raise NameError(ticker)
        return tickerData.info['regularMarketPrice']

    @abstractmethod
    def strategy(self):
        pass

    @abstractmethod
    def get_info(self):
        pass