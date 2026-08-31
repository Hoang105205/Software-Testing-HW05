# AI Audit Report

I use AI tools for the following tasks:

## Entry 1

### AI tool name
* Qoder (perf-on + perf-design skills, HW05 kit)

### Date and time
* 2026-08-30 13:55

### Prompt
```text
perf-on Load, hãy start từng stage
Workflow 4 — Quản trị viên Vận hành Đơn hàng & State Machine (Admin Order Fulfillment):
1. [Auth-heavy] POST /api/login (admin@eshop.com)
2. [Read-heavy] GET /api/admin/orders -> GET /api/orders/:id
3. [Transactional] PUT /api/admin/orders/:id/status (pending -> confirmed -> shipping)
```

### The AI output
```text
Stage 1 (perf-design) executed for plan-type Load:
- kb read (spec.md + api_specification.md); all 4 endpoints verified live against http://localhost:3000
- Seeded 242 pending orders via real cart/checkout flow (jmeter/scripts/seed_orders.ps1) and exported jmeter/data/orders.csv; jmeter/data/users.csv holds the admin credential
- Generated jmeter/plans/23127047_Load_20260830.jmx (20 threads, 60 s ramp-up, 5 loops, think time 800 ms, Aggregate Report listener, JWT extraction + Bearer header, response-code + content assertions)
- Smoke run exposed an AI defect: CSV configs with ignoreFirstLine=false consumed header rows as data -> 50% false 401s; fixed (ignoreFirstLine=true) and re-verified (0% login errors). Second finding: stale orders.csv caused 400s on already-confirmed ids; seed script now rewrites the CSV every re-seed
- 2 bug candidates recorded: FR-08 total_amount accepted from client; login response leaks user.password
- report/perf_report.md section 1 written
```

---

## Entry 2

### AI tool name
* Qoder (teach-mode Stage 2 + endurance analysis, HW05 kit)

### Date and time
* 2026-08-31 (session spanning 08-30 evening to 08-31)

### Prompt
```text
teach me step by step how to run manually (Stage 2), do not do it yourself;
then: determine the endurance threshold, run a 10-min soak, analyze it;
then: clean up unneeded files, design the Stress/Spike workflow;
then: commit the Load + endurance work in meaningful per-step commits
```

### The AI output
```text
Stage 2 (perf-run) executed in teach-mode: human ran the scenarios in the JMeter GUI, AI verified and analyzed:
- Load run verified: 400 samples, 0.00% errors, 20/20 active threads, HTML report complete, same-frame screenshots + hardware evidence (DESKTOP-N7HAG7L) accepted; leftover diag scripts deleted
- Endurance: AI wrote jmeter/scripts/endurance_windows.py (1-min windows + threshold rule); human ran 10-min soak (10 threads, scheduler 600 s, ~2000 seeded orders). Result: ~12.2 RPS sustained, 0% errors, p95 flat 22-29 ms; memory ceiling ~71 MB (backend node.exe identified as owner of port 3000; idle growth to ~110 MB flagged as leak candidate). report/endurance_threshold.md written
- Cleanup: deleted endurance working clone, run.log, jmeter.log; removed an Endurance thread group that had leaked into the Load plan (official Load .jtl verified untouched); fixed Stress ramp/loops defect (30/3 -> 10/6, same ramp>lifetime trap as Load - recorded as AI mistake #3 in report 1.3); set Stress/Spike listener filenames; created results dirs
- Diagnosed human's accidental GUI edit of the Load plan as unsaved in-memory change (disk file pristine) and taught the discard/reopen drill
- 7 per-step git commits created (design / scripts / report / audit / Load run / endurance / threshold); Stress+Spike plans left unstaged for their own runs
```

---
