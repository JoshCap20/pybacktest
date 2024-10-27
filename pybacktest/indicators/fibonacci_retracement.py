import pandas as pd

from .indicator import Indicator

class FibonacciRetracementLevels(Indicator):
 def apply(self, data: pd.DataFrame) -> None:
     for symbol in data.columns.get_level_values(0).unique():
         high = data[(symbol, "High")].max()
         low = data[(symbol, "Low")].min()

         data[(symbol, "Fib_23.6%")] = high - (high - low) * 0.236
         data[(symbol, "Fib_38.2%")] = high - (high - low) * 0.382
         data[(symbol, "Fib_50%")] = high - (high - low) * 0.5
         data[(symbol, "Fib_61.8%")] = high - (high - low) * 0.618