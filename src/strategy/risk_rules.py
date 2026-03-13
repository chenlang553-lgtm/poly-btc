from dataclasses import dataclass


@dataclass(slots=True)
class RiskState:
    has_position_in_window: bool = False
    day_pnl: float = 0.0
    consecutive_losses: int = 0


def passes_risk(
    *,
    side: str,
    ask_strong: float,
    ask_weak: float,
    spread_strong: float,
    spread_weak: float,
    tau_sec: int,
    state: RiskState,
    entry_min_sec: int,
    entry_max_sec: int,
    max_spread: float,
    daily_loss_cap: float,
    max_consecutive_losses: int,
) -> tuple[bool, str]:
    if state.has_position_in_window:
        return False, "one-entry-per-window"
    if tau_sec < entry_min_sec or tau_sec > entry_max_sec or tau_sec <= 3:
        return False, "tail-timing"
    if spread_strong > max_spread or spread_weak > max_spread:
        return False, "spread"
    if side == "BUY_STRONG" and ask_strong > 0.85:
        return False, "strong-cap"
    if side == "BUY_WEAK" and ask_weak < 0.08:
        return False, "weak-floor"
    if state.day_pnl <= -abs(daily_loss_cap):
        return False, "daily-loss-cap"
    if state.consecutive_losses >= max_consecutive_losses:
        return False, "consecutive-loss-stop"
    return True, "ok"
