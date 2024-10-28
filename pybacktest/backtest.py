from .data import DataFeed
from .portfolio import Portfolio

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
logger.propagate = False


class Backtest(object):
    def __init__(self, data_feed: DataFeed, initial_balance: float = 10000.0) -> None:
        self._data_feed = data_feed
        self._portfolio = Portfolio(initial_balance)
        self._context = {"portfolio": self._portfolio}

    def run(self) -> None:
        for data in self._data_feed:
            context = self._context.copy()
            context["data_feed"] = self._data_feed
            for strategy in self._data_feed._subscribers:
                strategy.apply(data, context)

    def run(self) -> None:
        """
        Runs the backtest to completion.
        """
        if not self._data_feed._subscribers:
            logger.warning("No subscribers attached to the data feed.")

        if self._data_feed._data.empty:
            logger.error(f"No data in the data feed\nData: {self._data_feed._data}")
            return

        # Iterate over the data feed
        for data_series in self._data_feed:
            context = self._context.copy()
            context["data_feed"] = self._data_feed
            context["index"] = self._data_feed._current_index
            # Apply strategies
            for strategy in self._data_feed._subscribers:
                strategy.apply(data_series, context)

    def buy(self, symbol: str, amount: float, price: float) -> None:
        self._portfolio.buy(symbol, amount, price)

    def sell(self, symbol: str, amount: float, price: float) -> None:
        self._portfolio.sell(symbol, amount, price)

    def calculate_performance(self, final_prices: dict):
        total_portfolio_value = self._portfolio.total_portfolio_value(final_prices)
        total_return = (
            total_portfolio_value - self._portfolio.initial_cash
        ) / self._portfolio.initial_cash
        logger.info(f"Total Return: {total_return * 100:.2f}%")

        # Implement additional metrics like Sharpe ratio, drawdowns, etc.

    def get_final_prices(self) -> dict:
        # Extract final prices from the data feed
        final_prices = {}
        last_row = self._data_feed._data.iloc[-1]
        for symbol in last_row.index.get_level_values(0).unique():
            final_prices[symbol] = last_row[(symbol, "Close")]
        return final_prices

    # Portfolio Metrics
    def get_final_portfolio(self) -> Portfolio:
        return self._portfolio

    def get_final_balance(self) -> float:
        return self._portfolio.balance

    def get_final_positions(self) -> dict:
        return self._portfolio.positions

    def get_final_value(self) -> float:
        return self._portfolio.balance + sum(self._portfolio.positions.values())

    def get_final_profit(self) -> float:
        return self.get_final_value() - self._portfolio.balance

    def get_final_roi(self) -> float:
        return self.get_final_profit() / self._portfolio.balance

    def get_final_roi_pct(self) -> float:
        return self.get_final_roi() * 100

    def get_final_positions_value(self, price_data: dict) -> float:
        return sum(
            [
                amount * price_data[symbol]
                for symbol, amount in self._portfolio.positions.items()
            ]
        )

    def get_final_positions_roi(self, price_data: dict) -> float:
        return self.get_final_positions_value(price_data) - self._portfolio.balance

    def get_final_positions_roi_pct(self, price_data: dict) -> float:
        return self.get_final_positions_roi(price_data) / self._portfolio.balance * 100

    def get_final_positions_roi_per_symbol(self, price_data: dict) -> dict:
        return {
            symbol: amount * price_data[symbol] - self._portfolio.balance
            for symbol, amount in self._portfolio.positions.items()
        }

    def get_final_positions_roi_pct_per_symbol(self, price_data: dict) -> dict:
        return {
            symbol: (amount * price_data[symbol] - self._portfolio.balance)
            / self._portfolio.balance
            * 100
            for symbol, amount in self._portfolio.positions.items()
        }
