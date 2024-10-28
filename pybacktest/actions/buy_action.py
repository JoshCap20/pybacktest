from .base import Action
from ..orders.order import Order
from ..portfolio import Portfolio

import pandas as pd


class BuyAction(Action):
    def __init__(self):
        super().__init__("Buy")

    def execute(self, data: pd.Series, context: dict) -> None:
        portfolio: Portfolio = context["portfolio"]
        symbol = context["symbol"]
        timeframe = context["timeframe"]
        price = data["Close"]

        quantity = self.calculate_quantity(portfolio, price)
        if quantity > 0:
            order = Order(symbol, quantity, price, "buy", timeframe)
            order.execute(portfolio)
            self.log_action(symbol, quantity, price)
