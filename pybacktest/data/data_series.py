import pandas as pd

class DataSeries(object):
    row: pd.Series
    
    def __init__(self, row: pd.Series):
        """
        Initializes a DataSeries wrapper around a single row in the DataFeed.
        :param row: A Series representing a row from the DataFeed DataFrame.
        """
        self.row = row

    def get(self, symbol: str, column: str) -> float:
        """
        Returns the value for a specific stock and column at this timeframe.
        :param symbol: The stock symbol (e.g., 'AAPL').
        :param column: The column name (e.g., 'Close').
        :return: The value for the stock's column at this timeframe.
        """
        try:
            value = self.row[(symbol, column)]
            if isinstance(value, pd.Series):
                raise ValueError(f"Expected a scalar value, but got a Series for symbol '{symbol}' and column '{column}'.")
            return float(value)
        except KeyError:
            raise KeyError(f"Column '{column}' for symbol '{symbol}' does not exist.")

    def all_symbols(self):
        """
        Returns all symbols available in this DataSeries.
        """
        return self.row.index.get_level_values(0).unique()
    
    def all_columns(self):
        """
        Returns all column types available in this DataSeries.
        """
        return self.row.index.get_level_values(1).unique()
