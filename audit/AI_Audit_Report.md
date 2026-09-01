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

## Entry 3

### AI tool name
* Qoder (run verification + commits)

### Date and time
* 2026-08-31

### Prompt
```text
I have just run for stress test plan. Before running for spike, please help me verify the result
and split meaningful commits for stress test plan task
```

### The AI output
```text
- Stress run verified: 1,440 samples (60x6x4), 0.00% errors, 60/60 active threads, 28.7 s; latency 3-4x Load (p95 46-91 ms) but zero failures = "degraded but never broke"; HTML report + 3 screenshots cross-checked against the .jtl
- Committed in two steps: test(perf): add Stress plan / add Stress run results and evidence
```

---

## Entry 4

### AI tool name
* Qoder (data integrity + Spike verification)

### Date and time
* 2026-08-31

### Prompt
```text
after seed, orders.csv is oke?
then revify for me the result [Spike]
```

### The AI output
```text
- orders.csv integrity checked before Spike: 140 pending ids (100 fresh + leftovers, all exported by the seed filter); spot-check via live API confirmed status=pending; AI's first check used a wrong JSON property path ($o.order.status) and was self-corrected to the root-level status field
- Spike run verified: 320 samples (80x1x4), 0.00% errors, 80/80 threads in a 3.5 s burst (~92.6 RPS); HTML report + screenshots present
- Evidence nit flagged to the human: tool.png captured an earlier run (08:56:50) while the official .jtl holds a second run (08:57:14) - both green; human accepted as-is
```

---

## Entry 5

### AI tool name
* Qoder (demo preparation)

### Date and time
* 2026-09-01

### Prompt
```text
toi dang can demo bo agent skill - hay giup toi biet cac skill trong bo kit va vai tro
bay gio toi can demo chay 3 test plan manually: step by step, command seed, command sinh html + goi y script demo
```

### The AI output
```text
- Produced the kit map for the demo narration: perf-on (orchestrator, workflow-as-argument, human gates, audit enforcement) / perf-design (Stage 1) / perf-run (Stage 2) / perf-analyze (Stage 3), plus shared state files (kit-state.md, audit, report)
- Wrote the per-plan manual re-run ceremony (seed counts 150/400/100, HTML report commands, expected sample/thread counts) and a >=6-min Vietnamese demo script mapping every project file to its role
```

---

## Entry 6

### AI tool name
* Qoder (post-demo revert + Spike commits)

### Date and time
* 2026-09-01

### Prompt
```text
toi vua demo chay manual lai cho load va stress... bay gio toi se revert lai voi dung cai ta commit - giup toi
ok [commit Spike], dong thoi gom doan chat vao ai audit log
```

### The AI output
```text
- Demo re-runs had overwritten tracked artifacts; reverted with git restore (orders.csv, Load plan re-saved by GUI, results/Load incl. HTML report, results/Stress/result.jtl) back to the committed official state; verified Load=400 and Stress=1,440 rows again; Spike artifacts untouched (untracked)
- Committed Spike in two steps: test(perf): add Spike plan / add Spike run results and evidence - all three scenarios now committed; working tree clean
```

---
