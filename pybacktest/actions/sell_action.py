from .base import Action
from ..orders.order import Order
from ..portfolio import Portfolio

import pandas as pd


class SellAction(Action):
    def __init__(self):
        super().__init__("Sell")

    def execute(self, data: pd.Series, context: dict) -> None:
        portfolio: Portfolio = context["portfolio"]
        symbol = context["symbol"]
        price = data["Close"]
        timeframe = context["timeframe"]

        quantity = portfolio.get_position(symbol)

        # TODO: Does not support short selling currently
        if quantity > 0:
            order = Order(symbol, quantity, price, "sell", timeframe)
            order.execute(portfolio)
            self.log_action(symbol, quantity, price, timeframe)
