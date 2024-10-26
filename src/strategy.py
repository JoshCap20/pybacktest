from typing import Callable
import pandas as pd
from .predicate_filter import PredicateFilter

"""
Basically a compound predicate with an action.
"""


class Strategy(PredicateFilter):
    _predicates: list[PredicateFilter] | PredicateFilter
    _action: Callable

    def __init__(
        self,
        predicates: list[PredicateFilter] | PredicateFilter,
        action: Callable = lambda x: x,
    ):
        self._predicates = predicates
        self._action = action

        if not isinstance(predicates, PredicateFilter) and not all(
            isinstance(subscriber, PredicateFilter) for subscriber in predicates
        ):
            raise ValueError("All predicates must be of type PredicateFilter")

        if not callable(action):
            raise ValueError("Action must be a callable")

    def test(self, row: pd.Series) -> bool:
        """
        Returns True if all predicates are true.
        """
        if isinstance(self._predicates, PredicateFilter):
            return self._predicates.test(row)
        return all(subscriber.test(row) for subscriber in self._predicates)

    def apply(self, row: pd.Series) -> None:
        """
        Called when all tests return True.

        Not required, will default to no action.
        """
        self._action(row)
