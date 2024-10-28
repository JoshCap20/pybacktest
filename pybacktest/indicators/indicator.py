import pandas as pd


class Indicator(object):
    def __init__(self):
        ## Subclasses must add any indicator column names to this list.
        self.column_names = []

    def apply(self, data: pd.DataFrame):
        """
        Calculates the indicator values for the given data and modifies the DataFrame.
        """
        raise NotImplementedError

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join(self.column_names)}"
