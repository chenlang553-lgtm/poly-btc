from schemas.fills import Fill


def simulate_fill(
    *,
    market_id: str,
    ts,
    side: str,
    ask: float,
    bid: float,
    shares: int,
    latency_ms: int = 150,
    slippage: float = 0.002,
) -> Fill:
    if side == "BUY":
        px = min(0.999, ask + slippage)
    else:
        px = max(0.001, bid - slippage)
    return Fill(
        market_id=market_id,
        ts=ts,
        side=side,
        price=px,
        shares=shares,
        latency_ms=latency_ms,
        slippage=slippage,
    )
