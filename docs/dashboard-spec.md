# Dashboard Spec

Dashboard URL: `/dashboard`

Required Layer-2 panels implemented:
1. Latency P50/P95/P99 from `/metrics`
2. Traffic request count from `/metrics`
3. Error breakdown from `/metrics.error_breakdown`
4. Average and total cost from `/metrics`
5. Tokens in/out from `/metrics`
6. Quality proxy from `/metrics.quality_avg`

Quality bar:
- default time range = 1 hour
- auto refresh every 15-30 seconds
- visible threshold/SLO line
- units clearly labeled
- no more than 6-8 panels on the main layer

SLO and threshold lines:
- Latency P95: below 3000 ms
- Error rate alert: above 5% for 5 minutes
- Cost budget: below $2.50 per day
- Quality proxy: at least 0.75 average score

Demo commands:

```bash
uvicorn app.main:app --reload
python scripts/load_test.py --concurrency 5
open http://127.0.0.1:8000/dashboard
```

Sandbox-friendly evidence command:

```bash
python scripts/generate_demo_logs.py
python scripts/validate_logs.py
```
