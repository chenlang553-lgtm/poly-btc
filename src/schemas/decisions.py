from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Decision(BaseModel):
    market_id: str
    snapshot_ts: datetime
    action: Literal["NO_TRADE", "BUY_STRONG", "BUY_WEAK"]
    edge_main: float
    edge_contra: float
    best_edge: float
    size: int
    reason: str
