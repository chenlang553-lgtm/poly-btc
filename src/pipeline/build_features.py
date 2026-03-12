import numpy as np
import polars as pl


def build_features(snapshots: pl.DataFrame, theta: float = 0.5) -> pl.DataFrame:
    df = snapshots.sort(["market_id", "snapshot_ts"]).with_columns(
        pl.when(pl.col("up_mid") >= pl.col("down_mid")).then(pl.lit("UP")).otherwise(pl.lit("DOWN")).alias("strong_side"),
    )

    df = df.with_columns(
        pl.when(pl.col("strong_side") == "UP").then(pl.col("up_ask")).otherwise(pl.col("down_ask")).alias("ask_strong"),
        pl.when(pl.col("strong_side") == "UP").then(pl.col("down_ask")).otherwise(pl.col("up_ask")).alias("ask_weak"),
        pl.when(pl.col("strong_side") == "UP").then(pl.col("up_mid")).otherwise(pl.col("down_mid")).alias("mid_strong"),
        pl.when(pl.col("strong_side") == "UP").then(pl.col("down_mid")).otherwise(pl.col("up_mid")).alias("mid_weak"),
        pl.when(pl.col("strong_side") == "UP").then(pl.col("spread_up")).otherwise(pl.col("spread_down")).alias("spread_strong"),
        pl.when(pl.col("strong_side") == "UP").then(pl.col("spread_down")).otherwise(pl.col("spread_up")).alias("spread_weak"),
        pl.when(pl.col("strong_side") == "UP").then(pl.lit("DOWN")).otherwise(pl.lit("UP")).alias("weak_side"),
    )

    x = np.log((df["btc_ref_now"] / df["btc_ref_open"]).to_numpy())
    df = df.with_columns(pl.Series("x", x))
    df = df.with_columns(
        pl.col("btc_ref_now").log().diff().over("market_id").alias("btc_ret_1s"),
        pl.col("btc_ref_now").log().diff(3).over("market_id").alias("btc_ret_3s"),
        pl.col("btc_ref_now").log().diff(5).over("market_id").alias("btc_ret_5s"),
        pl.col("mid_strong").diff().over("market_id").alias("strong_slope_1s"),
        pl.col("mid_strong").diff(3).over("market_id").alias("strong_slope_3s"),
        pl.col("mid_strong").diff(5).over("market_id").alias("strong_slope_5s"),
        pl.col("mid_weak").diff().over("market_id").alias("weak_slope_1s"),
        pl.col("mid_weak").diff(3).over("market_id").alias("weak_slope_3s"),
        pl.col("mid_weak").diff(5).over("market_id").alias("weak_slope_5s"),
    ).with_columns(
        pl.col("strong_slope_1s").diff().over("market_id").alias("strong_accel"),
        pl.col("weak_slope_1s").diff().over("market_id").alias("weak_accel"),
        pl.col("btc_ret_3s").diff().over("market_id").alias("btc_accel_3s"),
    )

    df = df.with_columns(
        pl.col("btc_ret_1s").rolling_std(window_size=30, min_periods=5).over("market_id").alias("sigma_hat_sec"),
    )

    safe_tau = pl.when(pl.col("tau_sec") > 0).then(pl.col("tau_sec")).otherwise(1)
    df = df.with_columns(
        (pl.col("x") / (pl.col("sigma_hat_sec").fill_null(1e-6) * safe_tau.sqrt())).alias("z"),
        (pl.col("mid_strong") - pl.col("mid_weak")).alias("price_gap"),
        pl.col("strong_side").neq(pl.col("strong_side").shift()).cast(pl.Int8).rolling_sum(5).over("market_id").alias("flip_count_5s"),
        pl.col("x").abs().alias("dist_to_open_abs"),
        pl.col("x").alias("dist_to_open_signed"),
        (pl.col("ask_weak") - theta).alias("weak_theta_gap"),
        (1 - pl.col("spread_strong")).clip(0, 1).alias("tail_confirmation_score"),
        pl.col("flip_count_5s").fill_null(0).truediv(5).alias("recent_flips_signal"),
        (1 - pl.col("spread_weak")).clip(0, 1).alias("stability_signal"),
    )

    return df.fill_null(0.0)
