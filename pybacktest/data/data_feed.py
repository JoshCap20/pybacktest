import logging
import pandas as pd

from .data_series import DataSeries
from ..strategies.strategy import Strategy
from ..indicators.indicator import Indicator

"""
DataFeed is a custom iterator over a pandas DataFrame. Each iteration runs a test on subscriber predicates by calling their test method.

Basically, a wrapper around a pandas DataFrame, an iterator, and a subject/observer pattern.
"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
logger.propagate = False


class DataFeed(object):
    __slots__ = ["_current_index", "_data", "_subscribers"]

    _current_index: int
    _data: pd.DataFrame
    _subscribers: list[Strategy]

    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._subscribers = []
        self._current_index = 0
        logger.debug(f"Data feed initialized with {len(data)} rows.")

    def subscribe(self, strategy: Strategy) -> None:
        """
        Attaches a strategy to the data feed.
        """
        self._subscribers.append(strategy)
        logger.debug(f"Strategy {strategy} attached to the data feed.")

    def __iter__(self):
        """
        Initialize the iteration and return the iterator object.
        """
        self._current_index = 0
        return self

    def __next__(self):
        """
        Iterate over each row in the DataFrame, testing each strategy.
        """
        if self._current_index >= len(self._data):
            self.end()

        row = self._data.iloc[self._current_index]
        data_series = DataSeries(row)
        self._current_index += 1

        return data_series

    def add_indicators(self, indicators: list[Indicator]) -> None:
        """
        Applies an indicator to the data series.
        """
        for indicator in indicators:
            indicator.apply(self._data)
            logger.debug(f"Applied indicator {indicator} to the data feed.")

    def end(self) -> None:
        """
        Ends the data feed iteration.
        """
        logger.debug("Data feed iteration complete.")
        raise StopIteration
