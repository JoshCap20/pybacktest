from numpy import column_stack
from pybacktest.backtest import Backtest
from pybacktest.data.yahoo_finance_data_feed import YahooFinanceDataFeed
from pybacktest.strategies import Strategy, IndicatorInput, Predicate
from pybacktest.indicators import (
    SMAIndicator,
    EMAIndicator,
    RSIIndicator,
    BollingerBands,
    VWAPIndicator,
    vwamp,
)
from pybacktest.actions.buy_action import BuyAction
from pybacktest.actions.sell_action import SellAction
import operator

from pybacktest.data.stock_groups import (
    index_tickers,
    sector_tickers,
    stocks_by_sector,
    all_tickers,
)

# Fetch data
symbols = all_tickers
data_feed = YahooFinanceDataFeed(symbols, start="2018-01-01", end="2023-12-01")

# Add indicators
sma_indicator = SMAIndicator(window=14)
ema_indicator = EMAIndicator(window=25)
rsi_indicator = RSIIndicator(window=14)
bb_indicator = BollingerBands(window=20)
vwamp_indicator = VWAPIndicator(column="Adj Close")
data_feed.add_indicators(
    [sma_indicator, ema_indicator, rsi_indicator, bb_indicator, vwamp_indicator]
)

# Define predicates using Indicator objects
sma_above_ema = Predicate(
    input1=sma_indicator,
    operator=operator.gt,
    input2=ema_indicator,
)

sma_below_ema = ~sma_above_ema

rsi_below_overbought = Predicate(
    input1=rsi_indicator,
    operator=operator.lt,
    input2=70,
)

vwamp_above_price = Predicate(
    input1=IndicatorInput(vwamp_indicator, column_name=vwamp_indicator.indicator_name),
    operator=operator.gt,
    input2="Adj Close",
)

vwamp_below_price = Predicate(
    input1=IndicatorInput(vwamp_indicator, column_name=vwamp_indicator.indicator_name),
    operator=operator.lt,
    input2="Adj Close",
)

price_below_bb = Predicate(
    input1=IndicatorInput(bb_indicator, column_name=bb_indicator.lower_band_name),
    operator=operator.gt,
    input2="Adj Close",
)

rsi_above_oversold = ~rsi_below_overbought


# Define actions
buy_action = BuyAction()
sell_action = SellAction()

# Define strategy
strategy = Strategy(
    entry_conditions=[vwamp_above_price, rsi_below_overbought],
    entry_action=buy_action,
    exit_conditions=[vwamp_below_price],
    exit_action=sell_action,
)

# Subscribe strategy to data feed
data_feed.subscribe(strategy)

# Create and run backtest
backtest = Backtest(data_feed, initial_balance=1000)
backtest.run()
