from datetime import datetime

from pydantic import BaseModel


class Fill(BaseModel):
    market_id: str
    ts: datetime
    side: str
    price: float
    shares: int
    latency_ms: int
    slippage: float
