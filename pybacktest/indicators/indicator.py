import pandas as pd


class Indicator(object):
    def apply(self, data: pd.DataFrame) -> pd.Series:
        """
        Calculates the indicator values for the given data and returns a Series.
        """
        raise NotImplementedError
