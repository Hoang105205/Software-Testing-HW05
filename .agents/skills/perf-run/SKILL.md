---
name: perf-run
description: Stage 2 of the HW05 kit. Executes the Load, Stress, and Spike scenarios plus the endurance soak, collecting raw .jtl logs, HTML reports, same-frame screenshots, and lockout-reset notes. Use when the user says "perf-run" or wants to execute the scenarios.
---

# Stage 2 — run (3 scenarios + endurance)

Goal: runs executed with complete evidence; `report/perf_report.md` §2. The kit drives; the human clicks JMeter, takes screenshots, and records the demo video (R8).

Scope: the plan-type passed by `/perf-on` (`Load` | `Stress` | `Spike` | all). Missing → ask the human which scenario to run next. All three scenarios are required for submission; endurance follows the last of them.

## Pre-flight (before the first run)

- SUT up, DB in known state, no locked accounts (verify with one manual login).
- Hardware evidence ONCE: dxdiag screenshot + spec table (hostname must match previous homeworks) → `jmeter/results/hardware/`.

## Per scenario (in scope; default order Load → Stress → Spike)

1. Task Manager open beside JMeter — same frame for screenshot + video. Start recording if due (Vietnamese narration, human's job).
2. Run. GUI for video evidence; CLI option for a stable log:
   ```bash
   jmeter -n -t "jmeter/plans/{SID}_{Scenario}_{DATE}.jmx" -l "jmeter/results/{Scenario}/result.jtl"
   ```
3. Mid-run screenshot (JMeter + Task Manager one frame) → `jmeter/results/{Scenario}/screenshots/`.
4. Keep the FULL raw `.jtl` (R5). Generate:
   ```bash
   jmeter -g "jmeter/results/{Scenario}/result.jtl" -o "jmeter/results/{Scenario}/html_report"
   ```
5. Lockout triggered? Reset accounts (method from report §1.1) and note it in §2 (R6).
6. Sanity check the `.jtl`: rows exist, duration spans the run, not all-fail.
7. Genuine bug or perf issue (error responses, crashes, functional regression)? → file a GitHub Issue with screenshot; note the issue link in §2.2.

## Endurance (after the last in-scope scenario)

- Clone the Load plan, duration 600–900 s at sustained load → `jmeter/results/Endurance/`.
- Compute the threshold from the raw log (1-minute windows): last window with error % < 1, p95 ≤ 2× first-window p95, throughput ±10% → max stable RPS + memory ceiling = endurance threshold.

## Output — append §2 to `report/perf_report.md`

```md
## 2. Execution
### 2.1 Environment
<hardware spec table · dxdiag screenshot path>
### 2.2 Scenario runs
| Scenario | Threads | Duration | Samples | Errors | Screenshot | Lockout resets | GitHub Issues |
### 2.3 Endurance
<window table · max stable RPS · memory ceiling · first degradation>
### 2.4 Evidence links
<demo video link (once uploaded) · result folders>
```

## Human gate & bookkeeping

Human confirms all evidence exists → `kit-state.md` (`run: done`) · audit entry · git commit per scenario. Next: `/perf-analyze`.
