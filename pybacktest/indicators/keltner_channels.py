import pandas as pd

from .indicator import Indicator


class KeltnerChannels(Indicator):

    def __init__(
        self, window: int = 20, multiplier: float = 2, column: str = "Adj Close"
    ):
        super().__init__()
        self.window = window
        self.multiplier = multiplier
        self.column = column

        self.keltner_upper_name = f"Keltner_Upper_{self.window}"
        self.keltner_lower_name = f"Keltner_Lower_{self.window}"
        self.keltner_center_name = f"Keltner_Center_{self.window}"

        self.column_names.extend(
            [self.keltner_upper_name, self.keltner_lower_name, self.keltner_center_name]
        )

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
                data[(symbol, self.keltner_upper_name)] = ema + self.multiplier * atr
                data[(symbol, self.keltner_lower_name)] = ema - self.multiplier * atr
            data[(symbol, self.keltner_center_name)] = ema
