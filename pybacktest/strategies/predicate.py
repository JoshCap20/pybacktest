from typing import Optional, Callable, Union, Any
import pandas as pd

from .indicator_input import IndicatorInput
from ..indicators import Indicator
from ..data.data_series import DataSeries


class Predicate:
    def __init__(
        self,
        input1: Union[IndicatorInput, Indicator, str, float],
        operator: Callable[[float, float], bool],
        input2: Optional[Union[IndicatorInput, Indicator, str, float]] = None,
        threshold: Optional[float] = None,
    ):
        """
        :param input1: Primary input for comparison.
        :param operator: Comparison function (e.g., operator.gt for >).
        :param input2: Optional second input for dynamic comparisons.
        :param threshold: Optional threshold for static comparisons.
        """
        self.input1 = self._ensure_indicator_input(input1)
        self.operator = operator
        self.input2 = (
            self._ensure_indicator_input(input2) if input2 is not None else None
        )
        self.threshold = threshold

    def _ensure_indicator_input(self, input_value, **kwargs):
        if isinstance(input_value, IndicatorInput):
            return input_value
        else:
            return IndicatorInput(input_value, **kwargs)

    def test(self, data: pd.Series) -> bool:
        """
        Tests the predicate against the data.
        """
        value1 = self.input1.get_value(data)
        if self.input2:
            value2 = self.input2.get_value(data)
            return self.operator(value1, value2)
        elif self.threshold is not None:
            return self.operator(value1, self.threshold)
        else:
            raise ValueError(
                "Predicate requires either a second input or a threshold for comparison."
            )

    def __str__(self):
        return f"{self.input1} {self.operator.__name__} {self.input2 or self.threshold}"
