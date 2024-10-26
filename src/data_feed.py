import logging
import pandas as pd
from .strategy import Strategy

"""
DataFeed is a custom iterator over a pandas DataFrame. Each iteration runs a test on subscriber predicates by calling their test method.

Basically, a wrapper around a pandas DataFrame, an iterator, and a subject/observer pattern.
"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
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
        logging.debug(f"Data feed initialized with {len(data)} rows.")

    def subscribe(self, strategy: Strategy) -> None:
        """
        Attaches a strategy to the data feed.
        """
        self._subscribers.append(strategy)
        logging.debug(f"Strategy {strategy} attached to the data feed.")

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
            logging.info("Data feed iteration complete.")
            raise StopIteration

        row = self._data.iloc[self._current_index]
        self._current_index += 1

        for strategy in self._subscribers:
            logging.debug(f"Testing strategy {strategy} on row {row.name}")
            if strategy.test(row):
                logging.debug(f"Strategy {strategy} triggered on row {row.name}")
                strategy.apply(row)

        return row

    def run(self) -> None:
        """
        Runs the data feed to completion.

        Automatically calls all strategies for all rows via iterator override.
        """
        if not self._subscribers:
            logging.warning("No subscribers attached to the data feed.")

        if self._data.empty:
            logging.error(f"No data in the data feed\nData: {self._data}")
            return

        for _ in self:
            pass
