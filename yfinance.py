import yfinance as yf

#tickers = yf.Tickers('MSFT AAPL GOOG')
#print(tickers.tickers['MSFT'].info)
data = yf.download(['MSFT', 'AAPL', 'GOOG'], period='1y', interval='1h')
data.to_csv('stocks_data.csv')