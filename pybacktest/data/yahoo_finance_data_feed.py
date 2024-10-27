import yfinance as yf
import pandas as pd
from typing import Union, List
from .data_feed import DataFeed

"""
Wrapper around DataFeed class with Yahoo Finance data fetching.
"""

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
    def fetch_data(symbols: Union[str, List[str]], start: str, end: str) -> pd.DataFrame:
        """
        Fetches data from Yahoo Finance for one or multiple symbols.
        """
        data = yf.download(symbols, start=start, end=end, group_by='ticker')

        if YahooFinanceDataFeed.validate_data(data):
            return data
        raise ValueError("YahooFinanceDataFeed: Data validation failed.")
    
    @staticmethod
    def validate_data(data: pd.DataFrame)-> bool:
        # TODO
        return True