from __future__ import annotations

import polars as pl


def add_legacy_features(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        (pl.col("ask_weak") - 0.5).alias("weak_theta_gap"),
        (1 - pl.col("spread_strong")).clip(0, 1).alias("tail_confirmation_score"),
        pl.col("flip_count_5s").truediv(5).alias("recent_flips_signal"),
        (1 - pl.col("spread_weak")).clip(0, 1).alias("stability_signal"),
    )
