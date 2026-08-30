---
name: perf-on
description: Orchestrates the 3-stage JMeter performance-testing pipeline for HW05 (design → run → analyze) for any backend API workflow passed as its argument, tracks progress in kit-state.md, and enforces the AI Audit Report entry after every stage. Use when the user says "perf-on <workflow description>", "start/continue the kit", or asks which stage is next.
---

# perf-on — Orchestrator

```
/perf-on [<workflow>] [<plan-type>]
```
- `<workflow>` (optional): free text naming the E2E API workflow, e.g. `admin login → GET /api/admin/orders → GET /api/orders/:id → PUT /api/admin/orders/:id/status`. Present in the prompt → use it and store it in the `kit-state.md` header. Missing → reuse the one stored in `kit-state.md`; if none → **ask the human**. Never source the workflow from `plan/checklist.md` — that file is the human's personal tracker, not a kit input.
- `<plan-type>` (optional): `Load` | `Stress` | `Spike`. Present → scope the stage to that single plan/scenario. Missing → **ask the human** which plan to work on next (all three are eventually required for submission). "all" → the full set.

Parse both from the free-form prompt flexibly; confirm your interpretation with the human before starting.

Drives ONE stage at a time, pauses for human approval, appends the audit entry. Pipeline:

```
perf-design  →  perf-run  →  perf-analyze
(context+plans)  (3 scenarios+endurance)  (Task 2 analysis)
```

## Layout

```
kit-state.md                    # stage tracker (this kit)
audit/AI_Audit_Report.md        # mandatory audit log — entry after EVERY stage
report/perf_report.md           # single report, appended stage by stage:
                                #   §1 design · §2 execution · §3 analysis
jmeter/plans/                   # {SID}_{Load|Stress|Spike}_{YYYYMMDD}.jmx
jmeter/data/                    # users.csv, products.csv
jmeter/results/<Scenario>/      # result.jtl, html_report/, screenshots/
kb/                             # READ-ONLY input: spec.md (feature spec) +
                                # api_specification.md (endpoints, base URL :3000)
```

`{SID}` = student ID. SUT: EShop (repo `ttbhanh/eshop-sut`), assumed already running. kb is the design basis but not 100% reliable — any kb ↔ live-SUT mismatch is a bug candidate to record, never silently "corrected".

## On each invocation

1. **Parse the prompt** for `<workflow>` and `<plan-type>` (see Arguments above). Ask the human for whatever is missing instead of guessing; never hardcode either into any skill.
2. Store the resolved workflow in the `kit-state.md` header; note the active plan-type.
3. Read `kit-state.md` (create it if missing). Report stage statuses, propose the next pending stage.
4. Confirm with the human, then direct to the stage skill (pass workflow + plan-type along): `/perf-design` · `/perf-run` · `/perf-analyze`.
5. Stage skills update `kit-state.md`, append `report/perf_report.md`, and append the audit entry themselves. Never redo an approved stage.

## Audit entry (append to `audit/AI_Audit_Report.md` after EVERY stage + significant interaction)

File header, written once:

```md
# AI Audit Report

I use AI tools for the following tasks:
```

Entry format (numbering continues across the file):

```md
## Entry <N>

### AI tool name
* <tool, e.g. Qoder (perf-<stage> skill)>

### Date and time
* <YYYY-MM-DD HH:MM>

### Prompt
\`\`\`text
<the exact prompt / command given to the AI>
\`\`\`

### The AI output
\`\`\`text
<concise factual summary: files created, run numbers, findings, fixes>
\`\`\`

---
```

## Hard rules

- **R1** One shared E2E workflow — the one resolved from the prompt / `kit-state.md` — across all 3 plans; plans differ ONLY in load profile + listener. All three plan types (Load, Stress, Spike) are required for submission; the kit simply allows working on them one at a time.
- **R2** Plan filenames exactly `{SID}_{ScenarioType}_{YYYYMMDD}.jmx`.
- **R3** CSV-driven requests (credentials + workflow data CSVs, values must exist in the live SUT); no hardcoded credentials or IDs.
- **R4** 3 distinct listeners across plans (Load: Aggregate Report · Stress: Summary Report · Spike: View Results Tree).
- **R5** Raw `.jtl` kept in FULL; HTML report generated from it.
- **R6** Account-lockout resets between runs, documented.
- **R7** Every AI interaction logged to `audit/AI_Audit_Report.md`; every stage committed to git.
- **R8** Human-only evidence (cannot be automated): demo video ≥6 min with Vietnamese narration, same-frame JMeter+Task Manager screenshots, dxdiag hardware report. The kit reminds, the human records.
- **R9** Scope guard: this homework tests the **backend API with JMeter** — no UI automation, no extra tools, no artifacts beyond the ones this kit names.

## Closeout (once `analyze: done`) — review loop then pack

Re-scan `requirement/2026.HW05.md` §6/§12/§14 against the artifacts; then finish the human-only items:

1. **Task 3 proposal** (human): append §4 to `report/perf_report.md` — continuous performance-testing model (watch SUT commits → decide run → flag p95 regressions) with a flow chart + trade-offs (cost, false alarms).
2. **AI Critique** (human, 200–300 words): where AI was wrong/biased/incomplete, why it missed it, principle learned — material is ready in §1.3 + §3.3.
3. **Exports**: `report/perf_report.md`, `audit/AI_Audit_Report.md`, AI Critique → PDF each. Git log: `git log --oneline --date=iso > git_commit_log.txt`.
4. **README.md** (repo root): self-assessment table (§15 of the requirement) + test summary — scenarios run, endpoint groups covered, endurance threshold numbers, bug count, demo video link.
5. **Bugs**: any genuine bug/perf issue found during runs → GitHub Issue with screenshot.
6. **Videos**: upload demo video (≥6 min, unlisted) + skill demo video; put both links in README.md + report §2.4.

### GitHub vs Moodle — the submission filter

**Push to GitHub: the ENTIRE project** (plans, data, results, report, audit, kit-state, `.agents/` skill kit, README.md).
**Submit to Moodle: a FILTERED zip** named `{SID}_HW05_AI_Performance_{grade}.zip` (grade = 3 digits 000–100) containing ONLY:

| Zip item | Source |
|---|---|
| Main report (MD + PDF) | `report/perf_report.md` (+ Task 3 §4, AI Critique inside/attached) |
| Public GitHub repo link | README.md §0 |
| 3 test plans | `jmeter/plans/{SID}_{Type}_{DATE}.jmx` |
| 3 raw `.jtl` + 3 HTML report folders | `jmeter/results/{Load,Stress,Spike}/` (full logs, not summaries) |
| Resource-monitor + hardware screenshots | `jmeter/results/*/screenshots/`, `hardware/` |
| Unlisted demo video link | README.md |
| AI Critique + AI Audit Report (MD + PDF) | `audit/AI_Audit_Report.md` + critique file |
| Git commit log | `git_commit_log.txt` |
| Bug report w/ screenshots (if any) | GitHub Issues links + screenshots |
| README.md w/ self-assessment table | repo root |
| Agent Skill + skill demo link | `.agents/` + YouTube link |

Do NOT include in the zip: Endurance working plan clone, `report/analysis/ai_analysis_raw.md`, `kit-state.md`, intermediate files (they stay on GitHub as supporting material).
