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
