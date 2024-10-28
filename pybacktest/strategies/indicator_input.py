import pandas as pd

from ..indicators.indicator import Indicator


class IndicatorInput:
    def __init__(self, source, percentage=False, column_name=None):
        """
        :param source: Either an Indicator object, a column name (string), or a numeric value.
        :param percentage: If true, treats the value as a percentage of the indicator.
        :param column_name: Specify the column name if the Indicator generates multiple columns.
        """
        self.source = source
        self.percentage = percentage
        self.column_name = column_name

    def get_value(self, data: pd.Series) -> float:
        if isinstance(self.source, Indicator):
            if self.column_name:
                column_name = self.column_name
            elif len(self.source.column_names) == 1:
                column_name = self.source.column_names[0]
            else:
                raise ValueError(
                    f"Indicator {self.source} generates multiple columns; specify the column name."
                )
            base_value = data[column_name]
        elif isinstance(self.source, str):
            base_value = data[self.source]
        else:
            base_value = self.source
        return base_value * 0.01 if self.percentage else base_value
