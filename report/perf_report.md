# HW05 Performance Testing Report
- Student: <name — fill in> · SID: 23127047 · SUT: EShop (backend API, `http://localhost:3000`) · Tool: JMeter 5.6.3 · Date: 20260830

## 1. Test Design

### 1.1 Endpoint map & workflow
Sources: kb/spec.md + kb/api_specification.md, verified live on 2026-08-30.

**Workflow 4 — Admin Order Fulfillment** (team-assigned; non-duplication: other group members handle other workflows). Goal: DB load tolerance when the admin lists, inspects and transitions many orders concurrently.

| # | Group | Endpoint | Method | Auth | Data source | Verified live |
|---|---|---|---|---|---|---|
| 1 | Auth-heavy | `/api/login` | POST | — (returns JWT) | `jmeter/data/users.csv` (admin@eshop.com) | ✅ 200 + JWT |
| 2 | Read-heavy | `/api/admin/orders` | GET | `Authorization: Bearer <token>` | token extracted from #1 | ✅ 200, 8→242 orders |
| 3 | Read-heavy | `/api/orders/:id` | GET | Bearer | `jmeter/data/orders.csv` (pending order ids) | ✅ 200 |
| 4 | Transactional | `/api/admin/orders/:id/status` | PUT | Bearer | `orders.csv` — body `{"status":"confirmed"}` | ✅ 200, persisted |

**Session mechanics.** Single admin account (`admin@eshop.com`). Login returns JWT, extracted by JSON Post-Processor (`$.token`) and injected via HTTP Header Manager (`Authorization: Bearer ${token}`).

**Lockout behaviour & reset.** FR-02: 3 consecutive failed logins lock the account for 30 s. Mitigation: one correct credential row (no invalid-password traffic), login content assertion ("token" in body) makes any lockout immediately visible in results, and between official runs the account is verified unlocked with one manual login (documented in §2).

**Per-group justification.** Auth-heavy: every iteration re-authenticates (JWT issuance cost + the lockout counter under concurrency). Read-heavy: system-wide order list + per-order detail = the two queries an admin console hammers. Transactional: state-machine transition `pending → confirmed` is a write path with validation, matching the workflow goal of bulk order processing.

**Data strategy (one-way state machine).** Transitions are one-way, so each run consumes pending orders. `jmeter/scripts/seed_orders.ps1` creates fresh pending orders via the real cart/checkout flow and rewrites `orders.csv`; the Load plan uses `recycle=false, stopThread=true` so a thread stops rather than hitting an already-consumed id. Data is re-seeded + CSV re-exported immediately before every official run.

**⚠️ kb ↔ live mismatches / bug candidates** (not adjusted in kb):
1. **FR-08 violation — client-supplied `total_amount` accepted.** Checkout was called with `total_amount: 0` while the cart held a 30,000,000 ₫ item; the order was stored with `total_amount = 0`. Spec: "Backend phải tự tính lại tổng tiền; không chấp nhận giá trị `total_amount` do client gửi lên."
2. **SEC-01 related — login response leaks the full user record**, including `password` (appears plaintext: `"password":"Admin123!"`), `login_attempts`, `locked_until`. Spec requires passwords never stored/exposed as plaintext.

### 1.2 Load profiles

Only the **Load** plan is designed so far (Stress/Spike cloned later — identical workflow, only Thread Group + listener differ).

| Plan | Threads | Ramp-up | Duration/loops | Listener (R4) |
|---|---|---|---|---|
| Load | 20 | gradual, 60 s | 5 loops (~70 s) | Aggregate Report |
| Stress | TBD (later stage) | step-wise | until errors rise | Summary Report |
| Spike | TBD (later stage) | 0–1 s | 1–2 min | View Results Tree |

Load justifications:
- **20 threads** — moderate concurrency for a laptop-class load generator; the SUT is local single-process Node+SQLite, so 20 concurrent admins already stresses the shared account path and SQLite write lock.
- **60 s ramp-up** — avoids a thundering-herd login wave that would measure JMeter thread startup rather than the SUT.
- **5 loops** — exactly 100 samples per sampler (20×5), meeting the ≥100-samples guideline; orders.csv holds 242 pending ids > 100 required PUTs, so `stopThread` never triggers mid-run.
- **Think time 800 ms** — realistic admin pause between actions; keeps request rate believable (~1.2 iter/s per thread).
- **Plan file:** `jmeter/plans/23127047_Load_20260830.jmx`

### 1.3 Human review — what the AI got wrong

| # | What was wrong | Impact | Fix | Why AI missed it |
|---|---|---|---|---|
| 1 | CSV Data Set Configs generated with `ignoreFirstLine=false` while headers were present and `variableNames` set — header row consumed as data | Every other iteration sent `email=email, password=password` → ~50% false 401s; orders header also produced a bogus `/api/orders/order_id` request | Set `ignoreFirstLine=true` in both CSV configs; re-verified: 0% login errors | Endpoint characteristic (CSV semantics) + model assumption that header rows are always skipped; caught by smoke run + response-body trace before any official run |
| 2 | Initial orders.csv was generated once at design time and reused across runs despite the one-way state machine | Stale confirmed ids → 400 "invalid transition" errors (50% PUT failures in a validation run) | Seed script now rewrites `orders.csv` on every re-seed; re-seed + re-export before each official run | Model did not track state consumption across repeated runs (no memory of data lifecycle between invocations) |

## 2. Test Execution
<to be appended by perf-run>

## 3. Analysis (Task 2)
<to be appended by perf-analyze>

## 4. Continuous Performance Testing (Task 3) <PLACEHOLDER — human-written at closeout>
