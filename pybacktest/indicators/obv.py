from matplotlib.pylab import f
import pandas as pd

from .indicator import Indicator


class OBVIndicator(Indicator):
    def init(self, column: str = "Close"):
        super().__init__()
        self.column = column
        self.indicator_name = "OBV"
        self.column_names.extend([self.indicator_name])

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            column = data[(symbol, self.column)]
            volume = data[(symbol, "Volume")]
            obv = volume.where(column.diff() > 0, -volume).cumsum()

            data[(symbol, self.indicator_name)] = obv
