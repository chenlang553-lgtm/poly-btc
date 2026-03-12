from pathlib import Path

import polars as pl


RAW_SCHEMA = {
    "source": pl.String,
    "event_type": pl.String,
    "exchange_ts": pl.Datetime(time_zone="UTC"),
    "received_ts": pl.Datetime(time_zone="UTC"),
    "market_id": pl.String,
    "payload": pl.Struct,
}


def load_raw_events(path: Path) -> pl.DataFrame:
    return pl.read_ndjson(path, schema=RAW_SCHEMA)


def to_bronze(raw_df: pl.DataFrame) -> pl.DataFrame:
    return raw_df.with_columns(
        pl.coalesce([pl.col("exchange_ts"), pl.col("received_ts")]).alias("event_ts")
    ).sort(["market_id", "event_ts"])
