# Mock Debug Q&A

## 1. How does the correlation ID flow work?

`CorrelationIdMiddleware` clears old context variables, reads `x-request-id` if present, or generates `req-<8 hex chars>`. It binds that value into structlog contextvars, stores it on `request.state.correlation_id`, and returns it in the `x-request-id` response header.

## 2. Why hash `user_id` instead of logging it directly?

Raw user identifiers are sensitive and may become PII depending on the source system. The app logs `user_id_hash`, which keeps requests groupable without exposing the original ID.

## 3. Where does PII redaction happen?

PII patterns live in `app/pii.py`. `app/logging_config.py` registers `scrub_event` as a structlog processor before the JSONL file processor, so payloads, error text, and nested strings are redacted before they are written.

## 4. How would you debug `rag_slow`?

Start with the latency P95/P99 dashboard panel, open the slow trace waterfall, then use the trace correlation ID to inspect JSON logs. The expected root cause is the `time.sleep(2.5)` branch in `app/mock_rag.py` when `STATE["rag_slow"]` is enabled.

## 5. How would you debug `tool_fail`?

Start from the error alert, inspect `/metrics.error_breakdown`, then search logs for `event=request_failed` and the `error_type`. The expected root cause is `RuntimeError("Vector store timeout")` in `app/mock_rag.py`.

## 6. How would you debug `cost_spike`?

Check the cost and tokens panels, compare `tokens_out_total` against baseline, then inspect traces by feature/model. The expected root cause is output tokens being multiplied when `STATE["cost_spike"]` is enabled.

## 7. What proves the lab implementation passes logging checks?

Run:

```bash
python scripts/generate_demo_logs.py
python scripts/validate_logs.py
```

The latest local run analyzed 43 log records, produced 0 missing required fields, 0 missing enrichment fields, 22 unique correlation IDs, 0 PII leaks, and an estimated score of 100/100.
