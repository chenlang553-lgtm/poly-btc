from strategy.continuation_router import route_decision
from strategy.risk_rules import RiskState


def process_snapshot(snapshot: dict[str, float | int | str], p_cont: float, risk_state: RiskState):
    return route_decision(
        market_id=str(snapshot["market_id"]),
        snapshot_ts=snapshot["snapshot_ts"],
        p_cont=p_cont,
        ask_strong=float(snapshot["ask_strong"]),
        ask_weak=float(snapshot["ask_weak"]),
        spread_strong=float(snapshot["spread_strong"]),
        spread_weak=float(snapshot["spread_weak"]),
        tau_sec=int(snapshot["tau_sec"]),
        min_edge=0.02,
        state=risk_state,
        entry_min_sec=3,
        entry_max_sec=120,
        max_spread=0.08,
        daily_loss_cap=100.0,
        max_consecutive_losses=5,
    )
