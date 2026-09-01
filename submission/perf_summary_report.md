# Performance Test Analysis & Quality Gate Summary

**Sinh viên:** Lưu Huy Hoàng · **MSSV:** 23127047 · **SUT:** EShop backend API (`http://localhost:3000`)  
**Workflow:** 4 — Admin Order Fulfillment (login → list orders → order detail → PUT status pending→confirmed)  
**Thời gian thực thi:** 16:19 30/8/2026 (Load) · 08:26 & 09:17 31/8/2026 (Stress, Spike)  
**Trạng thái Quality Gate:** **PASSED** ✅

---

## 1. Tổng quan Hiệu năng Toàn hệ thống (3 kịch bản chính thức — 2.160 samples)

| Kịch bản | Threads/Ramp | Tổng Samples | Throughput | Tỷ lệ Lỗi | Avg | p50 | p90 | p95 | p99 | Max |
| :---| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Load** (20/10 s/5 loops) | 20 | **400** | **16.03 req/s** | **0.00%** | 6 ms | 5 | 13 | **17** | 20 | 25 |
| **Stress** (60/10 s/6 loops) | 60 | **1.440** | **50.12 req/s** | **0.00%** | 22 ms | 7 | 24 | **60** | 428 | 633 |
| **Spike** (80/1 s/1 loop) | 80 | **320** | **92.62 req/s** | **0.00%** | 10 ms | 7 | 24 | **29** | 45 | 47 |
| **Endurance** (10 threads, 10 phút) | 10 | **7.286** | **≈12.2 req/s** | **0.00%** | p95 phẳng 22–29 ms qua 10 cửa sổ 1 phút | | | | | |

## 2. Chi tiết từng Sampler / Endpoint

Đơn vị latency: ms. Throughput chung của mỗi kịch bản lấy theo bảng §1.

**Load — 20 threads**

| Sampler / API Endpoint | Samples | Error % | Avg | p50 | p90 | p95 | p99 | Max |
| :---| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `1-Login (admin)` — POST /api/login | 100 | 0.00% | 3.99 | 3 | 7 | 9 | 10 | 10 |
| `2-Admin order list` — GET /api/admin/orders | 100 | 0.00% | 7.22 | 6 | 11 | 16 | 18 | 19 |
| `3-Order detail` — GET /api/orders/:id | 100 | 0.00% | 2.05 | 2 | 3 | 5 | 6 | 8 |
| `4-Transition pending->confirmed` — PUT /api/admin/orders/:id/status | 100 | 0.00% | 12.43 | 12 | 18 | 19 | 22 | 25 |

**Stress — 60 threads**

| Sampler / API Endpoint | Samples | Error % | Avg | p50 | p90 | p95 | p99 | Max |
| :---| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `1-Login (admin)` | 360 | 0.00% | 16.38 | 4 | 17 | 46 | 330 | 452 |
| `2-Admin order list` | 360 | 0.00% | 22.39 | 7 | 25 | 68 | 392 | 457 |
| `3-Order detail` | 360 | 0.00% | 14.78 | 3 | 13 | 46 | 330 | 430 |
| `4-Transition pending->confirmed` | 360 | 0.00% | 34.56 | 12 | 31 | 91 | 533 | 633 |

**Spike — 80 threads burst 1 s**

| Sampler / API Endpoint | Samples | Error % | Avg | p50 | p90 | p95 | p99 | Max |
| :---| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `1-Login (admin)` | 80 | 0.00% | 4.99 | 4 | 8 | 11 | 18 | 20 |
| `2-Admin order list` | 80 | 0.00% | 10.80 | 8 | 23 | 27 | 31 | 33 |
| `3-Order detail` | 80 | 0.00% | 5.28 | 3 | 14 | 16 | 25 | 31 |
| `4-Transition pending->confirmed` | 80 | 0.00% | 18.99 | 15 | 42 | 43 | 45 | 47 |

---

## 3. Tiêu chuẩn Quality Gate & Đối chiếu Baseline

Baseline: ngưỡng đề xuất bởi AI analysis (report §3.2) đã được human chấp thuận — p95 ≤ 100 ms, error < 1%, sustained ≥ 12 RPS (soak 10 phút giữ 12.2 RPS); quy tắc endurance: p95 mỗi cửa sổ ≤ 2× baseline.

| Tiêu chí Quality Gate | Giá trị Đo được | Ngưỡng Tiêu chuẩn | Trạng thái | Đánh giá Tác động |
| :---| :---: | :---: | :---: | :---|
| **p95 tuyệt đối (≤ 100 ms)** | Worst = `60 ms` (Stress OVERALL) | `100 ms` | **PASS** | Đạt SLA ở cả 3 kịch bản; tail Stress (p99 428 ms) phình nhưng p95 trong ngưỡng |
| **Tỷ lệ lỗi tổng thể (≤ 1%)** | `0.00%` (2.160/2.160 samples) | `1%` | **PASS** | Đạt độ tin cậy; không lockout, không invalid-transition |
| **Throughput duy trì ≥ Baseline (≥ 12 RPS)** | Load `16.03` · Stress `50.12` · Spike `92.62` | `12.2 RPS` (endurance baseline) | **PASS** | Scale gần tuyến tính 3.1× khi tăng 3× concurrency |
| **Độ ổn định theo thời gian (Endurance)** | p95 cửa sổ max `29 ms` ≤ 2× baseline `22 ms`; error 0% cả 10 cửa sổ | drift ≤ 2×, err < 1% | **PASS** | Không suy thoái trong 10 phút; trần bộ nhớ backend ≈ 71 MB |

**Kết luận:** hệ thống đạt Quality Gate ở mức tải khảo sát — điểm gãy (nếu có) nằm ngoài 60 threads; đường ghi PUT là thành phần nhạy tải nhất (p95 91 ms dưới Stress), phù hợp đề xuất bật SQLite WAL ở report §3.4.
