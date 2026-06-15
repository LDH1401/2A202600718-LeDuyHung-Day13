import asyncio
import json
import os
from pathlib import Path

import httpx

os.environ.setdefault("LOG_PATH", "data/test-logs.jsonl")

from app.main import app


def test_chat_logs_correlation_context_and_redacts_pii() -> None:
    log_path = Path(os.environ["LOG_PATH"])
    log_path.unlink(missing_ok=True)

    payload = {
        "user_id": "student-01",
        "session_id": "session-01",
        "feature": "qa",
        "message": "Refund question from student@vinuni.edu.vn with card 4111 1111 1111 1111",
    }

    async def post_chat() -> httpx.Response:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post("/chat", json=payload, headers={"x-request-id": "req-test1234"})

    response = asyncio.run(post_chat())

    assert response.status_code == 200
    body = response.json()
    assert body["correlation_id"] == "req-test1234"
    assert response.headers["x-request-id"] == "req-test1234"
    assert float(response.headers["x-response-time-ms"]) >= 0

    records = [
        json.loads(line)
        for line in log_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    api_records = [record for record in records if record.get("service") == "api"]

    assert {record["event"] for record in api_records} >= {"request_received", "response_sent"}
    assert all(record["correlation_id"] == "req-test1234" for record in api_records)
    assert all(record["env"] == "dev" for record in api_records)
    assert all(record["user_id_hash"] for record in api_records)
    assert all(record["session_id"] == "session-01" for record in api_records)
    assert all(record["feature"] == "qa" for record in api_records)
    assert all(record["model"] == "claude-sonnet-4-5" for record in api_records)

    raw_logs = log_path.read_text(encoding="utf-8")
    assert "student@vinuni.edu.vn" not in raw_logs
    assert "4111" not in raw_logs
    assert "REDACTED_EMAIL" in raw_logs
    assert "REDACTED_CREDIT_CARD" in raw_logs


def test_dashboard_route_contains_required_panels() -> None:
    async def get_dashboard() -> httpx.Response:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/dashboard")

    response = asyncio.run(get_dashboard())

    assert response.status_code == 200
    html = response.text
    for panel in ["Latency", "Traffic", "Errors", "Cost", "Tokens", "Quality"]:
        assert panel in html
