from datetime import datetime

from schemas.decisions import Decision
from strategy.risk_rules import RiskState, passes_risk
from strategy.sizing import discrete_size


def route_decision(
    *,
    market_id: str,
    snapshot_ts: datetime,
    p_cont: float,
    ask_strong: float,
    ask_weak: float,
    spread_strong: float,
    spread_weak: float,
    tau_sec: int,
    min_edge: float,
    state: RiskState,
    entry_min_sec: int,
    entry_max_sec: int,
    max_spread: float,
    daily_loss_cap: float,
    max_consecutive_losses: int,
) -> Decision:
    edge_main = p_cont - ask_strong
    edge_contra = (1.0 - p_cont) - ask_weak
    best_edge = max(edge_main, edge_contra)

    if best_edge <= min_edge:
        return Decision(
            market_id=market_id,
            snapshot_ts=snapshot_ts,
            action="NO_TRADE",
            edge_main=edge_main,
            edge_contra=edge_contra,
            best_edge=best_edge,
            size=0,
            reason="edge",
        )

    action = "BUY_STRONG" if edge_main > edge_contra else "BUY_WEAK"
    ask = ask_strong if action == "BUY_STRONG" else ask_weak
    allowed, reason = passes_risk(
        side=action,
        ask_strong=ask_strong,
        ask_weak=ask_weak,
        spread_strong=spread_strong,
        spread_weak=spread_weak,
        tau_sec=tau_sec,
        state=state,
        entry_min_sec=entry_min_sec,
        entry_max_sec=entry_max_sec,
        max_spread=max_spread,
        daily_loss_cap=daily_loss_cap,
        max_consecutive_losses=max_consecutive_losses,
    )
    if not allowed:
        action = "NO_TRADE"
        size = 0
    else:
        size = discrete_size(best_edge, ask)
        if size == 0:
            action = "NO_TRADE"
            reason = "size"

    return Decision(
        market_id=market_id,
        snapshot_ts=snapshot_ts,
        action=action,
        edge_main=edge_main,
        edge_contra=edge_contra,
        best_edge=best_edge,
        size=size,
        reason=reason,
    )
