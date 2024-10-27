from .indicator import Indicator
import pandas as pd


class EMAIndicator(Indicator):
    def __init__(self, window: int, column: str = "Close"):
        self.window = window
        self.column = column

    def apply(self, data: pd.DataFrame) -> None:
        """
        Calculates the EMA for each symbol in the multi-index DataFrame and adds it as a new column.
        """
        for symbol in data.columns.get_level_values(0).unique():
            ema_column_name = f"EMA_{self.window}"
            data[(symbol, ema_column_name)] = data[(symbol, self.column)].ewm(span=self.window, adjust=False).mean()
