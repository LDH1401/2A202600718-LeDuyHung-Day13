from __future__ import annotations


def render_dashboard() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Day 13 Observability Dashboard</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f7f8fa;
      --panel: #ffffff;
      --text: #1f2937;
      --muted: #667085;
      --border: #d8dee9;
      --blue: #2563eb;
      --green: #047857;
      --orange: #b45309;
      --red: #b91c1c;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 20px 24px 14px;
      border-bottom: 1px solid var(--border);
      background: #ffffff;
    }
    h1 {
      margin: 0;
      font-size: 22px;
      font-weight: 700;
    }
    .meta {
      display: flex;
      gap: 12px;
      align-items: center;
      color: var(--muted);
      font-size: 13px;
      white-space: nowrap;
    }
    main {
      width: min(1180px, 100%);
      margin: 0 auto;
      padding: 20px 24px 28px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }
    .panel {
      min-height: 174px;
      padding: 16px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--panel);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .panel h2 {
      margin: 0 0 12px;
      font-size: 14px;
      font-weight: 700;
      color: var(--muted);
    }
    .metric {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      align-items: baseline;
      padding: 6px 0;
      border-top: 1px solid #edf0f5;
    }
    .metric:first-of-type { border-top: 0; }
    .label {
      min-width: 0;
      overflow-wrap: anywhere;
      color: var(--muted);
      font-size: 13px;
    }
    .value {
      font-size: 24px;
      font-weight: 750;
      color: var(--text);
      text-align: right;
    }
    .unit {
      font-size: 12px;
      color: var(--muted);
      margin-left: 3px;
      font-weight: 600;
    }
    .threshold {
      margin-top: 10px;
      padding-top: 10px;
      border-top: 1px dashed var(--border);
      color: var(--muted);
      font-size: 12px;
    }
    .ok { color: var(--green); }
    .warn { color: var(--orange); }
    .bad { color: var(--red); }
    @media (max-width: 920px) {
      header { align-items: flex-start; flex-direction: column; }
      .meta { white-space: normal; flex-wrap: wrap; }
      .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 620px) {
      main { padding: 14px; }
      .grid { grid-template-columns: 1fr; }
      .value { font-size: 22px; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Day 13 Observability Dashboard</h1>
    <div class="meta">
      <span id="status">Loading</span>
      <span>Range: 1h</span>
      <span>Refresh: 15s</span>
    </div>
  </header>
  <main>
    <section class="grid" aria-label="Observability panels">
      <article class="panel">
        <h2>Latency</h2>
        <div class="metric"><span class="label">P50</span><span class="value" id="latency-p50">0<span class="unit">ms</span></span></div>
        <div class="metric"><span class="label">P95</span><span class="value" id="latency-p95">0<span class="unit">ms</span></span></div>
        <div class="metric"><span class="label">P99</span><span class="value" id="latency-p99">0<span class="unit">ms</span></span></div>
        <div class="threshold">SLO: P95 below 3000 ms</div>
      </article>
      <article class="panel">
        <h2>Traffic</h2>
        <div class="metric"><span class="label">Requests</span><span class="value" id="traffic">0</span></div>
        <div class="metric"><span class="label">Window</span><span class="value">1<span class="unit">h</span></span></div>
        <div class="threshold">Target: steady successful volume</div>
      </article>
      <article class="panel">
        <h2>Errors</h2>
        <div class="metric"><span class="label">Total error types</span><span class="value" id="error-types">0</span></div>
        <div class="metric"><span class="label">Breakdown</span><span class="value" id="error-breakdown">none</span></div>
        <div class="threshold">Alert: error rate above 5% for 5m</div>
      </article>
      <article class="panel">
        <h2>Cost</h2>
        <div class="metric"><span class="label">Average</span><span class="value">$<span id="avg-cost">0.0000</span></span></div>
        <div class="metric"><span class="label">Total</span><span class="value">$<span id="total-cost">0.0000</span></span></div>
        <div class="threshold">Budget: below $2.50 per day</div>
      </article>
      <article class="panel">
        <h2>Tokens</h2>
        <div class="metric"><span class="label">Input</span><span class="value" id="tokens-in">0</span></div>
        <div class="metric"><span class="label">Output</span><span class="value" id="tokens-out">0</span></div>
        <div class="threshold">Watch output spikes for cost alerts</div>
      </article>
      <article class="panel">
        <h2>Quality</h2>
        <div class="metric"><span class="label">Average score</span><span class="value" id="quality">0.00</span></div>
        <div class="metric"><span class="label">Target</span><span class="value">0.75</span></div>
        <div class="threshold">Proxy: heuristic answer quality</div>
      </article>
    </section>
  </main>
  <script>
    const statusEl = document.getElementById("status");
    const setText = (id, value) => { document.getElementById(id).textContent = value; };
    const formatNumber = (value) => Number(value || 0).toLocaleString();
    const formatMs = (value) => Math.round(Number(value || 0)).toString();
    const formatCost = (value) => Number(value || 0).toFixed(4);
    const formatQuality = (value) => Number(value || 0).toFixed(2);

    async function refresh() {
      try {
        const response = await fetch("/metrics", { cache: "no-store" });
        const data = await response.json();
        setText("latency-p50", formatMs(data.latency_p50));
        document.getElementById("latency-p50").insertAdjacentHTML("beforeend", "<span class='unit'>ms</span>");
        setText("latency-p95", formatMs(data.latency_p95));
        document.getElementById("latency-p95").insertAdjacentHTML("beforeend", "<span class='unit'>ms</span>");
        setText("latency-p99", formatMs(data.latency_p99));
        document.getElementById("latency-p99").insertAdjacentHTML("beforeend", "<span class='unit'>ms</span>");
        setText("traffic", formatNumber(data.traffic));
        setText("error-types", Object.keys(data.error_breakdown || {}).length);
        setText("error-breakdown", Object.keys(data.error_breakdown || {}).length ? JSON.stringify(data.error_breakdown) : "none");
        setText("avg-cost", formatCost(data.avg_cost_usd));
        setText("total-cost", formatCost(data.total_cost_usd));
        setText("tokens-in", formatNumber(data.tokens_in_total));
        setText("tokens-out", formatNumber(data.tokens_out_total));
        setText("quality", formatQuality(data.quality_avg));
        statusEl.textContent = "Updated " + new Date().toLocaleTimeString();
        statusEl.className = "ok";
      } catch (error) {
        statusEl.textContent = "Metrics unavailable";
        statusEl.className = "bad";
      }
    }
    refresh();
    setInterval(refresh, 15000);
  </script>
</body>
</html>"""
