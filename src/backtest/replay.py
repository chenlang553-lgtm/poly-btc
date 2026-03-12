from dataclasses import dataclass

import polars as pl

from backtest.fill_model import simulate_fill
from strategy.continuation_router import route_decision
from strategy.risk_rules import RiskState


@dataclass(slots=True)
class ReplayConfig:
    min_edge: float = 0.02
    entry_min_sec: int = 3
    entry_max_sec: int = 120
    max_spread: float = 0.08
    daily_loss_cap: float = 100.0
    max_consecutive_losses: int = 5


def run_replay(snapshots: pl.DataFrame, p_cont_col: str, config: ReplayConfig) -> pl.DataFrame:
    records: list[dict[str, object]] = []
    state = RiskState()
    for row in snapshots.sort("snapshot_ts").iter_rows(named=True):
        decision = route_decision(
            market_id=row["market_id"],
            snapshot_ts=row["snapshot_ts"],
            p_cont=float(row[p_cont_col]),
            ask_strong=float(row["ask_strong"]),
            ask_weak=float(row["ask_weak"]),
            spread_strong=float(row["spread_strong"]),
            spread_weak=float(row["spread_weak"]),
            tau_sec=int(row["tau_sec"]),
            min_edge=config.min_edge,
            state=state,
            entry_min_sec=config.entry_min_sec,
            entry_max_sec=config.entry_max_sec,
            max_spread=config.max_spread,
            daily_loss_cap=config.daily_loss_cap,
            max_consecutive_losses=config.max_consecutive_losses,
        )
        record = decision.model_dump()
        if decision.action in {"BUY_STRONG", "BUY_WEAK"} and decision.size > 0:
            state.has_position_in_window = True
            fill = simulate_fill(
                market_id=row["market_id"],
                ts=row["snapshot_ts"],
                side="BUY",
                ask=float(row["ask_strong"] if decision.action == "BUY_STRONG" else row["ask_weak"]),
                bid=float(row["up_bid"]),
                shares=decision.size,
            )
            record["fill_price"] = fill.price
        records.append(record)
    return pl.from_dicts(records)
