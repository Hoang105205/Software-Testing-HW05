# HW05 Kit State

## Workflow (from /perf-on argument)
**Workflow 4 — Admin Order Fulfillment** (goal: DB load tolerance when admin confirms/transitions many orders concurrently)

| # | Group | Endpoint |
|---|---|---|
| 1 | Auth-heavy | `POST /api/login` (admin@eshop.com) |
| 2 | Read-heavy | `GET /api/admin/orders` → `GET /api/orders/:id` |
| 3 | Transactional | `PUT /api/admin/orders/:id/status` (`pending → confirmed → shipping`) |

## Active scope
- plan-type: **Load** (submission later also requires Stress + Spike)
- mode: one stage at a time, human gate between stages

## Stages
- [ ] design (perf-design) ← Load plan generated + smoke-verified, AWAITING HUMAN APPROVAL
- [ ] run (perf-run)
- [ ] analyze (perf-analyze)

## Inputs from human
- `{SID}` = 23127047 · `{DATE}` = 20260830
- SUT confirmed UP at `http://localhost:3000` (probe 2026-08-30: POST /api/login → 401 on bad password = endpoint alive)

## Audit entries
- Entry 1 (2026-08-30 13:55) — perf-design Load: plan + CSVs + §1, 2 AI defects found & fixed, 2 bug candidates
