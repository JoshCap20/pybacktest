import pandas as pd


class PredicateFilter(object):
    """
    Base class for all subscribers.
    """

    def test(self, row: pd.Series) -> bool:
        """
        Determines if a certain condition is met on the row data.
        """
        raise NotImplementedError
