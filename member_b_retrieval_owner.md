# Member B — Retrieval Owner

Vai trò chính: Lead Retrieval trong Sprint 2
File chính: workers/retrieval.py
File phối hợp: contracts/worker_contracts.yaml

## Mục tiêu trong ngày
- Bảo đảm retrieval trả về evidence đúng, có score, có source.
- Là nền dữ liệu cho policy và synthesis.

## Cấu hình kỹ thuật bắt buộc
- Embedding ưu tiên: all-MiniLM-L6-v2
- Vector store: ChromaDB PersistentClient
- Collection: day09_docs
- Baseline retrieval từ Day 08:
  - top_k_search: 10
  - top_k_select: 3 (handoff cho synthesis)
  - dense abstain threshold tham chiếu: 0.3
- Metadata chunks cần giữ: source, section, effective_date

## Công việc chi tiết theo Sprint

## Sprint 1 (60') — Chuẩn bị phụ thuộc

Checklist chuẩn bị:
- [ ] Đồng bộ với Member A về state keys và route mặc định.
- [ ] Kiểm tra dữ liệu data/docs và cấu hình chroma_db.
- [ ] Xác nhận top_k mặc định và format chunk.

Checklist setup:
- [ ] Kiem tra env CHROMA_DB_PATH, CHROMA_COLLECTION.
- [ ] Neu collection rong, thong bao team chay lai index.

Đầu ra:
- Kế hoạch retrieval rõ ràng, không block Sprint 2.

## Sprint 2 (60') — Bắt buộc hoàn thành

Checklist implementation:
- [ ] Hoàn thiện _get_embedding_fn() với ưu tiên sentence-transformers.
- [ ] Hoàn thiện _get_collection() kết nối collection day09_docs.
- [ ] Hoàn thiện retrieve_dense(query, top_k):
  - [ ] Query ChromaDB thành công.
  - [ ] Trả list chunk có text, source, score, metadata.
  - [ ] Không có dữ liệu thì trả [] (không fake).
- [ ] Hoàn thiện run(state):
  - [ ] Ghi retrieved_chunks, retrieved_sources.
  - [ ] Ghi worker_io_logs đúng contract.

Format chunk target:
```json
{
  "text": "...",
  "source": "sla_p1_2026.txt",
  "score": 0.92,
  "metadata": {"section": "...", "effective_date": "..."}
}
```

Checklist validation:
- [ ] Test query SLA có chunks liên quan.
- [ ] score trong khoảng 0..1.
- [ ] source map đúng file trong data/docs.
- [ ] query không có dữ liệu thì trả [] sạch, không fake chunk.

Lệnh kiểm tra nhanh:
```bash
python workers/retrieval.py
```

Đầu ra bàn giao:
- workers/retrieval.py sẵn sàng cho C/D tích hợp.
- Cập nhật phần retrieval actual_implementation trong contracts.

## Sprint 3 (60') — Hỗ trợ MCP search_kb

Checklist phối hợp:
- [ ] Hỗ trợ Member C nối mcp_server search_kb tái sử dụng retrieve_dense.
- [ ] Rà output schema search_kb khớp expectation policy worker.

Schema search_kb cần thống nhất:
- chunks: list
- sources: list
- total_found: int

Đầu ra:
- search_kb trả chunks/sources/total_found ổn định.

## Sprint 4 (60') — Hỗ trợ trace + so sánh metrics

Checklist phối hợp:
- [ ] Cung cấp 3 trace minh chứng retrieval hoạt động đúng.
- [ ] Hỗ trợ D/E đọc top_sources và lý giải coverage.

Evidence ưu tiên:
- 1 trace câu SLA
- 1 trace câu policy
- 1 trace câu thiếu ngữ cảnh

Đầu ra:
- Evidence retrieval cho docs và report nhóm.

## Definition of Done cá nhân
- [ ] retrieval worker test độc lập pass.
- [ ] Contract retrieval khớp code triển khai.
- [ ] Giải thích được vì sao query nào không tìm thấy evidence.

## Rủi ro cần tránh
- Trả source thiếu hoặc sai khiến synthesis cite sai.
- Xử lý lỗi mơ hồ làm khó debug tích hợp.
- Không phân biệt top_k_search và top_k_select làm context quá nhiễu.