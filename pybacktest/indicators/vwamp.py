import pandas as pd

from .indicator import Indicator

class VWAPIndicator(Indicator): 
    
    def init(self): 
        pass

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            price = data[(symbol, "Close")]
            volume = data[(symbol, "Volume")]

            cum_volume = volume.cumsum()
            cum_vwap = (price * volume).cumsum() / cum_volume

            data[(symbol, "VWAP")] = cum_vwap
