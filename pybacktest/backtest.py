import os
import json
from pdb import run
import uuid
import logging
import numpy as np
import pandas as pd
from datetime import datetime


from .data import DataFeed
from .portfolio import Portfolio
from .plot.results_plot import plot_backtest
from .data.utils import export_to_json

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

        final_prices = self.get_final_prices()
        performance_metrics = self.calculate_performance(final_prices)
        total_portfolio_value = self._portfolio.total_portfolio_value(final_prices)
        roi = (
            total_portfolio_value - self._portfolio.initial_cash
        ) / self._portfolio.initial_cash
        logger.info("Backtest completed.")

        # Prepare results dictionary
        results = {
            "run_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "initial_balance": self._portfolio.initial_cash,
            "final_balance": self._portfolio.cash,
            "total_portfolio_value": total_portfolio_value,
            "roi": roi,
            # "total_return": performance_metrics.get("total_return"),
            # "symbols": self._data_feed.symbols,
            # "date_range": {"start": self._data_feed.start, "end": self._data_feed.end},
            "strategy": [
                strategy.as_dict() for strategy in self._data_feed._subscribers
            ],
            "transaction_history": self._portfolio.transaction_history,
            "final_positions": self._portfolio.positions,
            "data_hash": hash(self._data_feed._data.to_csv()),
        }

        os.makedirs("backtest_runs", exist_ok=True)
        run_filepath = f"backtest_runs/run_{results['run_id']}"

        data = self._data_feed._data.copy()
        print(data)
        data.columns = ["_".join(map(str, col)).strip() for col in data.columns.values]
        data = data.replace([np.nan, np.inf, -np.inf], None)
        data.reset_index(inplace=True)
        data["Date"] = data["Date"].apply(
            lambda x: x.isoformat() if isinstance(x, datetime) else x
        )
        results["data"] = data.to_dict(orient="records")
        results["performance"] = self.get_results()

        os.makedirs(run_filepath, exist_ok=True)
        with open(f"{run_filepath}/backtest.json", "w") as f:
            json.dump(results, f, cls=NumpyEncoder, indent=4)

        export_to_json(self._data_feed._data, run_filepath)
        plot_backtest(self._data_feed._data, run_filepath)
        logger.info(f"Run saved as {run_filepath}")

        print(f"Total Portfolio Value: ${results['total_portfolio_value']:.2f}")
        print(f"Final Cash: ${results['final_balance']:.2f}")
        print(f"Return on Investment: {roi:.2%}")

    def buy(self, symbol: str, amount: float, price: float) -> None:
        self._portfolio.buy(symbol, amount, price)

    def sell(self, symbol: str, amount: float, price: float) -> None:
        self._portfolio.sell(symbol, amount, price)

    def calculate_performance(self, final_prices: dict):
        total_portfolio_value = self._portfolio.total_portfolio_value(final_prices)
        total_return = (
            total_portfolio_value - self._portfolio.initial_cash
        ) / self._portfolio.initial_cash

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

    def get_final_positions(self) -> dict:
        return self._portfolio.positions

    def get_final_positions_value(self, price_data: dict) -> float:
        return sum(
            [
                amount * price_data[symbol]
                for symbol, amount in self._portfolio.positions.items()
            ]
        )

    def get_results(self):
        return {
            "performance": {
                "total_return": self.calculate_performance(self.get_final_prices()),
                "initial_cash": self._portfolio.initial_cash,
                "final_cash": self._portfolio.cash,
                "final_positions": self.get_final_positions(),
                "final_positions_value": self.get_final_positions_value(
                    self.get_final_prices()
                ),
            },
            "portfolio": self._portfolio.__dict__,
        }


class NumpyEncoder(json.JSONEncoder):
    """Custom encoder for numpy data types and datetime objects."""

    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            if np.isnan(obj) or np.isinf(obj):
                return None
            else:
                return float(obj)
        elif isinstance(obj, (np.ndarray, list)):
            return [None if (pd.isnull(x) or np.isinf(x)) else x for x in obj]
        elif isinstance(obj, (datetime, np.datetime64)):
            return str(obj)
        else:
            return super(NumpyEncoder, self).default(obj)
