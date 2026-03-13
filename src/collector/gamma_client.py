from typing import Any

import httpx


class GammaClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def fetch_active_markets(self) -> list[dict[str, Any]]:
        url = f"{self.base_url}/markets"
        params = {"active": "true", "closed": "false"}
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict)]
        return []
