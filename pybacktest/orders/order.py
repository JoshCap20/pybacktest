from datetime import datetime
from ..portfolio import Portfolio


class Order(object):
    def __init__(self, symbol: str, quantity: float, price: float, order_type: str):
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.order_type = order_type  # 'buy' or 'sell'
        self.timestamp = datetime.now()

    def execute(self, portfolio: Portfolio):
        if self.order_type == "buy":
            portfolio.buy(self.symbol, self.quantity, self.price)
        elif self.order_type == "sell":
            portfolio.sell(self.symbol, self.quantity, self.price)
        else:
            raise ValueError(f"Invalid order type: {self.order_type}")

    def __eq__(self, other: "Order"):
        if not isinstance(other, Order):
            return False
        return (
            self.symbol == other.symbol
            and self.quantity == other.quantity
            and self.price == other.price
            and self.order_type == other.order_type
        )

    def __str__(self):
        return f"Order({self.symbol}, {self.quantity}, {self.price}, {self.order_type})"
