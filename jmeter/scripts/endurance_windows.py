#!/usr/bin/env python3
"""Split a JMeter CSV .jtl into 1-minute windows and find the endurance threshold.

Usage: python endurance_windows.py <path/to/result.jtl>
Threshold rule (per requirement): the LAST window where
  error % < 1  AND  p95 <= 2 x first-window p95  AND  throughput within +/-10% of first window.
Prints a markdown table ready to paste into report/endurance_threshold.md.
"""
import csv
import sys
from pathlib import Path

REQUIRED = {"timeStamp", "elapsed", "success"}
WINDOW_MS = 60_000


def percentile(values, p):
    if not values:
        return 0.0
    s = sorted(values)
    k = (len(s) - 1) * p / 100.0
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def main(path):
    rows = []
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None or not REQUIRED.issubset(set(reader.fieldnames)):
            sys.exit(f"ERROR: {path} is not a CSV-format .jtl (missing {REQUIRED})")
        for r in reader:
            try:
                rows.append((int(r["timeStamp"]), int(r["elapsed"]), r["success"].strip().lower() == "true"))
            except (ValueError, KeyError):
                continue
    if not rows:
        sys.exit("ERROR: no samples found")

    t0 = min(ts for ts, _, _ in rows)
    windows = {}
    for ts, el, ok in rows:
        w = (ts - t0) // WINDOW_MS
        windows.setdefault(w, {"samples": 0, "err": 0, "elapsed": []})
        windows[w]["samples"] += 1
        windows[w]["elapsed"].append(el)
        if not ok:
            windows[w]["err"] += 1

    base = windows[0]
    base_p95 = percentile(base["elapsed"], 95)
    base_rps = base["samples"] / 60.0
    print(f"Baseline (window 1): p95={base_p95:.0f} ms | rps={base_rps:.2f}\n")

    print("| minute | samples | rps | p95 ms | error % | within rule |")
    print("|---|---|---|---|---|---|")
    last_ok = None
    for w in sorted(windows):
        d = windows[w]
        p95 = percentile(d["elapsed"], 95)
        err = 100.0 * d["err"] / d["samples"]
        rps = d["samples"] / 60.0
        ok = err < 1 and p95 <= 2 * base_p95 and abs(rps - base_rps) <= 0.1 * base_rps
        if ok and d["samples"] >= 30:  # ignore a partial final window
            last_ok = (w, rps, p95, err)
        print(f"| {w + 1} | {d['samples']} | {rps:.2f} | {p95:.0f} | {err:.2f} | {'PASS' if ok else 'FAIL'} |")

    print()
    if last_ok:
        w, rps, p95, err = last_ok
        print(f"ENDURANCE THRESHOLD: stable through minute {w + 1}"
              f" (~{rps:.1f} RPS sustained, p95={p95:.0f} ms, err={err:.2f}%).")
        print("=> Maximum stable RPS = the value above; pair it with the node.exe memory reading")
        print("   (MB) from your Task Manager screenshots at/just before that minute = memory ceiling.")
    else:
        print("No full minute window satisfied all three rules - soak degraded early.")
        print("Report the FIRST failing window and what broke (error % / p95 / throughput drop).")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "jmeter/results/Endurance/result.jtl")
