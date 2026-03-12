from datetime import datetime

from pydantic import BaseModel


class FeatureRow(BaseModel):
    market_id: str
    snapshot_ts: datetime
    tau_sec: int
    x: float
    sigma_hat_sec: float
    z: float
    strong_side: str
    weak_side: str
    ask_strong: float
    ask_weak: float
    mid_strong: float
    mid_weak: float
    spread_strong: float
    spread_weak: float
    price_gap: float
    strong_slope_1s: float
    strong_slope_3s: float
    strong_slope_5s: float
    weak_slope_1s: float
    weak_slope_3s: float
    weak_slope_5s: float
    strong_accel: float
    weak_accel: float
    flip_count_5s: int
    btc_ret_1s: float
    btc_ret_3s: float
    btc_ret_5s: float
    btc_accel_3s: float
    dist_to_open_abs: float
    dist_to_open_signed: float
    weak_theta_gap: float
    tail_confirmation_score: float
    recent_flips_signal: float
    stability_signal: float
    mispricing_strong: float = 0.0
