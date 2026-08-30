# Endurance / Soak Test — Threshold Report

SID 23127047 · 2026-08-30 · Dell OptiPlex 7040 (i7-6700, 32 GB RAM, Win10) · SUT and JMeter on the same machine

## Setup
- 10 threads, 10 s ramp-up, infinite loops, 600 s scheduler (10 min) — full admin workflow incl. PUT transitions
- ~2,000 pending orders seeded; 1,819 transitions executed without the id supply running dry

## Results

Baseline (minute 1): 11.42 RPS · p95 22 ms

| minute | samples | rps | p95 ms | error % |
|---|---|---|---|---|
| 1 | 685 | 11.42 | 22 | 0.00 |
| 2 | 735 | 12.25 | 24 | 0.00 |
| 3 | 733 | 12.22 | 28 | 0.00 |
| 4 | 735 | 12.25 | 27 | 0.00 |
| 5 | 734 | 12.23 | 26 | 0.00 |
| 6 | 734 | 12.23 | 27 | 0.00 |
| 7 | 734 | 12.23 | 27 | 0.00 |
| 8 | 737 | 12.28 | 29 | 0.00 |
| 9 | 733 | 12.22 | 29 | 0.00 |
| 10 | 726 | 12.10 | 26 | 0.00 |

Stability rule: error % < 1, p95 ≤ 2× baseline, throughput within ±10% of baseline — all 10 windows pass.

## Threshold (concrete numbers)
- **Maximum stable RPS: ≈ 12.2**, sustained for the full 10 minutes (7,286 samples, 0.00% errors)
- **Latency: no degradation** — p95 flat at 22–29 ms (worst window 1.3× baseline, rule allows 2×)
- **Memory ceiling: ~71 MB** backend working set at end of soak (baseline ~44 MB); negligible on 32 GB RAM — the machine's binding limit would be CPU/SQLite write serialization, not memory
- The breaking point was not reached: 10 concurrent admins for 10 min left clear headroom, so the threshold is "at least 12.2 RPS sustained"

## Observation
After the run, backend memory kept growing to ~110 MB while idle — a retention/leak symptom in the SUT, listed as a perf-issue candidate in the main report.
