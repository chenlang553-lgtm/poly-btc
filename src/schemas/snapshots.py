from datetime import datetime

from pydantic import BaseModel


class Snapshot(BaseModel):
    market_id: str
    window_start_ts: datetime
    window_end_ts: datetime
    snapshot_ts: datetime
    tau_sec: int
    btc_ref_open: float
    btc_ref_now: float
    btc_binance_now: float | None = None
    up_bid: float
    up_ask: float
    down_bid: float
    down_ask: float
    up_mid: float
    down_mid: float
    spread_up: float
    spread_down: float
