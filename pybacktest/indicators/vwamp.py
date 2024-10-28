import pandas as pd

from .indicator import Indicator


class VWAPIndicator(Indicator):

    def init(self, column: str = "Close"):
        self.column = column
        self.indicator_name = "VWAP"
        self.column_names.extend([self.indicator_name])

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            price = data[(symbol, self.column)]
            volume = data[(symbol, "Volume")]

            cum_volume = volume.cumsum()
            cum_vwap = (price * volume).cumsum() / cum_volume

            data[(symbol, self.indicator_name)] = cum_vwap
