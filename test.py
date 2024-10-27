from pybacktest import Backtest, Portfolio, DataFeed, YahooFinanceDataFeed
from pybacktest.indicators import (
    SMAIndicator,
    EMAIndicator,
    ATRIndicator,
    BollingerBands,
    RSIIndicator,
    MACDIndicator,
    StochasticOscillator,
    ATRIndicator,
    ADXIndicator,
    FibonacciRetracementLevels,
    OBVIndicator,
    VWAPIndicator,
    KeltnerChannels,
    keltner_channels,
)
import pandas as pd
import yfinance as yf

# Example usage
symbols = ["AAPL", "MSFT", "GOOGL"]
# Initialize the data feed
data_feed = YahooFinanceDataFeed(symbols, start="2021-01-01", end="2021-12-31")

# Define indicators
ema_indicator = EMAIndicator(window=20)
sma_indicator = SMAIndicator(window=50)
atr_indicator = ATRIndicator(window=20)
bb_indicator = BollingerBands(window=20)
rsi_indicator = RSIIndicator(window=14)
macd_indicator = MACDIndicator()
stochastic_indicator = StochasticOscillator()
adx_indicator = ADXIndicator(window=14)
fibonacci_retracement_levels = FibonacciRetracementLevels()
obv_indicator = OBVIndicator()
vwap_indicator = VWAPIndicator()
keltner_channels = KeltnerChannels(window=20)


indicators = [
    ema_indicator,
    sma_indicator,
    atr_indicator,
    bb_indicator,
    rsi_indicator,
    macd_indicator,
    stochastic_indicator,
    atr_indicator,
    adx_indicator,
    fibonacci_retracement_levels,
    obv_indicator,
    vwap_indicator,
    keltner_channels,
]
# Apply indicators to the entire DataFrame
data_feed.add_indicators(indicators)

data_feed.run()

print(data_feed._data.tail())
data_feed._data.to_csv("data.csv")
