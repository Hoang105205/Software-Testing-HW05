---
name: perf-analyze
description: Stage 3 of the HW05 kit (Task 2). Computes ground-truth metrics from raw .jtl logs, obtains the AI analysis, hunts misinterpretations against the raw logs, and judges the AI's optimizations as feasible or hallucinated. Use when the user says "perf-analyze" or wants to analyse the JMeter results.
---

# Stage 3 — analyze (Task 2, one stage)

Goal: `report/perf_report.md` §3 = AI analysis + misinterpretation hunt + optimization judgement.

## Steps

1. **Ground truth FIRST — paste straight into report §3.1 (no separate metrics files).** Per scenario:
   ```bash
   python .agents/skills/perf-analyze/scripts/jtl_stats.py "jmeter/results/{Scenario}/result.jtl"
   ```
   Append the three tables into `report/perf_report.md` §3.1. These numbers are the reference — never overwrite them after the AI analysis.
2. **AI analysis.** Give the AI the §3.1 tables + run context (threads, ramp-up, hardware). Ask it to: interpret each scenario (did Load hold, where did Stress break, did Spike recover) · compare endpoint groups · suggest performance thresholds · propose 4–6 optimizations (DB index, connection pool, SQLite WAL, caching…). Save verbatim to `report/analysis/ai_analysis_raw.md` — the ONLY extra file this stage creates (audit entries point to it). Do not correct it yet.
3. **Misinterpretation hunt.** Extract every numeric claim from the AI analysis; verify each against the metrics/raw log; classify ✅ correct · ⚠️ imprecise · ❌ wrong. Probe deliberately: avg-vs-p95 confusion · whole-run error rate hiding burst-window errors · recovery claims without checking final minutes · label mix-ups · think-time ignored · invented sample counts. For each ❌: cite the correct value + where it came from in the raw log + why the AI erred.
4. **Optimization judgement.** For each proposal: premise check (is that bottleneck visible in YOUR metrics?) + stack check (does the SUT repo actually use that tech? verify, never assume) → ✅ feasible · ⚠️ valid but unjustified · ❌ hallucinated.

## Output — append §3 to `report/perf_report.md`

```md
## 3. Analysis (Task 2)
### 3.1 Metrics (ground truth)
<jtl_stats.py tables for Load/Stress/Spike, pasted here BEFORE the AI analysis>
### 3.2 AI analysis
<summary; full text: report/analysis/ai_analysis_raw.md>
### 3.3 Misinterpretation hunt
| # | AI claim | Verdict | AI value | Correct value | Evidence |
<per-❌ detail: correct value + source + why the AI erred>
### 3.4 Optimization judgement
| # | Proposal | Verdict | Premise check | Stack check |
## 4. Continuous Performance Testing (Task 3)
<PLACEHOLDER — human-written at closeout: model + flow chart + trade-offs>
```

## Human gate & bookkeeping

Human reviews §3 → `kit-state.md` (`analyze: done` — pipeline complete) · audit entry · git commit. Remaining human-only items: Task 3 §4, AI Critique (200–300 words), demo video upload, README + packaging (see perf-on **Closeout**).
