import pandas as pd

from .indicator import Indicator

class OBVIndicator(Indicator): 
    def init(self): 
        pass

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            close = data[(symbol, "Close")]
            volume = data[(symbol, "Volume")]
            obv = volume.where(close.diff() > 0, -volume).cumsum()

            data[(symbol, "OBV")] = obv