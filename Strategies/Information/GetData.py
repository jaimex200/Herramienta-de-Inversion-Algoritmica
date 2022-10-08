import yfinance as yf

def get_data(ticker, start_date, end_date):
    try:
        tickerData = yf.Ticker(ticker)

        stock_data = tickerData.history(period = 'id', start = start_date, end = end_date, interval="1d")
    except:
        get_data(ticker, start_date, end_date)
    return stock_data