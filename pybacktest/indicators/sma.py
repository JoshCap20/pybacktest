from .indicator import Indicator
import pandas as pd


class SMAIndicator(Indicator):
    def __init__(self, window: int, column: str = "Close"):
        super().__init__()
        self.window = window
        self.column = column
        self.indicator_name = f"SMA_{self.window}"
        self.column_names.append(self.indicator_name)

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            data[(symbol, self.indicator_name)] = (
                data[(symbol, self.column)].rolling(window=self.window).mean()
            )
