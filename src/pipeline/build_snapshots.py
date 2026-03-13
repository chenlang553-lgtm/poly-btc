from datetime import timedelta

import polars as pl


def build_1s_snapshots(events: pl.DataFrame, market_windows: pl.DataFrame) -> pl.DataFrame:
    windows = market_windows.with_columns(
        pl.int_range(pl.len()).alias("window_idx")
    )
    grid_rows: list[dict[str, object]] = []
    for row in windows.iter_rows(named=True):
        ts = row["window_start_ts"]
        end = row["window_end_ts"]
        assert ts is not None and end is not None
        while ts <= end:
            grid_rows.append({"window_idx": row["window_idx"], "snapshot_ts": ts})
            ts += timedelta(seconds=1)
    grid = pl.from_dicts(grid_rows)

    quotes = events.select(
        "market_id",
        pl.col("event_ts").alias("quote_ts"),
        "up_bid",
        "up_ask",
        "down_bid",
        "down_ask",
        "btc_ref",
        "btc_binance",
    )

    joined = (
        grid.join(windows, on="window_idx", how="left")
        .join_asof(
            quotes.sort("quote_ts"),
            left_on="snapshot_ts",
            right_on="quote_ts",
            by="market_id",
            strategy="backward",
        )
        .with_columns(
            (pl.col("window_end_ts").dt.epoch("s") - pl.col("snapshot_ts").dt.epoch("s")).alias(
                "tau_sec"
            ),
            ((pl.col("up_bid") + pl.col("up_ask")) / 2).alias("up_mid"),
            ((pl.col("down_bid") + pl.col("down_ask")) / 2).alias("down_mid"),
            (pl.col("up_ask") - pl.col("up_bid")).alias("spread_up"),
            (pl.col("down_ask") - pl.col("down_bid")).alias("spread_down"),
        )
    )

    open_ref = joined.group_by(["market_id", "window_idx"]).agg(
        pl.col("btc_ref").first().alias("btc_ref_open")
    )

    return joined.join(open_ref, on=["market_id", "window_idx"], how="left").rename(
        {"btc_ref": "btc_ref_now", "btc_binance": "btc_binance_now"}
    )
