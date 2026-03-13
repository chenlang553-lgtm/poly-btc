from typing import Protocol


class OrderInterface(Protocol):
    def place_buy(self, market_id: str, token: str, price: float, shares: int) -> str: ...
