# HW05 Kit State

## Workflow (from /perf-on argument)
**Workflow 4 — Admin Order Fulfillment** (goal: DB load tolerance when admin confirms/transitions many orders concurrently)

| # | Group | Endpoint |
|---|---|---|
| 1 | Auth-heavy | `POST /api/login` (admin@eshop.com) |
| 2 | Read-heavy | `GET /api/admin/orders` → `GET /api/orders/:id` |
| 3 | Transactional | `PUT /api/admin/orders/:id/status` (`pending → confirmed → shipping`) |

## Active scope
- plan-type: **all** (Load + Stress + Spike) — submission scope complete
- mode: one stage at a time, human gate between stages

## Stages
- [x] design (perf-design) — 3 plans + CSVs + §1 (incl. §1.3 AI mistakes), human-approved
- [x] run (perf-run) — Load/Stress/Spike official runs + endurance soak, evidence committed
- [x] analyze (perf-analyze) — §3 (ground truth + AI analysis + hunt + judgement) + §4 Task 3 written — **pipeline complete**

Remaining human-only items: AI Critique (200–300 words), demo video upload, README + packaging (zip Moodle vs GitHub).

## Inputs from human
- `{SID}` = 23127047 · `{DATE}` = 20260830
- SUT confirmed UP at `http://localhost:3000` (probe 2026-08-30: POST /api/login → 401 on bad password = endpoint alive)

## Audit entries
- Entry 1 (2026-08-30 13:55) — perf-design Load: plan + CSVs + §1, 2 AI defects found & fixed, 2 bug candidates
- Entry 2 — teach-mode run stage, Load verification, endurance analysis, cleanup/decontamination, commits
- Entry 3 — Stress run verification + commits
- Entry 4 — orders.csv integrity check + Spike run verification
- Entry 5 — demo kit explanation + manual re-run ceremony + demo script
- Entry 6 — post-demo revert + Spike commits
- Entry 7 (2026-09-01) — perf-analyze: ground truth, AI analysis, misinterpretation hunt, optimization judgement, §4 Task 3
