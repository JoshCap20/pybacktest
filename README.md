Work in Progress

Why is every backtesting framework so complex, outdated, and a dependency nightmare? I figured it could be done simply, with a few files, using the iterator, observer, and predicate design pattenrs.

Current Development Notes

Going to keep on developing more indicators before fixing the strategy setup. Ignore strategeries for now. Need to change structure since want to allow strategy to iterate through every stock in a given timeframe for total control.

## Demo

Here is a demo which will retrieve the data for the specified stocks and add the SMA and EMA for each to the dataframe.

```python
from pybacktest import Backtest, Portfolio, DataFeed, YahooFinanceDataFeed
from pybacktest.indicators import SMAIndicator, EMAIndicator
import pandas as pd
import yfinance as yf

symbols = ["AAPL", "MSFT", "GOOGL"]

# Initialize the data feed
data_feed = YahooFinanceDataFeed(symbols, start="2021-01-01", end="2021-12-31")

# Define indicators
ema_indicator = EMAIndicator(window=20)
sma_indicator = SMAIndicator(window=50)

# Apply indicators to the entire DataFrame
data_feed.add_indicators([ema_indicator, sma_indicator])

print(data_feed._data.tail())
```

## Indicators

Indicators modify the entire dataframe explicitly to produce a new column for each stock. An example is adding the SMA indicator:

```python
from pybacktest.indicators import SMAIndicator, EMAIndicator
ema_indicator = EMAIndicator(window=20)
sma_indicator = SMAIndicator(window=50)
data_feed.add_indicators([ema_indicator, sma_indicator])
```

If you were to print the dataframe now, you would notice a new column for each stock with a SMA_50 and EMA_20 column. These are helpful for plotting and analysis. You can then build on these for strategies.

### Indicator Examples

Here are some already implemented indicators:

- See [SMA](indicators/sma.py) for the Simple Moving Average default implementation.
- See [EMA](indicators/ema.py) for the Exponential Moving Average default implementation.

### Indicator Interface

If you feel like building your own just extend the Indicator interface and implement the apply method. It receives a multiimdex dataframe where keys are stock and close/open/high/low/volume and values are the respective values.

Indicators should create a new column for each stock in the dataframe with the indicator values.

```python
class Indicator(object):
    def apply(self, data: pd.DataFrame) -> pd.Series:
        """
        Calculates the indicator values for the given data and returns a Series.
        """
        raise NotImplementedError
```
