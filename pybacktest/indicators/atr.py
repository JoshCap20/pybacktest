import pandas as pd

from .indicator import Indicator


class ATRIndicator(Indicator):
    def __init__(self, window: int = 14):
        self.window = window

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            high = data[(symbol, "High")]
            low = data[(symbol, "Low")]
            close = data[(symbol, "Close")]

            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

            data[(symbol, f"ATR_{self.window}")] = true_range.rolling(
                window=self.window
            ).mean()
