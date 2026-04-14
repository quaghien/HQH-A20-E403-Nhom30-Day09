# Team Technical Brief (Lab 9)

Tai lieu nay la mo ta ky thuat tong quat cho team 5 nguoi, theo dung khung 4 sprint trong README.

## 1) Kien truc tong the

- Pattern: Supervisor-Worker
- Luong: Input -> Supervisor -> Retrieval/Policy/Human Review -> Synthesis -> Output
- State trung tam: AgentState trong graph.py
- External capability: MCP tools qua mcp_server.py
- Tracing: eval_trace.py + artifacts/traces + artifacts/grading_run.jsonl

## 2) Tech stack va cau hinh chinh

- LLM tong hop:
	- Chinh: gpt-4o-mini (OpenAI)
	- Du phong: gemini-1.5-flash
- Embedding:
	- all-MiniLM-L6-v2 (sentence-transformers)
	- fallback OpenAI embedding text-embedding-3-small
- Vector store:
	- ChromaDB PersistentClient
	- Collection: day09_docs
- Retrieval baseline khuyen nghi (tham chieu Day 08):
	- retrieval_mode: dense
	- top_k_search: 10
	- top_k_select: 3
	- abstain threshold dense: 0.3
- Chunking baseline khuyen nghi neu can rebuild index:
	- chunk_size: 400
	- overlap: 80
	- metadata toi thieu: source, section, effective_date

## 3) Cac module ky thuat bat buoc

- graph.py:
	- supervisor_node, route_decision, human_review_node
	- Ghi supervisor_route, route_reason, risk_high, needs_tool
- workers/retrieval.py:
	- Query ChromaDB, tra ve retrieved_chunks + retrieved_sources
- workers/policy_tool.py:
	- Policy exception check (flash sale, digital product, activated, temporal)
	- MCP tool call logging
- workers/synthesis.py:
	- Grounded answer, citation, confidence
- mcp_server.py:
	- Toi thieu 2 tools: search_kb, get_ticket_info
	- dispatch_tool khong duoc crash
- eval_trace.py:
	- Chay test_questions
	- Chay grading_questions (17:00-18:00)
	- Luu trace dung format

## 4) Metrics bat buoc theo doi

- Chat luong answer:
	- faithfulness
	- relevance
	- context recall
	- completeness
- Van hanh multi-agent:
	- routing_distribution
	- mcp_usage_rate
	- hitl_rate
	- avg_latency_ms

## 5) Mapping vai tro 5 thanh vien

| Thanh vien | Role | Sprint lead | Trach nhiem ky thuat chinh |
|---|---|---|---|
| Member A | Supervisor Owner | Sprint 1 | Routing, AgentState, route_reason quality |
| Member B | Retrieval Owner | Sprint 2 | Embedding, Chroma query, chunk/source score |
| Member C | Policy + MCP Owner | Sprint 3 | Exception logic, MCP tools, dispatch stability |
| Member D | Synthesis + Docs Owner | Sprint 2+4 | Grounded generation, citation, docs technical |
| Member E | Integration + Trace Owner | Sprint 4 | End-to-end run, trace validation, release gate |

## 6) Deadline critical

Truoc 18:00:
- graph.py, workers/*.py, mcp_server.py, eval_trace.py
- contracts/worker_contracts.yaml
- docs/system_architecture.md
- docs/routing_decisions.md
- docs/single_vs_multi_comparison.md
- artifacts/grading_run.jsonl

Sau 18:00 duoc phep:
- reports/group_report.md
- reports/individual/[ten_thanh_vien].md
