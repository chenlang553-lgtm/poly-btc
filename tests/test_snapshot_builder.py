from datetime import datetime, timezone, timedelta

import polars as pl

from pipeline.build_snapshots import build_1s_snapshots


def test_build_snapshots_aligns_tau() -> None:
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    events = pl.from_dicts(
        [
            {
                "market_id": "m1",
                "event_ts": start,
                "up_bid": 0.49,
                "up_ask": 0.51,
                "down_bid": 0.49,
                "down_ask": 0.51,
                "btc_ref": 100000.0,
                "btc_binance": 100010.0,
            }
        ]
    )
    windows = pl.from_dicts(
        [{"market_id": "m1", "window_start_ts": start, "window_end_ts": start + timedelta(seconds=2)}]
    )
    out = build_1s_snapshots(events, windows)
    assert out.height == 3
    assert out.get_column("tau_sec").to_list() == [2, 1, 0]
