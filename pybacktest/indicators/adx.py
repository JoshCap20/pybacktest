from typing import List
import pandas as pd

from .indicator import Indicator


class ADXIndicator(Indicator):
    def __init__(self, window: int = 14):
        self.window = window
        self.indicator_name = f"ADX_{self.window}"
        self.column_names.append(self.indicator_name)

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            high = data[(symbol, "High")]
            low = data[(symbol, "Low")]
            close = data[(symbol, "Close")]

            plus_dm = high.diff()
            minus_dm = low.diff()

            plus_dm[plus_dm < 0] = 0
            minus_dm[minus_dm > 0] = 0

            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

            atr = tr.rolling(window=self.window).mean()
            plus_di = 100 * (plus_dm.ewm(alpha=1 / self.window).mean() / atr)
            minus_di = 100 * (minus_dm.ewm(alpha=1 / self.window).mean() / atr)
            dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
            adx = dx.rolling(window=self.window).mean()

            data[(symbol, self.indicator_name)] = adx
