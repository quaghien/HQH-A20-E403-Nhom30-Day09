# Member E — Integration + Trace Owner

Vai trò chính: Lead Sprint 4 (Trace & Integration)
File chính: eval_trace.py, artifacts/*

## Mục tiêu trong ngày
- Chạy lại trọn bộ luồng end-to-end để tổng hợp thông tin cho cả team.
- Là release gate trước commit 18:00.

## Trace schema can khoa
Moi ban ghi trace can co toi thieu:
- task
- supervisor_route
- route_reason
- workers_called
- mcp_tools_used
- retrieved_sources
- final_answer
- confidence
- hitl_triggered
- latency_ms
- timestamp

## Công việc chi tiết theo Sprint

## Sprint 1 (60') — Thiết kế checklist tích hợp

Checklist chuẩn bị:
- [ ] Tạo checklist trace fields bắt buộc theo README/SCORING.
- [ ] Thống nhất quy tắc pass/fail cho test tích hợp nhanh.

Pass/fail smoke test:
- pass: pipeline tra answer + trace du fields
- fail: crash hoac trace thieu field critical

Đầu ra:
- Bảng kiểm tích hợp dùng cho toàn team.

## Sprint 2 (60') — Test từng worker độc lập

Checklist validation:
- [ ] Chạy test retrieval/policy/synthesis độc lập.
- [ ] Ghi lỗi tích hợp gửi ngay cho owner tương ứng.
- [ ] Verify input/output workers bám contracts.

Lenh goi test de nghi:
```bash
python workers/retrieval.py
python workers/policy_tool.py
python workers/synthesis.py
```

Đầu ra:
- Danh sách bug + trạng thái fix theo vòng.

## Sprint 3 (60') — Test luồng có MCP

Checklist validation:
- [ ] Chạy các câu cần tool call để xác nhận mcp_tools_used.
- [ ] Kiểm tra dispatch_tool lỗi không làm vỡ pipeline.
- [ ] Kiểm tra route_reason có phản ánh tình huống MCP.

Case uu tien trong sprint nay:
- cau access emergency
- cau P1 + ticket info

Đầu ra:
- Xác nhận luồng policy + MCP hoạt động thực tế.

## Sprint 4 (60') — Bắt buộc hoàn thành trace/eval

Checklist implementation:
- [ ] Hoàn thiện eval_trace.py run_test_questions().
- [ ] Hoàn thiện eval_trace.py run_grading_questions().
- [ ] Chạy 15 test questions và lưu artifacts/traces/.
- [ ] Chạy grading sau 17:00 và xuất artifacts/grading_run.jsonl.
- [ ] Tổng hợp metrics cho docs comparison.

Lenh run chinh:
```bash
python eval_trace.py
python eval_trace.py --grading
python eval_trace.py --analyze
python eval_trace.py --compare
```

Checklist release gate trước 18:00:
- [ ] Tất cả file code bắt buộc đã pass chạy cơ bản.
- [ ] Trace có các field trọng yếu: supervisor_route, route_reason, workers_called, mcp_tools_used, confidence.
- [ ] artifacts/grading_run.jsonl đúng JSONL, đủ số dòng theo đề grading.
- [ ] Co bang tong hop metric gui cho Member D viet docs comparison.

Đầu ra bàn giao:
- Bộ artifacts cuối để nộp chấm nhóm.
- Summary kết quả để D viết docs/report.

## Definition of Done cá nhân
- [ ] eval_trace.py chạy end-to-end không crash ở luồng chính.
- [ ] artifacts sinh ra đúng format, đủ dữ liệu.
- [ ] Có thể giải thích kết quả pass/fail từng cụm câu hỏi.

## Rủi ro cần tránh
- Chạy xong nhưng không lưu đúng format JSONL.
- Có trace nhưng thiếu field khiến bị trừ điểm câu grading.
- Chỉ kiểm tra output answer ma bo qua chat luong route_reason.