# 🧪 ĐỒ ÁN THỰC HÀNH 05: KIỂM THỬ HIỆU NĂNG & HỢP TÁC VỚI AI (PERFORMANCE TESTING & AI COLLABORATION)

* **Sinh viên thực hiện:** Lưu Huy Hoàng  
* **Mã số sinh viên (MSSV):** 23127047  
* **Học phần:** Kiểm thử phần mềm (Software Testing)  
* **Hệ thống SUT:** EShop Platform — Backend API (Node.js Express 5 + SQLite) tại `http://localhost:3000`  
* **Workflow kiểm thử:** **Workflow 4 — Admin Order Fulfillment** (login → list orders → order detail → PUT status `pending → confirmed`)  
* **GitHub Repository:** [Hoang105205/Software-Testing-HW05](https://github.com/Hoang105205/Software-Testing-HW05)  
* **Ngày thực hiện:** 2026-08-30 → 2026-09-01

---

## BẢNG TỰ CHẤM ĐIỂM CHI TIẾT (SELF-ASSESSMENT)

| STT | Hạng mục / Tiêu chí Đánh giá (Rubric) | Trọng số | Tự chấm | Minh chứng & Trạng thái Hoàn thành |
| :---: | :--- | :---: | :---: | :---|
| **1** | **Task 1 — Load Testing**<br>• Plan `23127047_Load_20260830.jmx` (20 VUs, ramp-up 10 s, 5 loops, think time 800 ms).<br>• Data-driven CSV (`users.csv` + `orders.csv` re-seed trước mỗi run).<br>• Listener: *Aggregate Report*.<br>• Raw log `.jtl` + HTML Dashboard + screenshot tool & Task Manager cùng khung hình. | **30** | `27/30` | `jmeter/plans/` · `jmeter/results/Load/` · [Main Report.md](Main%20Report.md) §2.1 |
| **2** | **Task 1 — Stress Testing**<br>• Plan `23127047_Stress_20260830.jmx` (60 VUs, ramp-up 10 s, 6 loops).<br>• Listener: *Summary Report*; verify đủ 60/60 thread hoạt động.<br>• Phát hiện vùng *knee* latency (p95 60 ms, tail 633 ms) với 0% lỗi. | **20** | `18/20` | `jmeter/results/Stress/` · [Main Report.md](Main%20Report.md) §2.2 |
| **3** | **Task 1 — Spike Testing**<br>• Plan `23127047_Spike_20260830.jmx` (80 VUs, ramp-up 1 s, 1 loop).<br>• Listener: *View Results Tree*; burst 320 request hấp thụ trọn vẹn 0% lỗi.<br>• **Endurance threshold:** soak 10 phút → RPS ổn định tối đa **≈ 12.2**, trần bộ nhớ backend **≈ 71 MB**. | **20** | `18/20` | `jmeter/results/Spike/` · [Main Report.md](Main%20Report.md) §2.3–2.4 |
| **4** | **Task 2 — AI Analysis & Misinterpretation Hunt**<br>• Ground truth trích từ `.jtl` thô trước khi hỏi AI (`jtl_stats.py`).<br>• Săn lỗi hiểu sai: 3 ❌ (avg đọc thành p95 · "login nhanh nhất" sai · bịa "≥100 samples") + 2 ⚠️.<br>• Phán quyết 5 đề xuất tối ưu đối chiếu mã nguồn SUT: 2 ✅ feasible (WAL, gzip) · 1 ❌ hallucinated (connection pool) · 2 ⚠️ không cơ sở dữ liệu. | **10** | `8/10` | [Main Report.md](Main%20Report.md) §III.2–III.3 · `report/analysis/ai_analysis_raw.md` |
| **5** | **Task 3 — Continuous Performance Testing (G9.6)**<br>• Mô hình theo dõi commit với path filter `backend/**` + nightly run.<br>• Quality Gate: p95 > 1.2× baseline HOẶC error > 1% → flag regression.<br>• Baseline trung vị trượt 5 run xanh; thảo luận trade-offs (chi phí / false alarm / false negative). | **10** | `10/10` | [Main Report.md](Main%20Report.md) §IV |
| **6** | **Agent Skills — perf kit (4 skill)**<br>• `perf-on` (orchestrator) + `perf-design` / `perf-run` / `perf-analyze`.<br>• Human gate giữa các stage; tiến độ theo dõi trong `kit-state.md`; audit entry sau mỗi stage.<br>• Video demo skill end-to-end. | **10** | `9/10` | `.agents/skills/` · video demo số 2 |
| **TỔNG** | **TỔNG ĐIỂM TỰ ĐÁNH GIÁ** | **100** | `90/100` | *(con số này cũng là hậu tố của tên file zip nộp bài)* |

---

## LIÊN KẾT VIDEO DEMO (YOUTUBE UNLISTED)

1. **Video 1 — Thực nghiệm Kiểm thử Hiệu năng & Giám sát Tài nguyên (Task 1):**  
   - **Thời lượng:** ≥ 6 phút, thuyết minh tiếng Việt, JMeter + Task Manager cùng khung hình.  
   - **Link:** [https://youtu.be/6-3ojgsETVo](https://youtu.be/6-3ojgsETVo)
2. **Video 2 — Demo Agent Skill (perf kit) end-to-end:**  
   - **Thời lượng:** 2–3 phút.  
   - **Link:** [https://youtu.be/hNKRIW8gXgM](https://youtu.be/hNKRIW8gXgM)

---

## TÓM TẮT KỊCH BẢN & KẾT QUẢ ĐO ĐẠC

### 1. Luồng nghiệp vụ E2E (phủ đủ 3 nhóm endpoint, không trùng thành viên khác trong nhóm)

* **Auth-heavy:** `POST /api/login` (admin@eshop.com → JWT, mỗi iteration đăng nhập lại).
* **Read-heavy:** `GET /api/admin/orders` (full scan + JOIN, payload ~64 KB) và `GET /api/orders/:id`.
* **Transactional:** `PUT /api/admin/orders/:id/status` (`pending → confirmed`, state machine một chiều — CSV re-seed trước mỗi run).

### 2. Ma trận kịch bản & kết quả (ground truth từ raw `.jtl`)

| Chỉ số | Load (20 VUs/10 s/5 loops) | Stress (60 VUs/10 s/6 loops) | Spike (80 VUs/1 s/1 loop) | Endurance (10 VUs/10 phút) |
| :--- | :---: | :---: | :---: | :---: |
| **Tổng samples** | 400 | 1.440 | 320 | 7.286 |
| **Throughput** | **16.03 req/s** | **50.12 req/s** | **92.62 req/s** | **≈ 12.2 req/s (ổn định ±1%)** |
| **Tỷ lệ lỗi** | **0.00%** | **0.00%** | **0.00%** | **0.00%** |
| **p95 tổng** | **17 ms** | **60 ms** | **29 ms** | phẳng 22–29 ms |
| **Max latency** | 25 ms | 633 ms (PUT) | 47 ms | — |
| **Listener (R4)** | Aggregate Report | Summary Report | View Results Tree | — |

**Endurance threshold trên hardware này (DESKTOP-N7HAG7L, OptiPlex 7040 i7-6700/32 GB):** RPS ổn định tối đa ≈ **12.2** · trần bộ nhớ backend ≈ **71 MB** · điểm gãy chưa đạt tới ở mức tải khảo sát.

**Vấn đề ghi nhận:** 3 vấn đề hiệu năng (serialization đường ghi SQLite · admin list query không giới hạn · memory tăng khi idle nghi vấn leak) + 2 bug chức năng/bảo mật (FR-08 `total_amount`, SEC-01 lộ password) — chi tiết tại [Main Report.md](Main%20Report.md) §III.4.

---

## SĂN LỖI ẢO TƯỞNG CỦA AI (TASK 2 — MISINTERPRETATION HUNT)

Đối chiếu với số liệu `.jtl` thô và mã nguồn SUT (`backend/database.js`, `package.json`, `server.js`), AI bộc lộ **3 lỗi sai + 2 diễn đạt quá mức + 1 đề xuất hallucinated**:

1. **Trích *average* làm p95:** AI nói Load p95 ≈ 6 ms — đúng ra là **17 ms** (understate tail risk 3×).
2. **Bịa bảo chứng thống kê:** "mọi label ≥ 100 samples" — Spike chỉ có **80 samples/label** theo thiết kế burst.
3. **Hallucinated optimization — connection pool:** SUT dùng SQLite *embedded* sau một handle duy nhất, không phải client–server DB; pooling chỉ thêm contention.
4. **Đề xuất "vàng" bị AI bỏ quên:** bật **SQLite WAL** — trong khi PUT p95 91 ms dưới Stress chính là triệu chứng rollback-journal kinh điển (được xác nhận ✅ feasible).

---

## ĐỀ XUẤT CONTINUOUS PERFORMANCE TESTING (TASK 3)

* **Triggering:** commit/PR chạm `backend/**` → CI job (seed → headless JMeter → `jtl_stats.py`); commit chỉ đụng docs/frontend → skip; nightly cron bắt environment drift.
* **Quality Gate:** `p95 > 1.2× baseline` HOẶC `error > 1%` → flag regression (PR comment + Issue) với luật confirm-on-second-run; ngược lại cập nhật baseline = trung vị trượt 5 run xanh.
* **Xử lý đặc thù:** state machine một chiều → re-seed trước mỗi CI run; một credential duy nhất → lockout không thể xảy ra trong CI; nightly luân phiên Load/Stress để không lọt regression đường ghi.
* Sơ đồ luồng đầy đủ (Mermaid) + trade-offs: [Main Report.md](Main%20Report.md) §IV.

---

## HƯỚNG DẪN SỬ DỤNG AGENT SKILL (`.agents/skills/`)

Bộ kit 4 skill vận hành pipeline design → run → analyze, mỗi stage có human gate:

```text
/perf-on Workflow 4 Admin Order Fulfillment Load      # khởi động + scope kịch bản
/perf-design                                          # sinh plan + CSV, self-review cùng human
/perf-run                                             # quy trình chạy + verify bằng chứng
/perf-analyze                                         # ground truth → AI analysis → hunt → judgement
```

Phân tích một file `.jtl` bất kỳ trực tiếp:

```bash
python .agents/skills/perf-analyze/scripts/jtl_stats.py "jmeter/results/Load/result.jtl"
```

---

## CẤU TRÚC THƯ MỤC NỘP BÀI (PROJECT STRUCTURE)

```
23127047_HW05/
├── submission/
│   ├── README.md                                   # File này — tổng quan + bảng tự chấm
│   ├── Main Report.md                              # Báo cáo chính Task 1–3 (Markdown)
│   ├── Main Report.pdf                             # Bản PDF của báo cáo chính
│   ├── perf_summary_report.md                      # Tóm tắt số liệu + Quality Gate
│   ├── git_commit_log.txt                          # Lịch sử git commit dạng text
│   └── AI Template/
│       ├── AI_Audit_Report.md                      # Nhật ký tương tác AI (7 entries)
│       └── AI Critique.md                          # Bài phản biện AI 200–300 từ
├── jmeter/
│   ├── plans/
│   │   ├── 23127047_Load_20260830.jmx              # Load (20 VUs) — Aggregate Report
│   │   ├── 23127047_Stress_20260830.jmx            # Stress (60 VUs) — Summary Report
│   │   └── 23127047_Spike_20260830.jmx             # Spike (80 VUs) — View Results Tree
│   ├── data/
│   │   ├── users.csv                               # Credential admin (1 dòng duy nhất)
│   │   └── orders.csv                              # Order id pending — re-export mỗi lần seed
│   ├── scripts/
│   │   ├── seed_orders.ps1                         # Tạo đơn qua luồng cart/checkout thật
│   │   ├── probe_workflow.ps1                      # Probe endpoint live trước khi design
│   │   └── endurance_windows.py                    # Phân tích soak theo cửa sổ 1 phút
│   └── results/
│       ├── Load/  Stress/  Spike/                  # result.jtl + html_report/ + screenshots/
│       ├── Endurance/result.jtl                    # Soak 10 phút
│       └── hardware/hardware_evidence.png          # Báo cáo phần cứng
├── report/
│   ├── perf_report.md                              # Phân tích chi tiết §1–§4
│   ├── endurance_threshold.md                      # Báo cáo endurance threshold
│   └── analysis/ai_analysis_raw.md                 # AI analysis nguyên bản (chưa chỉnh sửa)
├── audit/AI_Audit_Report.md                        # Nhật ký audit (bản gốc trong repo)
├── .agents/skills/                                 # perf-on · perf-design · perf-run · perf-analyze
├── kit-state.md                                    # Trạng thái pipeline của kit
└── kb/                                             # spec.md + api_specification.md (READ-ONLY)
```

---

## HƯỚNG DẪN CÀI ĐẶT & TÁI HIỆN THỰC NGHIỆM (REPRODUCIBILITY GUIDE)

1. **Khởi động Backend SUT:**
   ```bash
   cd eshop-sut/backend
   npm install
   npm start
   # Server lắng nghe tại http://localhost:3000
   ```
2. **Nạp dữ liệu đơn hàng (state machine một chiều — bắt buộc trước mỗi run):**
   ```powershell
   # Load: 150 · Stress: 400 · Spike: 100 (luôn dư biên so với số PUT tiêu thụ)
   powershell -ExecutionPolicy Bypass -File jmeter\scripts\seed_orders.ps1 -Count 150
   ```
3. **Chạy kịch bản (GUI như lúc quay demo, hoặc headless):**
   ```bash
   # GUI: mở file .jmx tương ứng trong jmeter/plans/ rồi Start
   # Headless:
   jmeter -n -t "jmeter/plans/23127047_Load_20260830.jmx" -l jmeter/results/Load/result.jtl
   ```
4. **Sinh HTML Dashboard & phân tích:**
   ```bash
   jmeter -g jmeter/results/Load/result.jtl -o jmeter/results/Load/html_report
   python .agents/skills/perf-analyze/scripts/jtl_stats.py "jmeter/results/Load/result.jtl"
   ```
