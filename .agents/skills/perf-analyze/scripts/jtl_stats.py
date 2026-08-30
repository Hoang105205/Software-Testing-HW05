#!/usr/bin/env python3
"""Compute ground-truth metrics from a JMeter .jtl (CSV format) log.

Usage:
    python jtl_stats.py path/to/result.jtl [--markdown]

Outputs per-request-label stats (samples, error %, avg/min/max, p95, p99,
throughput) plus overall totals. Markdown mode emits a report table ready
to paste into report/analysis/metrics_{Scenario}.md.
"""

import csv
import sys
from collections import defaultdict


def percentile(sorted_vals, p):
    if not sorted_vals:
        return 0
    k = (len(sorted_vals) - 1) * p / 100.0
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def main():
    if len(sys.argv) < 2:
        print("Usage: python jtl_stats.py <result.jtl> [--markdown]", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    markdown = "--markdown" in sys.argv

    rows_by_label = defaultdict(list)
    ts_min, ts_max = None, None

    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        required = {"label", "elapsed", "success", "timeStamp"}
        if not required.issubset(set(reader.fieldnames or [])):
            print(f"ERROR: expected CSV .jtl with columns {required}, "
                  f"got {reader.fieldnames}", file=sys.stderr)
            sys.exit(2)
        for row in reader:
            try:
                elapsed = int(row["elapsed"])
                ts = int(row["timeStamp"])
            except (ValueError, KeyError):
                continue
            ok = str(row["success"]).strip().lower() == "true"
            rows_by_label[row["label"]].append((elapsed, ok, ts))
            ts_min = ts if ts_min is None else min(ts_min, ts)
            ts_max = ts if ts_max is None else max(ts_max, ts)

    if not rows_by_label:
        print("ERROR: no samples parsed", file=sys.stderr)
        sys.exit(2)

    duration_s = max((ts_max - ts_min) / 1000.0, 0.001)

    def stats(samples):
        n = len(samples)
        fails = sum(1 for _, ok, _ in samples if not ok)
        times = sorted(t for t, _, _ in samples)
        return {
            "n": n,
            "err_pct": 100.0 * fails / n if n else 0.0,
            "avg": sum(times) / n if n else 0.0,
            "min": times[0] if times else 0,
            "max": times[-1] if times else 0,
            "p95": percentile(times, 95),
            "p99": percentile(times, 99),
            "rps": n / duration_s,
        }

    results = {label: stats(samples)
               for label, samples in sorted(rows_by_label.items())}
    overall = stats([s for samples in rows_by_label.values() for s in samples])

    header = ("label", "samples", "error %", "avg ms", "min ms", "max ms",
              "p95 ms", "p99 ms", "rps")

    def fmt(label, s):
        return (label, str(s["n"]), f"{s['err_pct']:.2f}", f"{s['avg']:.0f}",
                str(s["min"]), str(s["max"]), f"{s['p95']:.0f}",
                f"{s['p99']:.0f}", f"{s['rps']:.2f}")

    lines = []
    lines.append(f"Source: `{path}`")
    lines.append(f"Duration: {duration_s:.1f} s | "
                 f"Total samples: {overall['n']} | "
                 f"Overall error rate: {overall['err_pct']:.2f}%")
    lines.append("")
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "---|" * len(header))
    for label, s in results.items():
        lines.append("| " + " | ".join(fmt(label, s)) + " |")
    lines.append("| " + " | ".join(fmt("**OVERALL**", overall)) + " |")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
