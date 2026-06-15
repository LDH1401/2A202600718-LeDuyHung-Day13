# Day 13 Observability Lab Report

## 1. Team Metadata
- [GROUP_NAME]: LeDuyHung-Day13
- [REPO_URL]: https://github.com/LDH1401/2A202600718-LeDuyHung-Day13
- [MEMBERS]:
  - Member A: Le Duy Hung | Role: Logging & PII
  - Member B: Le Duy Hung | Role: Tracing & Enrichment
  - Member C: Le Duy Hung | Role: SLO & Alerts
  - Member D: Le Duy Hung | Role: Load Test & Dashboard
  - Member E: Le Duy Hung | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 10 local demo requests generated; live Langfuse trace count must be confirmed after adding `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY`
- [PII_LEAKS_FOUND]: 0

Verification command:

```bash
python scripts/generate_demo_logs.py
python scripts/validate_logs.py
```

Latest local result:

```text
Total log records analyzed: 43
Records with missing required fields: 0
Records with missing enrichment (context): 0
Unique correlation IDs found: 22
Potential PII leaks detected: 0
Estimated Score: 100/100
```

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: `data/logs.jsonl` records for `req-demo001` through `req-demo010`
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: `data/logs.jsonl` records showing `[REDACTED_EMAIL]`, `[REDACTED_PHONE_VN]`, and `[REDACTED_CREDIT_CARD]`
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: Capture from Langfuse after running demo traffic with Langfuse keys configured
- [TRACE_WATERFALL_EXPLANATION]: The agent trace should show the `/chat` request entering the agent, retrieval running before the fake LLM call, then metadata for hashed user ID, session ID, feature, model, input tokens, output tokens, and document count.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: Open `/dashboard` while the app is running and capture the 6-panel view
- [SLO_TABLE]:

| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 150ms in socket demo |
| Error Rate | < 2% | 28d | 0 known API errors in socket demo |
| Cost Budget | < $2.5/day | 1d | $0.0203 total socket demo cost |
| Quality Score | >= 0.75 avg | 28d | 0.86 |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: `config/alert_rules.yaml`
- [SAMPLE_RUNBOOK_LINK]: `docs/alerts.md#1-high-latency-p95`

Implemented alert rules:
- `high_latency_p95`
- `high_error_rate`
- `cost_budget_spike`
- `pii_leak_detected`

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: `rag_slow`
- [SYMPTOMS_OBSERVED]: Latency P95/P99 rises while traffic continues to return successful responses.
- [ROOT_CAUSE_PROVED_BY]: `app/mock_rag.py` adds a 2.5 second sleep when `STATE["rag_slow"]` is enabled; the slow trace should isolate retrieval as the long span.
- [FIX_ACTION]: Disable the incident with `python scripts/inject_incident.py --scenario rag_slow --disable` or `POST /incidents/rag_slow/disable`.
- [PREVENTIVE_MEASURE]: Keep the `high_latency_p95` alert active, inspect slow traces first, and use the correlation ID to inspect sanitized request logs.

---

## 5. Individual Contributions & Evidence

### Le Duy Hung
- [TASKS_COMPLETED]: Implemented correlation ID middleware, structured JSON logging, PII scrubbing, request context enrichment, tracing-safe local fallback, dashboard endpoint, SLOs, alert runbooks, demo log generator, and automated tests.
- [EVIDENCE_LINK]: Local files changed in `app/`, `config/`, `docs/`, `scripts/`, and `tests/`; create a commit after review for final Git evidence.

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: Cost metrics are tracked in `/metrics` as `avg_cost_usd` and `total_cost_usd`; `cost_budget_spike` alert documents mitigation.
- [BONUS_AUDIT_LOGS]: Audit log path is configured in `.env.example`; current implementation focuses on structured application logs.
- [BONUS_CUSTOM_METRIC]: `quality_avg` is exposed as a custom quality proxy in `/metrics` and `/dashboard`.
