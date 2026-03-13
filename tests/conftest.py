from datetime import datetime, timezone, timedelta

import polars as pl
import pytest


@pytest.fixture
def sample_snapshots() -> pl.DataFrame:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    rows = []
    for i in range(10):
        ts = start + timedelta(seconds=i)
        rows.append(
            {
                "market_id": "m1",
                "window_start_ts": start,
                "window_end_ts": start + timedelta(seconds=60),
                "snapshot_ts": ts,
                "tau_sec": 60 - i,
                "btc_ref_open": 100000.0,
                "btc_ref_now": 100000.0 + i,
                "btc_binance_now": 100000.0 + i,
                "up_bid": 0.48 + i * 0.001,
                "up_ask": 0.50 + i * 0.001,
                "down_bid": 0.49 - i * 0.001,
                "down_ask": 0.51 - i * 0.001,
                "up_mid": 0.49 + i * 0.001,
                "down_mid": 0.50 - i * 0.001,
                "spread_up": 0.02,
                "spread_down": 0.02,
            }
        )
    return pl.from_dicts(rows)
