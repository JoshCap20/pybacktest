from pybacktest.backtest import Backtest
from pybacktest.data.yahoo_finance_data_feed import YahooFinanceDataFeed
from pybacktest.strategies import Strategy, IndicatorInput, Predicate
from pybacktest.indicators import SMAIndicator, EMAIndicator, MACDIndicator
from pybacktest.actions.buy_action import BuyAction
from pybacktest.actions.sell_action import SellAction
import operator

# Fetch data
symbols = ["AAPL", "MSFT", "GOOGL"]
data_feed = YahooFinanceDataFeed(symbols, start="2020-01-01", end="2020-12-31")

# Add indicators
sma_indicator = SMAIndicator(window=14)
ema_indicator = EMAIndicator(window=25)
macd_indicator = MACDIndicator()
data_feed.add_indicators([sma_indicator, ema_indicator, macd_indicator])

# Define predicates using Indicator objects
sma_above_ema = Predicate(
    input1=sma_indicator,
    operator=operator.gt,
    input2=ema_indicator,
)

sma_below_ema = Predicate(
    input1=sma_indicator,
    operator=operator.lt,
    input2=ema_indicator,
)

# macd_line_input = IndicatorInput(
#     macd_indicator, column_name=macd_indicator.macd_line_name
# )

# macd_above_signal = Predicate(
#     input1=macd_line_input,
#     operator=operator.gt,
#     input2=IndicatorInput(macd_indicator, column_name=macd_indicator.signal_line_name),
# )

# Define actions
buy_action = BuyAction()
sell_action = SellAction()

# Define strategy
strategy = Strategy(
    entry_conditions=[sma_below_ema],
    entry_action=buy_action,
    exit_conditions=[sma_above_ema],
    exit_action=sell_action,
)

# Subscribe strategy to data feed
data_feed.subscribe(strategy)

# Create and run backtest
backtest = Backtest(data_feed, initial_balance=10000)
backtest.run()

# After running, you can analyze the results
final_prices = backtest.get_final_prices()
backtest.calculate_performance(final_prices)
