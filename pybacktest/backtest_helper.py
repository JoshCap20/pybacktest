import os
import json
import uuid
import logging
import numpy as np
import pandas as pd
from datetime import datetime
from .plot.results_plot import plot_backtest
from .data.utils import export_to_json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
logger.propagate = False


class BacktestHelper:
    def __init__(self, backtest, plot=False):
        self.backtest = backtest
        self.plot = plot
        self.results = {}
        self.run_id = str(uuid.uuid4())
        self.run_timestamp = datetime.now().isoformat()

    def calculate_performance_metrics(self):
        portfolio = self.backtest._portfolio
        initial_cash = portfolio.initial_cash
        final_cash = portfolio.cash
        final_prices = self.backtest.get_final_prices()
        total_portfolio_value = portfolio.total_portfolio_value(final_prices)
        roi = (total_portfolio_value - initial_cash) / initial_cash
        duration_days = (
            self.backtest._data_feed.end_date - self.backtest._data_feed.start_date
        ).days
        duration_years = duration_days / 365.25 if duration_days > 0 else 0
        avg_roi_per_year = roi / duration_years if duration_years > 0 else roi

        returns = self.calculate_returns()
        sharpe_ratio = self.calculate_sharpe_ratio(returns)

        self.results["performance"] = {
            "initial_balance": initial_cash,
            "final_balance": final_cash,
            "total_portfolio_value": total_portfolio_value,
            "roi": roi,
            "avg_roi_per_year": avg_roi_per_year,
            "sharpe_ratio": sharpe_ratio,
            "duration_days": duration_days,
            "duration_years": duration_years,
        }

    def calculate_returns(self):
        data = self.backtest._data_feed._data.copy()
        data["Total_Portfolio_Value"] = self.backtest.calculate_portfolio_values()
        data["Returns"] = data["Total_Portfolio_Value"].pct_change().fillna(0)
        returns = data["Returns"]
        return returns

    def calculate_sharpe_ratio(self, returns, risk_free_rate=0.0):
        excess_returns = returns - risk_free_rate / 252  # Assuming 252 trading days
        std_dev = excess_returns.std()
        if std_dev != 0:
            sharpe_ratio = np.sqrt(252) * excess_returns.mean() / std_dev
        else:
            sharpe_ratio = np.nan
        return sharpe_ratio

    def generate_results(self):
        self.calculate_performance_metrics()
        portfolio = self.backtest._portfolio
        final_prices = self.backtest.get_final_prices()

        buy_trades = [t for t in portfolio.transaction_history if t["type"] == "buy"]
        sell_trades = [t for t in portfolio.transaction_history if t["type"] == "sell"]

        self.results["strategy"] = [
            strategy.as_dict() for strategy in self.backtest._data_feed._subscribers
        ]
        self.results["portfolio"] = {
            "total_trades": len(portfolio.transaction_history),
            "total_buy_trades": len(buy_trades),
            "total_sell_trades": len(sell_trades),
            "final_positions": portfolio.positions,
            "final_positions_value": self.backtest.get_final_positions_value(
                final_prices
            ),
            "transaction_history": portfolio.transaction_history,
        }
        self.results["backtest_info"] = {
            "run_id": self.run_id,
            "timestamp": self.run_timestamp,
            "symbols": self.backtest._data_feed.symbols,
            "date_range": {
                "start": self.backtest._data_feed.start_date.isoformat(),
                "end": self.backtest._data_feed.end_date.isoformat(),
            },
            "data_hash": hash(self.backtest._data_feed._data.to_csv()),
        }

    def save_results(self, save_path="backtest_runs"):
        self.generate_results()
        os.makedirs(save_path, exist_ok=True)
        run_filepath = os.path.join(save_path, f"run_{self.run_id}")
        os.makedirs(run_filepath, exist_ok=True)

        with open(os.path.join(run_filepath, "backtest_results.json"), "w") as f:
            json.dump(self.results, f, cls=NumpyEncoder, indent=4)

        export_to_json(self.backtest._data_feed._data, run_filepath)

        if self.plot:
            plot_backtest(self.backtest._data_feed._data, run_filepath)

        logger.info(f"Backtest results saved in {run_filepath}")

    def get_results(self):
        return self.results


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
