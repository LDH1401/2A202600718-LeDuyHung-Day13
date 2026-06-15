# Evidence Collection Sheet

## Local verification

Commands run:

```bash
python scripts/generate_demo_logs.py
python scripts/validate_logs.py
pytest -q
```

Current result:
- `pytest`: 5 passed
- `validate_logs.py`: 100/100
- Total log records analyzed: 43
- Missing required fields: 0
- Missing enrichment fields: 0
- Unique correlation IDs: 22
- Potential PII leaks: 0
- `/metrics.traffic`: 10
- `/metrics.quality_avg`: 0.86

## Required screenshots
- Langfuse trace list with >= 10 traces
- One full trace waterfall
- JSON logs showing correlation_id
- Log line with PII redaction
- Dashboard with 6 panels
- Alert rules with runbook link

## Capture targets
- Logs: `data/logs.jsonl`
- Dashboard: `http://127.0.0.1:8000/dashboard`
- Metrics: `http://127.0.0.1:8000/metrics`
- Alerts: `config/alert_rules.yaml`
- Runbooks: `docs/alerts.md`

## Optional screenshots
- Incident before/after fix
- Cost comparison before/after optimization
- Auto-instrumentation proof
