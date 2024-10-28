import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Portfolio:
    brokerage_fee: float = 0.001  # 0.1%
    order_allocation: float = 0.1  # 10%

    def __init__(self, initial_cash: float):
        self.cash = initial_cash
        self.initial_cash = initial_cash
        self.positions = {}  # symbol -> quantity
        self.transaction_history = []  # List of transaction records

    def buy(self, symbol: str, quantity: float, price: float) -> None:
        total_cost = quantity * price * (1 + self.brokerage_fee)
        if self.cash >= total_cost:
            self.cash -= total_cost
            self.positions[symbol] = self.positions.get(symbol, 0) + quantity
            self.record_transaction("buy", symbol, quantity, price)
            logger.info(f"Bought {quantity} shares of {symbol} at {price}")
        else:
            logger.warning(
                f"Insufficient funds to buy {quantity} shares of {symbol} at {price}"
            )

    def sell(self, symbol: str, quantity: float, price: float) -> None:
        current_position = self.positions.get(symbol, 0)
        if current_position >= quantity:
            total_proceeds = quantity * price * (1 - self.brokerage_fee)
            self.cash += total_proceeds
            self.positions[symbol] -= quantity
            self.record_transaction("sell", symbol, quantity, price)
            logger.info(f"Sold {quantity} shares of {symbol} at {price}")
        else:
            logger.warning(
                f"Insufficient holdings to sell {quantity} shares of {symbol} at {price}"
            )

    def get_position(self, symbol: str) -> float:
        return self.positions.get(symbol, 0)

    def record_transaction(
        self, transaction_type: str, symbol: str, quantity: float, price: float
    ):
        transaction = {
            "type": transaction_type,
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "timestamp": datetime.now(),
            "cash_balance": self.cash,
        }
        self.transaction_history.append(transaction)

    def total_portfolio_value(self, current_prices: dict) -> float:
        total_value = self.cash
        for symbol, quantity in self.positions.items():
            price = current_prices.get(symbol, 0)
            total_value += quantity * price
        return total_value

    def print_positions(self):
        for symbol, quantity in self.positions.items():
            logger.info(f"Position in {symbol}: {quantity} shares")
