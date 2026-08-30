# HW05 Checklist — Performance Testing with JMeter (progress tracker)

> Tool: **JMeter** · SUT: EShop (already running) · Kit: `.agents/` (`perf-on` → `perf-design` → `perf-run` → `perf-analyze` → Closeout)
> Naming: `{SID}` = StudentID · `{DATE}` = YYYYMMDD

---

## 📦 My workflow — [ADMIN] Workflow 4: Admin Order Fulfillment

> Purpose: DB load capacity when Admin approves and transitions many orders concurrently.
> Non-duplication: confirmed with team — no other member tests this workflow.

| # | Group | Endpoint | Notes |
|---|---|---|---|
| 1 | Auth-heavy | `POST /api/login` | admin account `admin@eshop.com` (mind 3-fail lockout) |
| 2 | Read-heavy | `GET /api/admin/orders` → `GET /api/orders/:id` | list all orders, then view each order detail |
| 3 | Transactional | `PUT /api/admin/orders/:id/status` | state machine: `pending → confirmed → shipping` |

Design-time notes (resolve in `perf-design`):
- Single admin account → think about lockout risk under many threads + how to parameterize credentials (CSV).
- Orders must exist before status updates → data setup strategy (seed/reset DB, or create orders first).
- Status transitions are one-way → each iteration needs fresh `pending` orders (or DB reset between runs).

---

## Progress

### Phase 0 — Repo & coordination
- [ ] GitHub repo created; commit after every step

### Phase 1 — Design (kit: `perf-design`)
- [ ] Endpoint map verified live (kb + probes) → report §1.1
- [ ] CSVs + 3 plans: `{SID}_Load_{DATE}.jmx` / `_Stress_` / `_Spike_`
- [ ] Distinct listeners: Load → Aggregate · Stress → Summary · Spike → View Results Tree
- [ ] Human review + "what AI got wrong" table → report §1.3

### Phase 2 — Execution & evidence (kit: `perf-run`)
- [ ] Hardware evidence once: dxdiag + spec table (hostname matches previous HWs)
- [ ] Load run: `.jtl` + HTML report + same-frame screenshot (JMeter + Task Manager)
- [ ] Stress run: same evidence
- [ ] Spike run: same evidence (lockout reset if triggered, documented)
- [ ] Endurance soak 10–15 min → threshold numbers (max stable RPS, memory ceiling)
- [ ] Demo video ≥6 min, Vietnamese narration, uploaded unlisted
- [ ] Bugs (if any) → GitHub Issues with screenshots

### Phase 3 — Analysis (kit: `perf-analyze`, Task 2)
- [ ] Ground-truth metrics in report §3.1 (before AI analysis)
- [ ] AI analysis saved verbatim
- [ ] Misinterpretation hunt with cited correct values
- [ ] Optimization verdicts: feasible vs hallucinated

### Phase 4 — Closeout (kit: `perf-on` Closeout)
- [ ] Task 3: continuous perf-testing proposal + flow chart → report §4
- [ ] AI Critique 200–300 words
- [ ] PDFs: report · AI Audit Report · critique
- [ ] `git_commit_log.txt` exported
- [ ] README.md: self-assessment table + test summary + video links
- [ ] Skill demo video uploaded
- [ ] Zip filtered per kit table → `{SID}_HW05_AI_Performance_{grade}.zip` → Moodle

---

## ⚠️ Hard-fail traps
Wrong plan filenames · missing any document · `.jtl` not full raw · video without same-frame monitor + own voice · hostname mismatch · copied prompts.
