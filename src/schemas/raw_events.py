from datetime import datetime
from typing import Any

from pydantic import BaseModel


class RawEvent(BaseModel):
    source: str
    event_type: str
    exchange_ts: datetime | None = None
    received_ts: datetime
    market_id: str | None = None
    payload: dict[str, Any]
