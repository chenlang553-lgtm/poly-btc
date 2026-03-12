import polars as pl

from pipeline.build_labels import build_labels


def test_labels_use_current_strong_side(sample_snapshots) -> None:
    features = sample_snapshots.with_columns(pl.lit("UP").alias("strong_side"))
    outcomes = pl.from_dicts([{"market_id": "m1", "winner": "UP"}])
    labels = build_labels(features, outcomes)
    assert labels.select("y_cont").to_series().sum() == labels.height
