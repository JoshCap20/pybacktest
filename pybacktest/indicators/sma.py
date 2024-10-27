from .indicator import Indicator
import pandas as pd


class SMAIndicator(Indicator):
    def __init__(self, window: int, column: str = "Close"):
        self.window = window
        self.column = column

    def apply(self, data: pd.DataFrame) -> None:
        """
        Calculates the SMA for each symbol in the multi-index DataFrame and adds it as a new column.
        """
        for symbol in data.columns.get_level_values(0).unique():
            sma_column_name = f"SMA_{self.window}"
            data[(symbol, sma_column_name)] = data[(symbol, self.column)].rolling(window=self.window).mean()
