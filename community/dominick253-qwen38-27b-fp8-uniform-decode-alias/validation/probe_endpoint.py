#!/usr/bin/env python3
"""Bounded tiny-prefill/mixed-session screen; not a quality suite or long soak."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


PROMPTS = [
    ("one-token", [17]),
    ("two-token", [17, 18]),
    ("arithmetic", "Calculate 17 + 25. Give the answer in a short sentence."),
    ("operations", "A small team runs a document search service on one server. "
     "Requests slowed down after a new index was installed, but memory use and "
     "CPU use look normal. Explain three concrete checks an engineer should "
     "perform to distinguish storage latency, a query-plan regression, and a "
     "network problem. Keep the explanation practical and do not assume the "
     "service can be restarted during business hours."),
]


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def response_checks(response):
    """Return normalized evidence and errors without accepting partial responses."""
    errors = []
    if not isinstance(response, dict):
        return {"errors": ["response is not an object"], "passed": False}
    choices = response.get("choices")
    if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
        return {"errors": ["expected exactly one choice object"], "passed": False}
    choice = choices[0]
    text = choice.get("text")
    ids = choice.get("token_ids")
    valid_text = isinstance(text, str) and bool(text.strip())
    valid_ids = (isinstance(ids, list) and bool(ids)
                 and all(type(i) is int and i >= 0 for i in ids))
    if not valid_text:
        errors.append("missing, empty or invalid completion text")
    if not valid_ids:
        errors.append("missing, empty or invalid completion token_ids")
    if choice.get("finish_reason") not in ("stop", "length"):
        errors.append("unexpected or absent finish_reason")
    usage = response.get("usage")
    if not isinstance(usage, dict):
        errors.append("missing or invalid usage")
        usage = {}
    cached_values = []
    for field in ("prompt_tokens_details", "input_tokens_details"):
        details = usage.get(field)
        if details is not None and not isinstance(details, dict):
            errors.append("invalid " + field)
        if isinstance(details, dict) and "cached_tokens" in details:
            cached_values.append(details["cached_tokens"])
    if "cached_tokens" in usage:
        cached_values.append(usage["cached_tokens"])
    if any(type(value) is not int or value != 0 for value in cached_values):
        errors.append("reported cached_tokens is not zero")
    repetition = {"extreme_character_repetition": False, "extreme_token_repetition": False}
    if valid_text:
        visible = "".join(text.split())
        repetition["extreme_character_repetition"] = (
            len(visible) >= 32 and Counter(visible).most_common(1)[0][1] / len(visible) >= 0.90)
    if valid_ids:
        repetition["extreme_token_repetition"] = (
            len(ids) >= 24 and Counter(ids).most_common(1)[0][1] / len(ids) >= 0.90)
        if len(ids) > 64:
            errors.append("completion exceeds requested 64-token cap")
    if any(repetition.values()):
        errors.append("obvious output repetition")
    return {"passed": not errors, "errors": errors, "text": text,
            "token_ids": ids, "text_sha256": digest(text) if valid_text else None,
            "token_ids_sha256": digest(ids) if valid_ids else None,
            "usage": usage, "cached_tokens_reported": bool(cached_values),
            "cached_tokens_values": cached_values, **repetition}


def request_one(url, model, prompt_id, prompt, phase, timeout):
    payload = {"model": model, "prompt": prompt, "temperature": 0,
               "seed": 42, "max_tokens": 64, "stream": False,
               "return_token_ids": True, "add_special_tokens": False}
    record = {"prompt_id": prompt_id, "phase": phase, "request": payload,
              "started_at": datetime.now(timezone.utc).isoformat()}
    start = time.monotonic()
    try:
        request = Request(url, data=json.dumps(payload).encode(),
                          headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=timeout) as result:
            record["http_status"] = result.status
            raw = result.read().decode("utf-8")
        record["raw_response"] = raw
        response = json.loads(raw)
        record["response"] = response
        record.update(response_checks(response))
    except HTTPError as exc:
        record.update(passed=False, http_status=exc.code,
                      raw_response=exc.read().decode("utf-8", errors="replace"),
                      errors=[str(exc)])
    except Exception as exc:
        record.update(passed=False, errors=[type(exc).__name__ + ": " + str(exc)])
    record["elapsed_seconds"] = time.monotonic() - start
    return record


def exact_match(left, right):
    if not left.get("passed") or not right.get("passed"):
        return None
    return left["token_ids"] == right["token_ids"] and left["text"] == right["text"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--timeout", type=float, default=180)
    args = parser.parse_args()
    parsed = urlparse(args.base_url)
    if (parsed.scheme != "http" or parsed.hostname not in ("localhost", "127.0.0.1", "::1")
            or parsed.username or parsed.password or parsed.query or parsed.fragment
            or parsed.path.rstrip("/") not in ("", "/v1")):
        parser.error("base-url must be a local HTTP origin, optionally ending in /v1")
    if args.timeout <= 0:
        parser.error("timeout must be positive")
    url = args.base_url.rstrip("/")
    url += "/completions" if parsed.path.rstrip("/") == "/v1" else "/v1/completions"
    rows = []
    references = {}
    repeats = {}
    started = time.monotonic()
    for prompt_id, prompt in PROMPTS:
        pair = [request_one(url, args.model, prompt_id, prompt,
                            "sequential-" + str(i), args.timeout) for i in range(2)]
        rows.extend(pair)
        references[prompt_id] = pair[0]
        repeats[prompt_id] = exact_match(*pair)
    mixed_matches = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for batch in range(4):
            futures = [pool.submit(request_one, url, args.model, prompt_id, prompt,
                                   "mixed-" + str(batch), args.timeout)
                       for prompt_id, prompt in PROMPTS]
            for future in futures:
                row = future.result()
                rows.append(row)
                mixed_matches.append({"prompt_id": row["prompt_id"], "phase": row["phase"],
                                      "exact": exact_match(references[row["prompt_id"]], row)})
    result = {"schema": "qwen38-r50-tiny-prefill-screen-v1", "base_url": args.base_url,
              "model": args.model, "passed": all(row["passed"] for row in rows),
              "elapsed_seconds": time.monotonic() - started,
              "completed_at": datetime.now(timezone.utc).isoformat(),
              "request_count": len(rows), "sequential_repeat_exact": repeats,
              "sequential_repeat_drift": any(value is False for value in repeats.values()),
              "mixed_vs_sequential": mixed_matches,
              "identity_comparisons_are_diagnostic": True,
              "limits": "24-request screen, not a sustained soak or semantic quality gate; "
                        "R50 batch-shape differences are reported without failing this screen.",
              "rows": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"passed": result["passed"], "request_count": len(rows),
                      "sequential_repeat_drift": result["sequential_repeat_drift"],
                      "out": str(args.out)}))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
