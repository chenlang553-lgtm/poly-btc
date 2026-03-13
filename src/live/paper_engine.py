from dataclasses import dataclass, field
from datetime import datetime

from schemas.decisions import Decision


@dataclass(slots=True)
class PaperTrade:
    ts: datetime
    market_id: str
    action: str
    price: float
    shares: int


@dataclass(slots=True)
class PaperEngine:
    trades: list[PaperTrade] = field(default_factory=list)

    def execute(self, decision: Decision, price: float) -> None:
        if decision.action == "NO_TRADE" or decision.size <= 0:
            return
        self.trades.append(
            PaperTrade(
                ts=decision.snapshot_ts,
                market_id=decision.market_id,
                action=decision.action,
                price=price,
                shares=decision.size,
            )
        )
