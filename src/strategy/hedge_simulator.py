def simulate_hedge(entry_price: float, exit_price: float, shares: int, hedge_ratio: float = 0.5) -> float:
    return (exit_price - entry_price) * shares * hedge_ratio
