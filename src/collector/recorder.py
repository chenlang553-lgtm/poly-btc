from pathlib import Path

import orjson

from schemas.raw_events import RawEvent


class JsonlRecorder:
    def __init__(self, out_path: Path) -> None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        self.out_path = out_path

    def append(self, event: RawEvent) -> None:
        with self.out_path.open("ab") as fh:
            fh.write(orjson.dumps(event.model_dump(mode="json")))
            fh.write(b"\n")
