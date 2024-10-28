import pandas as pd

from .indicator import Indicator


class BollingerBands(Indicator):

    def __init__(
        self, window: int = 20, num_std_dev: float = 2, column: str = "Adj Close"
    ):
        super().__init__()
        self.window = window
        self.num_std_dev = num_std_dev
        self.column = column

        self.lower_band_name = f"Bollinger_Lower_{self.window}"
        self.upper_band_name = f"Bollinger_Upper_{self.window}"
        self.sma_name = f"Bollinger_SMA_{self.window}"

        self.column_names.extend(
            [self.lower_band_name, self.upper_band_name, self.sma_name]
        )

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            sma = data[(symbol, self.column)].rolling(window=self.window).mean()
            std_dev = data[(symbol, self.column)].rolling(window=self.window).std()

            upper_band = sma + (self.num_std_dev * std_dev)
            lower_band = sma - (self.num_std_dev * std_dev)

            data[(symbol, self.sma_name)] = sma
            data[(symbol, self.upper_band_name)] = upper_band
            data[(symbol, self.lower_band_name)] = lower_band
