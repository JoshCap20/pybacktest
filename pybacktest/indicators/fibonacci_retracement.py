import pandas as pd

from .indicator import Indicator


class FibonacciRetracementLevels(Indicator):

    def __init__(self, column: str = "Adj Close"):
        super().__init__()
        self.column = column
        self.column_names = ["Fib_23.6%", "Fib_38.2%", "Fib_50%", "Fib_61.8%"]

    def apply(self, data: pd.DataFrame) -> None:
        for symbol in data.columns.get_level_values(0).unique():
            column = data[(symbol, self.column)]
            high = data[(symbol, "High")]
            low = data[(symbol, "Low")]
            diff = high - low
            data[(symbol, "Fib_23.6%")] = column - diff * 0.236
            data[(symbol, "Fib_38.2%")] = column - diff * 0.382
            data[(symbol, "Fib_50%")] = column - diff * 0.5
            data[(symbol, "Fib_61.8%")] = column - diff * 0.618
