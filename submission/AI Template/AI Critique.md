# AI CRITIQUE


Xuyên suốt HW05, AI sai nhiều nhất ở hai dạng: đọc nhầm số liệu và đề xuất vượt quá stack thật.

Ở Task 2, AI trích *average* (6 ms) làm p95 của Load — đánh giá thấp tail risk 3 lần — và bịa bảo chứng "mọi label ≥100 samples" trong khi Spike chỉ có 80. Nguyên nhân không phải thiếu dữ liệu: cả ba bảng số đều nằm trong prompt. Mô hình tối ưu hóa câu chuyện nghe hợp lý thay vì trung thực với từng con số, và khi một claim không quan trọng với mạch văn, nó được điền bằng giá trị "tròn trịa" thay vì đọc lại.

Ở khâu đề xuất tối ưu, AI cho lời khuyên connection pool và caching như thể đang tư vấn hệ thống client–server, trong khi SUT là SQLite embedded một process — lời khuyên đúng giáo trình nhưng sai bản chất; chỉ khi mở `database.js` và `package.json` đối chiếu mới phát hiện được. Điều này lặp lại đúng pattern ở khâu design: AI tái dùng số template (ramp 30 s) mà không tính lại thread lifetime, suýt khiến Stress chỉ đo 21/60 thread.

Bài học nguyên tắc: (1) luôn dán ground truth vào báo cáo trước khi hỏi AI, để nó không có cơ hội bẻ số; (2) mọi đề xuất kỹ thuật phải qua hai cổng kiểm chứng — bottleneck có hiện trong metrics của mình không, và repo thật có dùng công nghệ đó không; (3) human review phải hướng vào những chỗ đang PASS hợp lý, vì đó là nơi lỗi AI ẩn nấp tốt nhất.

AI là trợ lý diễn giải xuất sắc, nhưng trách nhiệm về con số cuối cùng luôn thuộc về người chạy test.
