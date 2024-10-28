from ..portfolio import Portfolio
from ..orders.order import Order

import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
logger.propagate = False


class Action:
    def __init__(self, action_type: str):
        self.action_type = action_type

    def execute(self, data: pd.Series, context: dict) -> None:
        portfolio: Portfolio = context["portfolio"]
        # TODO: refactor this to access the data in a more generic way
        symbol = context["symbol"]
        price = data["Close"]
        timestamp = context["timeframe"]

        order: Order | None = None
        amount: float = 0.0
        if self.action_type == "Buy":
            amount = self.calculate_quantity(portfolio, price)
            order = Order(symbol, amount, price, "buy", timestamp)
        elif self.action_type == "Sell":
            amount = portfolio.get_position(symbol)
            order = Order(symbol, amount, price, "sell", timestamp)
        else:
            raise ValueError(f"Unknown action type: {self.action_type}")

        if order:
            order.execute(portfolio)
            self.log_action(symbol, amount, price, timestamp)
        raise NotImplementedError("Implement the execute method in a subclass")

    def calculate_quantity(self, portfolio: Portfolio, price: float) -> float:
        allocation = portfolio.cash * portfolio.order_allocation
        quantity = allocation // price
        return quantity

    def log_action(
        self, symbol: str, amount: float, price: float, timestamp: pd.Timestamp
    ) -> None:
        logger.info(
            f"{timestamp}: {self.action_type} {amount} shares of {symbol} at {price}"
        )

    def __str__(self):
        return self.action_type
