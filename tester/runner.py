import time
import json
from datetime import datetime
from tester.client import http_get
from tester.tests import run_contract_tests

API_URL = "https://api.ipify.org?format=json"

def run_tests():
    results = []
    latencies = []

    for i in range(5):
        response, latency = http_get(API_URL)
        latencies.append(latency)

        json_body = response.json()

        tests = run_contract_tests(response, json_body)

        for name, ok, details in tests:
            results.append({
                "name": name,
                "status": "PASS" if ok else "FAIL",
                "details": details
            })

        time.sleep(1)

    avg_latency = sum(latencies) / len(latencies)
    p95_latency = sorted(latencies)[int(len(latencies)*0.95)-1]

    summary = {
        "timestamp": datetime.now().isoformat(),
        "latency_avg": avg_latency,
        "latency_p95": p95_latency,
        "tests": results
    }

    return summary


if __name__ == "__main__":
    print(json.dumps(run_tests(), indent=2))
