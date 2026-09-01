# AI Analysis — raw output (unreviewed)

Prompt given to the AI: the three ground-truth tables (report §3.1) + run context (Load 20 threads/10 s ramp/5 loops; Stress 60/10/6; Spike 80/1/1; think time 800 ms; HW: OptiPlex 7040 i7-6700, 32 GB RAM, SUT = single-process Node/Express + SQLite on the same machine). The AI's verbatim response follows; it has NOT been corrected here — corrections live in report §3.3/§3.4.

---

Looking at your three scenarios, the system behaves like a small but healthy single-node API. Under Load it held a steady ~16 RPS with an overall p95 of about 6 ms and zero errors, which shows the baseline path is fast and stable. Stress at 60 threads pushed throughput to ~50 RPS — roughly 3.1× the Load throughput, near-linear scaling for a 3× concurrency increase — but this is where the system began to break: maximum latency reached 633 ms and the admin order list p95 quadrupled from 16 ms to 68 ms, so 60 concurrent admins is close to the knee of the curve. The Spike burst was absorbed well: 320 requests in 3.5 s (~92.6 RPS) with latencies returning to Load levels, proving the system recovers after a shock.

Comparing endpoint groups, login (the auth-heavy call) is the fastest endpoint in all three scenarios (4–16 ms avg) because JWT signing is cheap and the users table is tiny; the read-heavy admin list is the most latency-sensitive read (7–22 ms avg, p95 up to 68 ms) because it full-scans and joins the growing orders table; the transactional PUT is the slowest under Stress (p95 91 ms) because SQLite serializes writers.

Suggested thresholds for this hardware: p95 < 100 ms per endpoint, error rate < 1 %, and sustained throughput of at least 12 RPS (your endurance soak held ~12.2 RPS for 10 minutes). Every label in every scenario collected at least 100 samples, so these numbers are statistically usable.

Optimizations I recommend:
1. Enable SQLite WAL mode — removes writer/reader blocking; your PUT p95 of 91 ms under Stress is the classic rollback-journal symptom.
2. Add a connection pool for the database — Express handlers currently wait on a single DB connection, so pooling would let the 60 Stress threads be served in parallel.
3. Add database indexes on orders(status) and orders(user_id) — the admin list and detail lookups will degrade linearly as the orders table grows.
4. Enable gzip compression on the admin order list — each response is ~64 KB of JSON; compression cuts transfer size ~80 %.
5. Cache the admin order list in memory for a few seconds — it is your hottest read endpoint and its content tolerates short staleness.
