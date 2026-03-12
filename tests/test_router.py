from datetime import datetime, timezone

from strategy.continuation_router import route_decision
from strategy.risk_rules import RiskState


def test_router_picks_best_edge() -> None:
    decision = route_decision(
        market_id="m1",
        snapshot_ts=datetime(2026, 1, 1, tzinfo=timezone.utc),
        p_cont=0.7,
        ask_strong=0.55,
        ask_weak=0.40,
        spread_strong=0.02,
        spread_weak=0.02,
        tau_sec=50,
        min_edge=0.02,
        state=RiskState(),
        entry_min_sec=3,
        entry_max_sec=120,
        max_spread=0.08,
        daily_loss_cap=100,
        max_consecutive_losses=5,
    )
    assert decision.action == "BUY_STRONG"
    assert decision.size > 0
