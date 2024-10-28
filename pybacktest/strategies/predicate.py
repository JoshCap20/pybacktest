import pandas as pd
from typing import Union, Optional, Callable
from .indicator_input import IndicatorInput
from ..indicators import Indicator

class Predicate:

    def __init__(
        self,
        input1: Union[IndicatorInput, Indicator, str, float, "Predicate"],
        operator: Optional[Callable[[float, float], bool]] = None,
        input2: Optional[Union[IndicatorInput, Indicator, str, float]] = None,
        threshold: Optional[float] = None,
        negate: bool = False,
    ):
        self.input1 = self._ensure_indicator_input(input1)
        self.operator = operator
        self.input2 = (
            self._ensure_indicator_input(input2) if input2 is not None else None
        )
        self.threshold = threshold
        self.negate = negate
        self.is_combined = False
        self.left = None
        self.right = None
        self.logic_operator = None

    def _ensure_indicator_input(self, input_value):
        if isinstance(input_value, Predicate):
            return input_value
        elif isinstance(input_value, IndicatorInput):
            return input_value
        else:
            return IndicatorInput(input_value)

    def test(self, data: pd.Series) -> bool:
        if self.is_combined:
            left_result = self.left.test(data)
            right_result = self.right.test(data)
            if self.logic_operator == "and":
                result = left_result and right_result
            elif self.logic_operator == "or":
                result = left_result or right_result
            else:
                raise ValueError("Invalid logic operator.")
        else:
            if isinstance(self.input1, Predicate):
                value1 = self.input1.test(data)
            else:
                value1 = self.input1.get_value(data)
            if self.input2 is not None:
                if isinstance(self.input2, Predicate):
                    value2 = self.input2.test(data)
                else:
                    value2 = self.input2.get_value(data)
                result = self.operator(value1, value2)
            elif self.threshold is not None:
                result = self.operator(value1, self.threshold)
            else:
                raise ValueError("Predicate requires a second input or a threshold.")

        return not result if self.negate else result

    def __invert__(self):
        return Predicate(
            input1=self.input1,
            operator=self.operator,
            input2=self.input2,
            threshold=self.threshold,
            negate=not self.negate,
        )

    def __and__(self, other):
        combined = Predicate(input1=self)
        combined.is_combined = True
        combined.left = self
        combined.right = other
        combined.logic_operator = "and"
        return combined

    def __or__(self, other):
        combined = Predicate(input1=self)
        combined.is_combined = True
        combined.left = self
        combined.right = other
        combined.logic_operator = "or"
        return combined

    def __str__(self):
        if self.is_combined:
            return f"({self.left} {self.logic_operator.upper()} {self.right})"
        else:
            base_str = f"{self.input1} {self.operator.__name__} {self.input2 or self.threshold}"
            return f"NOT ({base_str})" if self.negate else base_str
