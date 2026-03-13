import asyncio
from datetime import datetime, timezone
from typing import Any

import orjson
import websockets

from collector.recorder import JsonlRecorder
from schemas.raw_events import RawEvent


class PolymarketMarketWsCollector:
    def __init__(self, ws_url: str, recorder: JsonlRecorder, heartbeat_sec: int = 10) -> None:
        self.ws_url = ws_url
        self.recorder = recorder
        self.heartbeat_sec = heartbeat_sec

    async def run(self, subscribe_payload: dict[str, Any]) -> None:
        backoff = 1
        while True:
            try:
                async with websockets.connect(self.ws_url, ping_interval=self.heartbeat_sec) as ws:
                    await ws.send(orjson.dumps(subscribe_payload).decode())
                    async for msg in ws:
                        raw = orjson.loads(msg)
                        event = RawEvent(
                            source="polymarket_market_ws",
                            event_type=str(raw.get("event_type", "market_update")),
                            exchange_ts=_parse_ts(raw.get("timestamp")),
                            received_ts=datetime.now(timezone.utc),
                            market_id=raw.get("market"),
                            payload=raw,
                        )
                        self.recorder.append(event)
                backoff = 1
            except Exception:
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 30)


def _parse_ts(raw_ts: Any) -> datetime | None:
    if raw_ts is None:
        return None
    try:
        return datetime.fromtimestamp(float(raw_ts), tz=timezone.utc)
    except (TypeError, ValueError):
        return None
