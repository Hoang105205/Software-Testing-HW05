# HW05 Performance Testing — Agent Skill Kit (slim)

3-stage JMeter pipeline for the EShop SUT, modeled on the HW04 auto-script-kit: one orchestrator, one stage skill per step, an audit entry after every stage.

```
perf-on ──► perf-design ──► perf-run ──► perf-analyze ──► perf-on Closeout
            (context+plans)   (3 runs+soak)   (Task 2)      (Task 3 + packaging)
```

| Skill | Stage | Produces |
|---|---|---|
| `perf-on` | orchestrator | `kit-state.md` tracking, audit format, hard rules R1–R9, closeout & zip filter |
| `perf-design` | 1 | endpoint map (from `kb/spec.md` + `kb/api_specification.md`, verified live) + `{SID}_{Type}_{DATE}.jmx` ×3 + CSVs + report §1 (incl. "what AI got wrong") |
| `perf-run` | 2 | `.jtl` + HTML reports + screenshots + endurance threshold → report §2 |
| `perf-analyze` | 3 | metrics (pasted into §3.1 via `scripts/jtl_stats.py`) + AI analysis + misinterpretation hunt + optimization verdicts → report §3 |

Shared conventions: single report file `report/perf_report.md` (appended §1→§2→§3; §4 Task 3 is human-written at closeout), audit log at `audit/AI_Audit_Report.md` (Entry format per homework template), results under `jmeter/results/<Scenario>/`, one git commit per stage, backend API via JMeter only. After `analyze: done`, perf-on **Closeout** re-scans the requirement and packages the Moodle zip — the ENTIRE project goes to GitHub, but the zip is a FILTERED subset (table in perf-on).

Usage: invoke **"perf-on"** to see progress and get the next stage, or call a stage skill directly. Human-only evidence (demo video, live screenshots, dxdiag) is reminded by the kit but cannot be automated.
