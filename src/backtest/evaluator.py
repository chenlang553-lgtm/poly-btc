import numpy as np
import polars as pl
from sklearn.metrics import brier_score_loss, log_loss


def evaluate_probabilities(y_true: np.ndarray, p_pred: np.ndarray) -> dict[str, float]:
    return {
        "brier": float(brier_score_loss(y_true, p_pred)),
        "log_loss": float(log_loss(y_true, np.clip(p_pred, 1e-6, 1 - 1e-6))),
    }


def evaluate_trades(trades: pl.DataFrame) -> dict[str, float]:
    if trades.is_empty():
        return {"total_pnl": 0.0, "hit_rate": 0.0}
    pnl = trades.get_column("pnl") if "pnl" in trades.columns else pl.Series([0.0] * trades.height)
    wins = (pnl > 0).sum()
    return {
        "total_pnl": float(pnl.sum()),
        "hit_rate": float(wins / max(1, trades.height)),
    }
