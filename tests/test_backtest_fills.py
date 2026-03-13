from datetime import datetime, timezone

from backtest.fill_model import simulate_fill


def test_fill_buy_uses_ask_plus_slippage() -> None:
    fill = simulate_fill(
        market_id="m1",
        ts=datetime(2026, 1, 1, tzinfo=timezone.utc),
        side="BUY",
        ask=0.6,
        bid=0.5,
        shares=3,
        slippage=0.01,
    )
    assert fill.price == 0.61
