import logging
import pandas as pd

from .data import DataFeed
from .portfolio import Portfolio
from .backtest_helper import BacktestHelper

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
logger.propagate = False


class Backtest(object):

    def __init__(
        self, data_feed: DataFeed, initial_balance: float = 10000.0, plot: bool = False
    ) -> None:
        self._data_feed = data_feed
        self._portfolio = Portfolio(initial_balance)
        self._context = {"portfolio": self._portfolio}
        self.plot = plot
        self.helper = BacktestHelper(self, plot=self.plot)

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

        logger.info("Backtest completed.")

        # Generate and save results
        self.helper.save_results()

        # Print summary
        results = self.helper.get_results()
        performance = results["performance"]
        print(f"Total Portfolio Value: ${performance['total_portfolio_value']:.2f}")
        print(f"ROI: {performance['roi']:.2%}")
        print(f"Average ROI per Year: {performance['avg_roi_per_year']:.2%}")
        print(f"Sharpe Ratio: {performance['sharpe_ratio']:.4f}")
