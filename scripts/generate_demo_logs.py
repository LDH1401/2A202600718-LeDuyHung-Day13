import asyncio
import json
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.main import app

QUERIES = Path("data/sample_queries.jsonl")


async def main() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://demo") as client:
        for idx, line in enumerate(QUERIES.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            response = await client.post(
                "/chat",
                json=json.loads(line),
                headers={"x-request-id": f"req-demo{idx:03d}"},
            )
            body = response.json()
            print(f"[{response.status_code}] {body.get('correlation_id')} | {body.get('latency_ms')}ms")


if __name__ == "__main__":
    asyncio.run(main())
