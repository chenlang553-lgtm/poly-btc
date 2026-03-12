from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import polars as pl


def save_calibration_plot(df: pl.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 4))
    plt.plot([0, 1], [0, 1], "k--", label="ideal")
    plt.scatter(df["p_pred"], df["y_true"], s=8, alpha=0.4, label="obs")
    plt.xlabel("Predicted p_cont")
    plt.ylabel("Observed y_cont")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)


def save_z_curve(df: pl.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    z = df["z"].to_numpy()
    y = df["y_cont"].to_numpy()
    bins = np.linspace(z.min(), z.max(), 20)
    ids = np.digitize(z, bins)
    x_pts = [z[ids == i].mean() for i in range(1, len(bins)) if np.any(ids == i)]
    y_pts = [y[ids == i].mean() for i in range(1, len(bins)) if np.any(ids == i)]
    plt.figure(figsize=(6, 4))
    plt.plot(x_pts, y_pts, marker="o")
    plt.xlabel("z")
    plt.ylabel("Empirical P(y_cont=1)")
    plt.tight_layout()
    plt.savefig(path)


def save_edge_bucket_plot(df: pl.DataFrame, edge_col: str, pnl_col: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bucketed = df.with_columns(pl.col(edge_col).cut([-1, 0, 0.02, 0.04, 0.07, 1]).alias("bucket"))
    agg = bucketed.group_by("bucket").agg(pl.col(pnl_col).mean().alias("ev")).sort("bucket")
    plt.figure(figsize=(6, 4))
    plt.bar(agg["bucket"].cast(pl.String), agg["ev"])
    plt.xticks(rotation=45)
    plt.ylabel("EV")
    plt.tight_layout()
    plt.savefig(path)


def generate_required_reports(df: pl.DataFrame, out_dir: Path) -> None:
    save_z_curve(df, out_dir / "z_vs_empirical_pcont.png")
    save_calibration_plot(df.select("p_pred", "y_true"), out_dir / "calibration.png")
    if {"edge_main", "pnl"}.issubset(set(df.columns)):
        save_edge_bucket_plot(df, "edge_main", "pnl", out_dir / "ev_edge_main.png")
    if {"edge_contra", "pnl"}.issubset(set(df.columns)):
        save_edge_bucket_plot(df, "edge_contra", "pnl", out_dir / "ev_edge_contra.png")
