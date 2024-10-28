# PyBacktest

PyBacktest is a simple and intuitive backtesting framework for Python. It aims to reduce the complexity often associated with backtesting libraries, allowing you to focus on developing and testing trading strategies with ease.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Key Concepts](#key-concepts)
  - [Indicators](#indicators)
  - [Predicates](#predicates)
  - [Strategies](#strategies)
  - [Actions](#actions)
- [API Reference](#api-reference)
  - [DataFeed](#datafeed)
  - [Indicators](#indicators-api)
  - [Predicates](#predicates-api)
  - [Strategies](#strategies-api)
  - [Actions](#actions-api)
  - [Backtest](#backtest)
  - [Portfolio](#portfolio)
- [Examples](#examples)
  - [Indicator Demo: Feature Engineering](#indicator-demo-feature-engineering)
  - [Strategy Demo: SMA EMA Crossover](#strategy-demo-sma-ema-crossover)
- [Advanced Usage](#advanced-usage)
  - [Creating Custom Indicators](#creating-custom-indicators)
  - [Extending Strategies](#extending-strategies)
- [Contributing](#contributing)
- [License](#license)

## Overview

Current backtesting frameworks are often overly complex and difficult to use. PyBacktest simplifies the process by providing:

- A modular structure with clear components.
- An intuitive API for defining indicators, predicates, strategies, and actions.
- Easy integration with data sources like Yahoo Finance.
- Flexibility to extend and customize components according to your needs.

Every backtest run automatically outputs to the run directory all of the data used, trades made, and other relevant information, including graphs of stocks with indicators overlayed. This makes it easy to analyze and visualize the results of your backtest.

## Features

- **Simple API**: Minimal boilerplate code to set up and run backtests.
- **Modular Design**: Components like indicators and strategies are modular and reusable.
- **Extensibility**: Easily create custom indicators and strategies.
- **Data Integration**: Built-in support for fetching data from Yahoo Finance using `yfinance`.
- **Real-Time Simulation**: Step through data points to simulate real-time trading decisions.

## Installation

Install PyBacktest using pip:

```bash
pip install pybacktest
```

## Quick Start

Here's how you can get started with PyBacktest in just a few steps.

```python
from pybacktest import Backtest, YahooFinanceDataFeed
from pybacktest.indicators import SMAIndicator, EMAIndicator
from pybacktest.predicates import Predicate
from pybacktest.strategies import Strategy
from pybacktest.actions import BuyAction, SellAction
import operator

# Define symbols and fetch data
symbols = ["AAPL", "MSFT", "GOOGL"]
data_feed = YahooFinanceDataFeed(symbols, start="2021-01-01", end="2021-12-31")

# Add indicators
sma_indicator = SMAIndicator(window=14)
ema_indicator = EMAIndicator(window=25)
data_feed.add_indicators([sma_indicator, ema_indicator])

# Define predicates
sma_below_ema = Predicate(sma_indicator, operator.lt, ema_indicator)
sma_above_ema = Predicate(sma_indicator, operator.gt, ema_indicator)

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
```

## Key Concepts

### Indicators

Indicators transform data and add new columns to the DataFrame for each stock. They are akin to feature engineering in machine learning. When an indicator is added, it mutates the DataFrame to include its own columns.

Examples of indicators:

- SMA (Simple Moving Average)
- EMA (Exponential Moving Average)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)

### Predicates

Predicates use indicators, comparison operators, and values to return a boolean. They form the logical conditions for strategies.

Example Predicate:

```python
from pybacktest.strategies import Predicate
import operator

sma_below_ema = Predicate(
        input1=sma_indicator,
        operator=operator.lt,
        input2=ema_indicator
)
```

### Strategies

Strategies are composed of one or more predicates with actions to take when they evaluate to True. They define the entry and exit points of your trading algorithm.

Example Strategy:

```python
from pybacktest.strategies import Strategy

strategy = Strategy(
        entry_conditions=[sma_below_ema],
        entry_action=buy_action,
        exit_conditions=[sma_above_ema],
        exit_action=sell_action,
)
```

### Actions

Actions are what happens when predicates evaluate to True in a strategy. Common actions include buying or selling assets.

Available Actions:

- BuyAction
- SellAction

## API Reference

### DataFeed

The `DataFeed` class handles the data input for the backtest. It manages the data retrieval, indicator application, and strategy subscriptions.

YahooFinanceDataFeed Example:

```python
from pybacktest.data.yahoo_finance_data_feed import YahooFinanceDataFeed

data_feed = YahooFinanceDataFeed(symbols=["AAPL"], start="2021-01-01", end="2021-12-31")
```

Methods:

- `add_indicators(indicators)`: Adds indicators to the data feed.
- `subscribe(strategy)`: Subscribes a strategy to the data feed.

### Indicators API

Indicators calculate specific metrics based on historical data and add them to the DataFrame.

Base Indicator Class:

```python
from pybacktest.indicators import Indicator

class Indicator:
        def apply(self, data: pd.DataFrame) -> None:
                pass
```

Built-in Indicators:

- `SMAIndicator(window)`
- `EMAIndicator(window)`
- `RSIIndicator(window)`
- `MACDIndicator()`
- `BollingerBandsIndicator(window)`
- `ATRIndicator(window)`
- `ADXIndicator(window)`
- `OBVIndicator()`

Adding Indicators:

```python
from pybacktest.indicators import SMAIndicator, EMAIndicator

sma_indicator = SMAIndicator(window=14)
ema_indicator = EMAIndicator(window=25)
data_feed.add_indicators([sma_indicator, ema_indicator])
```

### Predicates API

Predicates evaluate conditions based on indicators or specific values. This should be intuitive: in order to take an action, whether buy or sell, there must be some definite condition to encapsulate that logic. Predicates are the way to do that.

Predicate Class:

```python
from pybacktest.strategies import Predicate

predicate = Predicate(
        input1=indicator_or_value,
        operator=comparison_operator,
        input2=indicator_or_value
)
```

Operators:

- `operator.lt` (less than)
- `operator.gt` (greater than)
- `operator.eq` (equal to)
- `operator.ne` (not equal)
- `operator.le` (less than or equal to)
- `operator.ge` (greater than or equal to)

Example:

```python
import operator

rsi_below_70 = Predicate(
        input1=rsi_indicator,
        operator=operator.lt,
        input2=70  # Comparing RSI value to 70
)

vwamp_above_price = Predicate(
    input1=IndicatorInput(vwamp_indicator, column_name=vwamp_indicator.indicator_name),
    operator=operator.gt,
    input2="Adj Close",
)

sma_above_ema = Predicate(
    input1=sma_indicator,
    operator=operator.gt,
    input2=ema_indicator,
)
```

#### Predicate Extension via Bitwise Operators

To make using predicates even easier, you can use the following bitwise operators to extend the functionality of the `Predicate` class:

- `&` (and)
- `|` (or)
- `~` (not)

```python
# Example of combining predicates
combined_predicate = rsi_below_70 & sma_above_ema

# Example of negating a predicate
rsi_above_70 = ~rsi_below_70
```

**These are brand new and in testing stages. Please report any issues you may encounter.**

### Strategies API

Strategies combine predicates and actions to define trading logic.

Strategy Class:

```python
from pybacktest.strategies import Strategy

strategy = Strategy(
        entry_conditions=[predicate1, predicate2],
        entry_action=buy_action,
        exit_conditions=[predicate3],
        exit_action=sell_action,
)
```

Methods:

- `apply(data, context)`: Applies the strategy to the data at each time step.

### Actions API

Actions define what happens when a strategy's conditions are met.

Action Base Class:

```python
from pybacktest.actions import Action

class Action:
        def execute(self, data: pd.Series, context: dict) -> None:
                pass
```

Available Actions:

- `BuyAction()`
- `SellAction()`

Using Actions:

```python
from pybacktest.actions import BuyAction, SellAction

buy_action = BuyAction()
sell_action = SellAction()
```

### Backtest

The `Backtest` class orchestrates the execution of the backtest.

Creating a Backtest:

```python
from pybacktest import Backtest

backtest = Backtest(data_feed, initial_balance=10000)
```

Running the Backtest:

```python
backtest.run()
```

### Portfolio

The `Portfolio` class manages cash, positions, and transaction history.

Portfolio Attributes:

- `cash`: Current cash balance.
- `positions`: Dictionary of symbol to quantity held.
- `transaction_history`: List of transactions executed.

Portfolio Methods:

- `buy(symbol, quantity, price, timestamp)`: Buys a specified quantity of a symbol.
- `sell(symbol, quantity, price, timestamp)`: Sells a specified quantity of a symbol.
- `total_portfolio_value(current_prices)`: Calculates the total value of the portfolio.

## Examples

### Indicator Demo: Feature Engineering

This demo retrieves data for specified stocks and adds SMA and EMA indicators to the DataFrame.

```python
from pybacktest import YahooFinanceDataFeed
from pybacktest.indicators import SMAIndicator, EMAIndicator

symbols = ["AAPL", "MSFT", "GOOGL"]

# Initialize data feed
data_feed = YahooFinanceDataFeed(symbols, start="2021-01-01", end="2021-12-31")

# Define indicators
sma_indicator = SMAIndicator(window=50)
ema_indicator = EMAIndicator(window=20)

# Add indicators to data feed
data_feed.add_indicators([sma_indicator, ema_indicator])

# Display the modified DataFrame
print(data_feed._data.tail())
```

### Strategy Demo: SMA EMA Crossover

This strategy buys when the SMA crosses below the EMA and sells when the SMA crosses above the EMA.

```python
from pybacktest import Backtest, YahooFinanceDataFeed
from pybacktest.indicators import SMAIndicator, EMAIndicator
from pybacktest.strategies import Predicate, Strategy
from pybacktest.actions import BuyAction, SellAction
import operator

# Fetch data
symbols = ["AAPL", "MSFT", "GOOGL"]
data_feed = YahooFinanceDataFeed(symbols, start="2020-01-01", end="2020-12-01")

# Add indicators
sma_indicator = SMAIndicator(window=14)
ema_indicator = EMAIndicator(window=25)
data_feed.add_indicators([sma_indicator, ema_indicator])

# Define predicates
sma_below_ema = Predicate(
        input1=sma_indicator,
        operator=operator.lt,
        input2=ema_indicator
)

sma_above_ema = Predicate(
        input1=sma_indicator,
        operator=operator.gt,
        input2=ema_indicator
)

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
```

### Strategy Demo: VWAMP and Price Crossover

This strategy buys when the SMA crosses below the EMA and sells when the SMA crosses above the EMA.

```python
from pybacktest import Backtest, YahooFinanceDataFeed
from pybacktest.indicators import VWAPIndicator
from pybacktest.strategies import Predicate, Strategy, IndicatorInput
from pybacktest.actions import BuyAction, SellAction
from pybacktest.data.stock_groups import SPY_500
import operator

# Fetch data
symbols = SPY_500
data_feed = YahooFinanceDataFeed(symbols, start="2020-01-01", end="2020-12-01")

# Add indicators
vwamp_indicator = VWAPIndicator(column="Adj Close")
data_feed.add_indicators([vwamp_indicator])

# Define predicates
# Note: When an indicator has multiple column names, one must be explicitly specified via an IndicatorInput object
vwamp_above_price = Predicate(
    input1=IndicatorInput(vwamp_indicator, column_name=vwamp_indicator.indicator_name),
    operator=operator.gt,
    input2="Adj Close",
)

# We can use the overridden operators to negate predicates
vwamp_below_price = ~vwamp_above_price

# Define actions
buy_action = BuyAction()
sell_action = SellAction()

# Define strategy
strategy = Strategy(
    entry_conditions=[vwamp_above_price],
    entry_action=buy_action,
    exit_conditions=[vwamp_below_price],
    exit_action=sell_action,
)

# Subscribe strategy to data feed
data_feed.subscribe(strategy)

# Create and run backtest
backtest = Backtest(data_feed, initial_balance=10000)
backtest.run()
```

## Advanced Usage

### Creating Custom Indicators

You can extend the `Indicator` base class to create custom indicators.

```python
from pybacktest.indicators import Indicator

class CustomIndicator(Indicator):
        def __init__(self, window, column: str = "Close"):
                self.window = windows
                self.column = column
                self.column_names = [f"Custom_{window}"]

        def apply(self, data: pd.DataFrame) -> None:
                for symbol in data.columns.get_level_values(0).unique():
                        data[(symbol, self.column_names[0])] = (
                                data[(symbol, self.column)].rolling(window=self.window).mean()
                        )
```

Usage:

```python
custom_indicator = CustomIndicator(window=10)
data_feed.add_indicators([custom_indicator])
```

### Extending Strategies

You can create more complex strategies by combining multiple predicates and actions.

Example:

```python
from pybacktest.indicators import RSIIndicator
from pybacktest.predicates import Predicate
import operator

# Add RSI indicator
rsi_indicator = RSIIndicator(window=14)
data_feed.add_indicators([rsi_indicator])

# Define additional predicates
rsi_below_30 = Predicate(
        input1=rsi_indicator,
        operator=operator.lt,
        input2=30
)

# Update strategy
strategy = Strategy(
        entry_conditions=[sma_below_ema, rsi_below_30],
        entry_action=buy_action,
        exit_conditions=[sma_above_ema],
        exit_action=sell_action,
)
```

## Contributing

Contributions are welcome! If you'd like to contribute to PyBacktest, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.
