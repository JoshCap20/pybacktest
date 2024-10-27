import pandas as pd

from .indicator import Indicator


class KeltnerChannels(Indicator):
    def __init__(self, window: int = 20, multiplier: float = 2, column: str = "Close"):
        self.window = window
        self.multiplier = multiplier
        self.column = column

    def apply(self, data: pd.DataFrame) -> None:
        # TODO: Add validation that ATR window is same as Keltner window
        for symbol in data.columns.get_level_values(0).unique():
            ema = data[(symbol, self.column)].ewm(span=self.window, adjust=False).mean()

            atr = None
            if (symbol, f"ATR_{self.window}") in data.columns:
                atr = data[(symbol, f"ATR_{self.window}")]
            else:
                # Search for any ATR indicator in the DataFrame
                for column in data.columns:
                    print(
                        f"No ATR with same window as KeltnerChannels found for {symbol}"
                    )
                    if "ATR" in column[1]:
                        atr = data[column]
                        break

            if atr is not None:
                data[(symbol, f"Keltner_Upper_{self.window}")] = (
                    ema + self.multiplier * atr
                )
                data[(symbol, f"Keltner_Lower_{self.window}")] = (
                    ema - self.multiplier * atr
                )
            data[(symbol, f"Keltner_Center_{self.window}")] = ema
