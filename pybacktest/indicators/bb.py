import pandas as pd

from .indicator import Indicator


class BollingerBands(Indicator):
    def __init__(self, window: int = 20, num_std_dev: float = 2, column: str = "Close"):
        super().__init__()
        self.window = window
        self.num_std_dev = num_std_dev
        self.column = column

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            sma = data[(symbol, self.column)].rolling(window=self.window).mean()
            std_dev = data[(symbol, self.column)].rolling(window=self.window).std()

            upper_band = sma + (self.num_std_dev * std_dev)
            lower_band = sma - (self.num_std_dev * std_dev)

            data[(symbol, f"Bollinger_Upper_{self.window}")] = upper_band
            data[(symbol, f"Bollinger_Lower_{self.window}")] = lower_band
            data[(symbol, f"Bollinger_SMA_{self.window}")] = sma
