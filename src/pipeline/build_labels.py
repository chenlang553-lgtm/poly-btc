import polars as pl


def build_labels(features: pl.DataFrame, outcomes: pl.DataFrame) -> pl.DataFrame:
    df = features.join(outcomes.select("market_id", "winner"), on="market_id", how="left")
    return df.select(
        "market_id",
        "snapshot_ts",
        pl.when(pl.col("winner") == "UP").then(1).otherwise(0).alias("y_up"),
        pl.when(pl.col("winner") == pl.col("strong_side")).then(1).otherwise(0).alias("y_cont"),
    )
