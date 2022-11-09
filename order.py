import datetime

class Order():
    def __init__(self, quantity, ticker, option):
        self.quantity = quantity
        self.ticker = ticker
        self.option = option
        self.date = datetime.date.today()
    
    def toList(self):
        return [str(self.quantity), str(self.ticker), str(self.option), self.date.strftime("%m/%d/%Y")]