import time
import requests

def http_get(url: str, timeout_s: float = 3.0, retries: int = 1):
    last_err = None
    for attempt in range(retries + 1):
        start = time.perf_counter()
        try:
            r = requests.get(url, timeout=timeout_s, headers={"User-Agent": "M1-API-Monitor/1.0"})
            latency_ms = (time.perf_counter() - start) * 1000.0
            return r, latency_ms
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(0.5)
    raise last_err
