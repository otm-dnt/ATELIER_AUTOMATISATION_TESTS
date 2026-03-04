import re

IPV4_RE = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
IPV6_RE = re.compile(r"^[0-9a-fA-F:]+$")

def _is_ip(s: str) -> bool:
    if not isinstance(s, str) or not s:
        return False
    if IPV4_RE.match(s):
        parts = s.split(".")
        return all(0 <= int(p) <= 255 for p in parts)
    return bool(IPV6_RE.match(s))

def run_contract_tests(response, json_body):
    """
    Retourne une liste de tests: (name, ok, details)
    API: ipify -> {"ip":"x.x.x.x"}
    """
    tests = []

    # 1) status code
    tests.append(("status_200", response.status_code == 200, f"status={response.status_code}"))

    # 2) content-type
    ctype = response.headers.get("Content-Type", "")
    tests.append(("content_type_json", "application/json" in ctype.lower(), f"content-type={ctype}"))

    # 3) json is object
    tests.append(("json_is_object", isinstance(json_body, dict), f"type={type(json_body).__name__}"))

    # 4) has ip field
    has_ip = isinstance(json_body, dict) and "ip" in json_body
    tests.append(("has_ip_field", has_ip, f"keys={list(json_body.keys()) if isinstance(json_body, dict) else 'n/a'}"))

    # 5) ip is string
    ip_is_str = has_ip and isinstance(json_body["ip"], str)
    tests.append(("ip_is_string", ip_is_str, f"ip_type={type(json_body.get('ip')).__name__}"))

    # 6) ip format valid (v4 or v6)
    ip_ok = ip_is_str and _is_ip(json_body["ip"])
    tests.append(("ip_format_valid", ip_ok, f"ip={json_body.get('ip')}"))

    return tests
