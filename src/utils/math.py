import math


def safe_log_ratio(now_price: float, open_price: float) -> float:
    if now_price <= 0 or open_price <= 0:
        return 0.0
    return math.log(now_price / open_price)
