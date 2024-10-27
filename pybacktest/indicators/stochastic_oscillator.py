import pandas as pd

from .indicator import Indicator


class StochasticOscillator(Indicator):
    def __init__(self, k_window: int = 14, d_window: int = 3):
        self.k_window = k_window
        self.d_window = d_window

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            low_min = data[(symbol, "Low")].rolling(window=self.k_window).min()
            high_max = data[(symbol, "High")].rolling(window=self.k_window).max()
            k_percent = 100 * (
                (data[(symbol, "Close")] - low_min) / (high_max - low_min)
            )

            data[(symbol, f"%K_{self.k_window}")] = k_percent
            data[(symbol, f"%D_{self.d_window}")] = k_percent.rolling(
                window=self.d_window
            ).mean()
