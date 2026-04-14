# Member C — Policy + MCP Owner

Vai trò chính: Lead Sprint 3 (MCP) và policy logic
File chính: workers/policy_tool.py, mcp_server.py

## Mục tiêu trong ngày
- Xử lý đúng policy exceptions theo tài liệu.
- Tích hợp MCP tools thật trong luồng worker.

## Ma tran exception toi thieu
- flash sale -> policy_applies=False
- digital product (license key/subscription) -> policy_applies=False
- activated product -> policy_applies=False
- don truoc 01/02/2026 -> gan policy_version_note (temporal scoping)

## Công việc chi tiết theo Sprint

## Sprint 1 (60') — Chuẩn bị rules

Checklist chuẩn bị:
- [ ] Đồng bộ với A về điều kiện route policy_tool_worker và needs_tool.
- [ ] Xác nhận exception rules từ policy_refund_v4.

Ket qua can chot:
- keyword map chuyen vao analyze_policy
- format policy_result thong nhat cho synthesis

Đầu ra:
- Danh sách keyword/rule dùng cho policy analysis.

## Sprint 2 (60') — Hoàn thiện policy worker

Checklist implementation:
- [ ] Hoàn thiện analyze_policy(task, chunks):
  - [ ] Detect flash_sale_exception.
  - [ ] Detect digital_product_exception.
  - [ ] Detect activated_exception.
  - [ ] Đánh dấu temporal scoping nếu đơn trước 01/02/2026.
- [ ] Hoàn thiện run(state):
  - [ ] Ghi policy_result đầy đủ.
  - [ ] Ghi worker_io_logs và mcp_tools_used (nếu có).

Khung policy_result muc tieu:
```json
{
  "policy_applies": false,
  "policy_name": "refund_policy_v4",
  "exceptions_found": [{"type": "flash_sale_exception", "rule": "...", "source": "policy_refund_v4.txt"}],
  "source": ["policy_refund_v4.txt"],
  "policy_version_note": "..."
}
```

Checklist validation:
- [ ] Test case flash sale trả policy_applies=False.
- [ ] Test case license key trả policy_applies=False.
- [ ] Không bịa policy ngoài dữ liệu có thật.
- [ ] Test 1 case temporal scoping trả note rõ ràng.

Lệnh kiểm tra nhanh:
```bash
python workers/policy_tool.py
```

Đầu ra bàn giao:
- workers/policy_tool.py sẵn sàng tích hợp MCP.

## Sprint 3 (60') — Bắt buộc hoàn thành MCP

Checklist implementation:
- [ ] Hoàn thiện mcp_server.py:
  - [ ] search_kb(query, top_k)
  - [ ] get_ticket_info(ticket_id)
  - [ ] dispatch_tool(tool_name, tool_input) trả error dict chuẩn
  - [ ] list_tools() trả schema discoverable
- [ ] Nối policy worker gọi _call_mcp_tool khi needs_tool=True.

Contract MCP call log trong state.mcp_tools_used:
- tool
- input
- output
- error
- timestamp

Checklist validation:
- [ ] Gọi tool hợp lệ trả output đúng.
- [ ] Tool không tồn tại trả error không crash.
- [ ] Trace có ít nhất 1 mcp_tools_used thật.

Lệnh kiểm tra nhanh:
```bash
python mcp_server.py
```

Đầu ra bàn giao:
- mcp_server.py + policy_tool.py chạy qua luồng tích hợp.

## Sprint 4 (60') — Hỗ trợ grading và docs

Checklist phối hợp:
- [ ] Cùng E kiểm tra các câu cần MCP trong trace.
- [ ] Cung cấp evidence cho phần MCP trong docs/system_architecture.md.

Case uu tien:
- cau lien quan ticket P1
- cau lien quan access level emergency

Đầu ra:
- Minh chứng MCP integration trong bài nộp.

## Definition of Done cá nhân
- [ ] Policy worker xử lý ít nhất 1 exception case đúng rubric.
- [ ] MCP có tối thiểu 2 tools và được gọi thực tế.
- [ ] Giải thích được đầy đủ input/output của mcp_tools_used.

## Rủi ro cần tránh
- Chỉ implement tool nhưng không có call thực tế trong trace.
- Exception detection thiếu khiến mất điểm câu grading refund.
- dispatch_tool raise exception ra ngoài thay vi tra error dict.