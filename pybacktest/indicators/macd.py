import pandas as pd

from .indicator import Indicator


class MACDIndicator(Indicator):

    def __init__(
        self,
        short_window: int = 12,
        long_window: int = 26,
        signal_window: int = 9,
        column: str = "Adj Close",
    ):
        super().__init__()
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window
        self.column = column

        self.macd_line_name = f"MACD_{self.short_window}_{self.long_window}"
        self.signal_line_name = f"MACD_Signal_{self.signal_window}"
        self.histogram_name = "MACD_Histogram"

        self.column_names.extend(
            [self.macd_line_name, self.signal_line_name, self.histogram_name]
        )

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

            data[(symbol, self.macd_line_name)] = macd_line
            data[(symbol, self.signal_line_name)] = signal_line
            data[(symbol, self.histogram_name)] = macd_histogram
