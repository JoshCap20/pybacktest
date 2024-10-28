from .predicate import Predicate
from ..actions import Action
from ..data.data_series import DataSeries

import pandas as pd


class Strategy:
    def __init__(
        self,
        entry_conditions: list[Predicate],
        entry_action: Action,
        exit_conditions: list[Predicate],
        exit_action: Action,
    ):
        self.entry_conditions = entry_conditions
        self.entry_action = entry_action
        self.exit_conditions = exit_conditions
        self.exit_action = exit_action

    def apply(self, data: DataSeries, context: dict) -> None:
        context["timeframe"] = data.get_date_index()

        for symbol in data.all_symbols():
            symbol_data: pd.Series = data.get_all(symbol)
            context["symbol"] = symbol
            if all(cond.test(symbol_data) for cond in self.entry_conditions):
                self.entry_action.execute(symbol_data, context)
            elif all(cond.test(symbol_data) for cond in self.exit_conditions):
                self.exit_action.execute(symbol_data, context)

    def __str__(self):
        return f"{self.__class__.__name__} with {len(self.entry_conditions)} entry conditions and {len(self.exit_conditions)} exit conditions"

    def as_dict(self) -> dict:
        return {
            "entry_conditions": [str(cond) for cond in self.entry_conditions],
            "entry_action": str(self.entry_action),
            "exit_conditions": [str(cond) for cond in self.exit_conditions],
            "exit_action": str(self.exit_action),
        }
