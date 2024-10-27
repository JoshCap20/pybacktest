import pandas as pd

from .indicator import Indicator


class MACDIndicator(Indicator):
    def __init__(
        self,
        short_window: int = 12,
        long_window: int = 26,
        signal_window: int = 9,
        column: str = "Close",
    ):
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window
        self.column = column

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            ema_short = (
                data[(symbol, self.column)]
                .ewm(span=self.short_window, adjust=False)
                .mean()
            )
            ema_long = (
                data[(symbol, self.column)]
                .ewm(span=self.long_window, adjust=False)
                .mean()
            )

            macd_line = ema_short - ema_long
            signal_line = macd_line.ewm(span=self.signal_window, adjust=False).mean()
            macd_histogram = macd_line - signal_line

            data[(symbol, f"MACD_{self.short_window}_{self.long_window}")] = macd_line
            data[(symbol, f"MACD_Signal_{self.signal_window}")] = signal_line
            data[(symbol, "MACD_Histogram")] = macd_histogram
