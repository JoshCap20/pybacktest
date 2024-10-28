import pandas as pd

from .indicator import Indicator


class RSIIndicator(Indicator):

    def __init__(self, window: int = 14, column: str = "Adj Close"):
        super().__init__()
        self.window = window
        self.column = column

        self.indicator_name = f"RSI_{self.window}"
        self.column_names.extend([self.indicator_name])

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            delta = data[(symbol, self.column)].diff()
            gain = delta.where(delta.astype(float) > 0, 0.0)
            loss = -delta.where(delta.astype(float) < 0, 0.0)

            avg_gain = gain.rolling(window=self.window, min_periods=self.window).mean()
            avg_loss = loss.rolling(window=self.window, min_periods=self.window).mean()

            rs = avg_gain / avg_loss
            data[(symbol, self.indicator_name)] = 100 - (100 / (1 + rs))
