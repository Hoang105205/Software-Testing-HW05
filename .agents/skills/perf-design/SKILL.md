---
name: perf-design
description: Stage 1 of the HW05 kit. Gathers SUT context, maps endpoints into the three groups, then designs and generates the three CSV-driven JMeter plans (Load/Stress/Spike) and records the human-review findings. Use when the user says "perf-design" or wants to create the performance test plans.
---

# Stage 1 — design (context + plans + review, one stage)

Goal: endpoint map → 3 named `.jmx` plans → reviewed, with AI mistakes documented. Creates `report/perf_report.md` §1.

## Input

- **kb (read first, READ-ONLY — never edit):** `kb/api_specification.md` = endpoint reference (base URL `http://localhost:3000`, methods, payloads, auth header `Authorization: Bearer <token>`); `kb/spec.md` = feature spec (behaviour basis, incl. the 3-fail account lockout).
- Running SUT to verify kb claims against reality.
- From the human: `{SID}`, `{DATE}` (YYYYMMDD), and group members' workflow choices (must not duplicate).

## Steps

1. **Context.** From `kb/api_specification.md` + `kb/spec.md`, map the SUT endpoints for: login (note 3-fail lockout), product list/search, product detail, add-to-cart, checkout. Note the session mechanism (JWT via `Authorization: Bearer`) and which response fields must be extracted for later requests. Then **verify each endpoint live** with a quick cURL/Postman probe; any kb ↔ live mismatch (status, payload shape, behaviour) is recorded as a ⚠️ bug candidate in §1.1 — do not adjust kb.
2. **CSV data.** `jmeter/data/users.csv` (≥5 accounts — spreads threads to limit lockout collisions) and `jmeter/data/products.csv` (existing product IDs / search keywords).
3. **Base plan.** Thread Group · HTTP Request Defaults · Cookie/Header Manager · 2× CSV Data Set Config · requests in E2E order · post-processors for token/cart/order dependencies · response-code + content assertions (login content assertion makes lockouts visible) · think-time Timer.
4. **Clone ×3** — change ONLY Thread Group + listener; save to `jmeter/plans/` as `{SID}_{Load|Stress|Spike}_{DATE}.jmx` (R2):

   | Plan | Threads | Ramp-up | Duration | Listener (R4) |
   |---|---|---|---|---|
   | Load | moderate (~20) | gradual (~60 s) | 3–5 min | Aggregate Report |
   | Stress | high (~60–100) | step-wise | until errors rise | Summary Report |
   | Spike | burst (~80) | 0–1 s | 1–2 min | View Results Tree |

   Tune to the human's hardware; justify every number.
5. **Self-review (graded).** Walk the checklist WITH the human: realistic ramp-up/think-time? plausible thread count? ≥100 samples per request? CSV paths + sharing mode? lockout detectable? assertions/extractors match real responses? listener + filename per plan? Fix defects, and for EACH record: what was wrong → impact → fix → why AI missed it (prompt quality / model limitation / endpoint characteristic).

## Output

Append §1 to `report/perf_report.md`:

```md
# HW05 Performance Testing Report
- Student: <name> · SID: {SID} · SUT: EShop · Tool: JMeter · Date: {DATE}

## 1. Test Design
### 1.1 Endpoint map & workflow
Sources: kb/spec.md + kb/api_specification.md, verified live on <YYYY-MM-DD>
| # | Group | Endpoint | Method | Auth | Data source | Verified live |
<session mechanics · lockout behaviour & reset method · per-group justification · non-duplication declaration · ⚠️ kb ↔ live mismatches (bug candidates)>
### 1.2 Load profiles
<the table from step 4 with justifications>
### 1.3 Human review — what the AI got wrong
| # | What was wrong | Impact | Fix | Why AI missed it |
```

## Human gate & bookkeeping

Human approves plans → update `kit-state.md` (`design: done`) · append audit entry (perf-on format) · git commit. Next: `/perf-run`.
