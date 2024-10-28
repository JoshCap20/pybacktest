import yfinance as yf
import pandas as pd
from typing import Union, List
import logging

from .data_feed import DataFeed

"""
Wrapper around DataFeed class with Yahoo Finance data fetching.
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
logger.propagate = False


class YahooFinanceDataFeed(DataFeed):
    def __init__(self, symbols: Union[str, List[str]], start: str, end: str):
        """
        Initializes the data feed for one or multiple symbols.
        :param symbols: Single ticker symbol or a list of ticker symbols.
        :param start: Start date for fetching data.
        :param end: End date for fetching data.
        """
        data: pd.DataFrame = YahooFinanceDataFeed.fetch_data(symbols, start, end)
        super().__init__(data)

    @staticmethod
    def fetch_data(
        symbols: Union[str, List[str]], start: str, end: str
    ) -> pd.DataFrame:
        """
        Fetches data from Yahoo Finance for one or multiple symbols.
        """
        data = yf.download(symbols, start=start, end=end, group_by="ticker")

        if YahooFinanceDataFeed.validate_data(data):
            return data
        raise ValueError("YahooFinanceDataFeed: Data validation failed.")

    @staticmethod
    def validate_data(data: pd.DataFrame) -> bool:
        if data.empty:
            logger.error("Fetched data is empty.")
            return False
        if data.isnull().values.any():
            logger.warning("Data contains null values. Consider cleaning the data.")
        # Additional validation checks
        return True
