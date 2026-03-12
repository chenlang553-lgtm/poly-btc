def discrete_size(edge: float, ask: float) -> int:
    if edge <= 0.02:
        return 0
    if edge <= 0.04:
        base = 2
    elif edge <= 0.07:
        base = 3
    else:
        base = 5

    if ask > 0.85:
        return 0
    if ask > 0.80:
        return max(1, int(base * 0.5))
    return base
