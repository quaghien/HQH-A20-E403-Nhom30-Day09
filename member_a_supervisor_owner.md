# Member A — Supervisor Owner

Vai trò chính: Lead Sprint 1 (Refactor Graph)
File chính: graph.py

## Mục tiêu trong ngày
- Chốt luồng điều phối supervisor-worker để toàn team tích hợp ổn định.
- Đảm bảo route_reason rõ ràng để trace debug được.

## Cấu hình kỹ thuật cần nắm
- Input route classes:
  - SLA/P1/ticket/escalation -> retrieval_worker
  - refund/hoan tien/flash sale/license/access -> policy_tool_worker
  - unknown error code (ERR-*) + risk_high -> human_review
- State keys khung:
  - task, supervisor_route, route_reason, risk_high, needs_tool
  - workers_called, retrieved_chunks, policy_result, final_answer, confidence
  - mcp_tools_used, hitl_triggered, latency_ms

## Công việc chi tiết theo Sprint

## Sprint 1 (60') — Bắt buộc hoàn thành

Checklist implementation:
- [ ] Hoàn thiện AgentState trong graph.py với các field cần cho trace.
- [ ] Hoàn thiện supervisor_node(state):
  - [ ] Nhận task, chuẩn hóa keyword.
  - [ ] Route đúng giữa retrieval_worker, policy_tool_worker, human_review.
  - [ ] Ghi route_reason rõ, không dùng mô tả chung chung.
  - [ ] Set risk_high, needs_tool theo ngữ cảnh.
- [ ] Hoàn thiện route_decision(state) cho conditional edge.
- [ ] Hoàn thiện human_review_node(state) (placeholder HITL có log rõ ràng).

Checklist validation:
- [ ] Chạy python graph.py không lỗi.
- [ ] Ít nhất 2 query ra 2 route khác nhau.
- [ ] route_reason nhìn vào là hiểu vì sao route.
- [ ] workers_called phản ánh đúng thứ tự thực thi.

Lệnh kiểm tra nhanh:
```bash
python graph.py
```

Format route_reason đề xuất:
- "task contains SLA/P1 keyword -> retrieval_worker"
- "task contains refund/access keyword -> policy_tool_worker"
- "risk_high + unknown error code -> human_review"

Đầu ra bàn giao:
- graph.py ổn định cho Sprint 2 tích hợp workers.
- Note ngắn về routing rules gửi team.

## Sprint 2 (60') — Hỗ trợ tích hợp workers

Checklist phối hợp:
- [ ] Làm rõ state keys cho B/C/D: retrieved_chunks, policy_result, final_answer, confidence.
- [ ] Kiểm tra workers_called ghi đúng thứ tự khi chạy graph.
- [ ] Cùng Member E chạy 3 test query tích hợp.

Bộ query smoke test tối thiểu:
- "SLA xử lý ticket P1 là bao lâu?"
- "Khách hàng flash sale yêu cầu hoàn tiền, được không?"
- "ERR-403-AUTH là lỗi gì và cách xử lý?"

Đầu ra bàn giao:
- Xác nhận graph tương thích với 3 worker.

## Sprint 3 (60') — Hỗ trợ MCP route logic

Checklist phối hợp:
- [ ] Rà lại điều kiện needs_tool để C gọi MCP đúng lúc.
- [ ] Bổ sung route_reason cho trường hợp có MCP.

Yêu cầu log khi needs_tool=True:
- route_reason phải nêu luôn signal dẫn tới tool call
- state.mcp_tools_used để rỗng cho tới khi worker gọi tool

Đầu ra bàn giao:
- Route có ngữ nghĩa rõ cho câu cần tool call.

## Sprint 4 (60') — Hỗ trợ trace và docs

Checklist phối hợp:
- [ ] Cung cấp 3 ví dụ routing thực tế cho docs/routing_decisions.md.
- [ ] Hỗ trợ Member E kiểm tra trace fields bắt buộc.

Trace fields A phải xác nhận:
- supervisor_route
- route_reason
- workers_called
- hitl_triggered

Đầu ra bàn giao:
- Evidence routing cho tài liệu nhóm.

## Definition of Done cá nhân
- [ ] graph.py pass test chạy tay.
- [ ] route_reason không để unknown/rỗng.
- [ ] Giải thích được đầy đủ logic routing khi bị hỏi.

## Rủi ro cần tránh
- Routing quá mơ hồ dẫn đến trace khó debug.
- Đổi state key đột ngột làm vỡ worker contract.
- Đặt default route không hợp lý khiến policy câu hỏi bị chệch worker.