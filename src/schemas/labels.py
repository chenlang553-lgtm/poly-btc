from datetime import datetime

from pydantic import BaseModel


class LabelRow(BaseModel):
    market_id: str
    snapshot_ts: datetime
    y_up: int
    y_cont: int
