import pandas as pd

from .indicator import Indicator

class KeltnerChannels(Indicator):
 def __init__(self, window: int = 20, multiplier: float = 2, column: str = "Close"):
     self.window = window
     self.multiplier = multiplier
     self.column = column

 def apply(self, data: pd.DataFrame) -> None:
     for symbol in data.columns.get_level_values(0).unique():
         ema = data[(symbol, self.column)].ewm(span=self.window, adjust=False).mean()
         atr = data[(symbol, f"ATR_{self.window}")]  # Ensure ATR is precomputed

         data[(symbol, f"Keltner_Upper_{self.window}")] = ema + self.multiplier * atr
         data[(symbol, f"Keltner_Lower_{self.window}")] = ema - self.multiplier * atr
         data[(symbol, f"Keltner_Center_{self.window}")] = ema