from flask import Flask, render_template
from datetime import datetime
import json

from tester.client import http_get
from tester.tests import run_contract_tests
from storage import init_db, save_run, list_runs

app = Flask(__name__)

API_NAME = "ipify"
API_URL = "https://api.ipify.org?format=json"


def p95(values):
    if not values:
        return 0.0
    s = sorted(values)
    k = int(round(0.95 * (len(s) - 1)))
    return float(s[k])


@app.get("/")
def home():
    # page d'accueil = dashboard
    return dashboard()


@app.get("/dashboard")
def dashboard():
    init_db()
    runs = list_runs(50)
    last = runs[0] if runs else None

    # details des tests (si présent)
    tests = []
    if last and last.get("details"):
        try:
            tests = json.loads(last["details"])
        except Exception:
            tests = []

    return render_template("dashboard.html", runs=runs, last=last, tests=tests)


@app.get("/run")
def run():
    init_db()

    latencies = []
    test_rows = []
    passed_tests = 0
    failed_tests = 0

    # 5 appels max = charge limitée
    for i in range(5):
        resp, ms = http_get(API_URL, timeout_s=3.0, retries=1)
        latencies.append(ms)

        try:
            body = resp.json()
        except Exception:
            body = {}

        # tests contrat (>=6)
        tests = run_contract_tests(resp, body)

        for name, ok, details in tests:
            test_rows.append({
                "name": name,
                "status": "PASS" if ok else "FAIL",
                "latency_ms": round(ms, 1),
                "http": resp.status_code,
                "details": details
            })
            if ok:
                passed_tests += 1
            else:
                failed_tests += 1

    avg_ms = sum(latencies) / len(latencies) if latencies else 0.0
    p95_ms = p95(latencies)

    # Stockage SQLite
    save_run(
        ts=datetime.utcnow().isoformat(),
        api_name=API_NAME,
        avg_ms=float(avg_ms),
        p95_ms=float(p95_ms),
        passed=int(passed_tests),
        failed=int(failed_tests),
        details=json.dumps(test_rows)
    )

    return dashboard()
