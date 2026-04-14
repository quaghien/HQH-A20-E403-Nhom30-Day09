# Member D — Synthesis + Docs Owner

Vai trò chính: Synthesis worker (Sprint 2) + tài liệu kỹ thuật (Sprint 4)
File chính: workers/synthesis.py, docs/*.md

## Mục tiêu trong ngày
- Tạo câu trả lời cuối grounded, có citation và confidence hợp lý.
- Chốt 3 tài liệu docs trước 18:00.

## Cấu hình model va generation
- Model uu tien: gpt-4o-mini
- Model du phong: gemini-1.5-flash
- Temperature: 0.1 (uu tien on dinh)
- Max tokens: 500-512
- Prompt rule: chi duoc tra loi tu context, thieu context thi abstain ro rang

## Công việc chi tiết theo Sprint

## Sprint 1 (60') — Chuẩn hóa output format

Checklist chuẩn bị:
- [ ] Chốt với A/B/C các field đầu vào synthesis: task, retrieved_chunks, policy_result.
- [ ] Thống nhất format sources và confidence.

Output contract muc tieu:
- final_answer: str
- sources: list[str]
- confidence: float

Đầu ra:
- Khung output final_answer/sources/confidence thống nhất.

## Sprint 2 (60') — Bắt buộc hoàn thành synthesis

Checklist implementation:
- [ ] Hoàn thiện _build_context(chunks, policy_result) rõ ràng, dễ grounding.
- [ ] Hoàn thiện _call_llm(messages) với fallback an toàn.
- [ ] Hoàn thiện _estimate_confidence(chunks, answer, policy_result).
- [ ] Hoàn thiện run(state): ghi final_answer, sources, confidence, worker_io_logs.

Checklist prompt grounding:
- [ ] Nhan manh "khong dung kien thuc ngoai context"
- [ ] Neu policy_result co exception, can neu truoc khi ket luan
- [ ] Citation theo ten file nguon

Checklist validation:
- [ ] Có chunks thì answer có citation nguồn.
- [ ] Không có chunks thì abstain rõ ràng.
- [ ] confidence phản ánh mức độ evidence, không hard-code.
- [ ] Khong co hallucination o query out-of-scope.

Lệnh kiểm tra nhanh:
```bash
python workers/synthesis.py
```

Đầu ra bàn giao:
- workers/synthesis.py tích hợp ổn trong graph.

## Sprint 3 (60') — Hỗ trợ policy-aware synthesis

Checklist phối hợp:
- [ ] Đảm bảo synthesis phản ánh policy exceptions khi policy_result có cảnh báo.
- [ ] Rà câu trả lời để tránh hallucination.

Ky thuat can dam bao:
- Neu policy_applies=False, answer khong duoc ket luan nguoc policy
- Neu source rong, confidence phai thap

Đầu ra:
- Answer nhất quán giữa evidence và policy.

## Sprint 4 (60') — Bắt buộc hoàn thành docs kỹ thuật

Checklist implementation docs:
- [ ] Điền docs/system_architecture.md.
- [ ] Điền docs/routing_decisions.md với ít nhất 3 quyết định thật từ trace.
- [ ] Điền docs/single_vs_multi_comparison.md với ít nhất 2 metrics có số liệu.

Metrics docs comparison nen co:
- avg_confidence
- avg_latency_ms
- abstain_rate
- context_recall hoac routing_visibility

Checklist phối hợp:
- [ ] Lấy trace evidence từ E.
- [ ] Lấy routing explanation từ A, MCP evidence từ C, retrieval evidence từ B.

Đầu ra bàn giao:
- 3 file docs hoàn chỉnh trước 18:00.

## Definition of Done cá nhân
- [ ] Synthesis worker trả answer grounded và source rõ.
- [ ] 3 docs kỹ thuật điền đầy đủ, có bằng chứng trace.
- [ ] Giải thích được phương pháp confidence và abstain.

## Rủi ro cần tránh
- Docs ghi giả định không khớp trace thực.
- Câu trả lời dài nhưng thiếu citation cụ thể.
- confidence cao bat thuong khi evidence yeu.