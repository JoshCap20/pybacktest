from pybacktest import YahooFinanceDataFeed
from pybacktest.indicators import SMAIndicator, EMAIndicator

# Example usage
symbols = ["AAPL", "MSFT", "GOOGL"]
# data = yf.download(symbols, start="2021-01-01", end="2021-12-31", group_by="ticker")

# Initialize the data feed
# data_feed = DataFeed(data)
data_feed = YahooFinanceDataFeed(symbols, start="2021-01-01", end="2021-12-31")

# Define indicators
ema_indicator = EMAIndicator(window=20)
sma_indicator = SMAIndicator(window=50)

# Apply indicators to the entire DataFrame
data_feed.add_indicators([ema_indicator, sma_indicator])

print(data_feed._data.tail())