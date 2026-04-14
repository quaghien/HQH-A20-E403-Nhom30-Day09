"""
workers/retrieval.py — Retrieval Worker
Sprint 2: Implement retrieval từ ChromaDB, trả về chunks + sources.

Input (từ AgentState):
    - task: câu hỏi cần retrieve
    - (optional) retrieved_chunks nếu đã có từ trước

Output (vào AgentState):
    - retrieved_chunks: list of {"text", "source", "score", "metadata"}
    - retrieved_sources: list of source filenames
    - worker_io_log: log input/output của worker này

Gọi độc lập để test:
    python workers/retrieval.py
"""

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import sys

# ─────────────────────────────────────────────
# Worker Contract (xem contracts/worker_contracts.yaml)
# Input:  {"task": str, "top_k": int = 3}
# Output: {"retrieved_chunks": list, "retrieved_sources": list, "error": dict | None}
# ─────────────────────────────────────────────

WORKER_NAME = "retrieval_worker"
DEFAULT_TOP_K = 3
TOP_K_SEARCH = 10       # Số chunks query từ ChromaDB
TOP_K_SELECT = 3        # Số chunks handoff cho synthesis
ABSTAIN_THRESHOLD = 0.3 # Lọc bỏ chunk có score < threshold


def _get_embedding_fn():
    """
    Trả về embedding function.
    TODO Sprint 1: Implement dùng OpenAI hoặc Sentence Transformers.
    """
    # Option A: Sentence Transformers (offline, không cần API key)
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        def embed(text: str) -> list:
            return model.encode([text])[0].tolist()
        return embed
    except ImportError:
        pass

    # Option B: OpenAI (cần API key)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        def embed(text: str) -> list:
            resp = client.embeddings.create(input=text, model="text-embedding-3-small")
            return resp.data[0].embedding
        return embed
    except ImportError:
        pass

    # Fallback: random embeddings cho test (KHÔNG dùng production)
    import random
    def embed(text: str) -> list:
        return [random.random() for _ in range(384)]
    print("⚠️  WARNING: Using random embeddings (test only). Install sentence-transformers.")
    return embed


def _get_collection():
    """
    Kết nối ChromaDB collection.
    Đọc path và collection name từ env vars CHROMA_DB_PATH, CHROMA_COLLECTION.
    """
    import chromadb
    chroma_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    collection_name = os.getenv("CHROMA_COLLECTION", "day09_docs")
    client = chromadb.PersistentClient(path=chroma_path)
    try:
        collection = client.get_collection(collection_name)
    except Exception:
        # Auto-create nếu chưa có
        collection = client.get_or_create_collection(
            collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"⚠️  Collection '{collection_name}' chưa có data. Chạy index script trong README trước.")
    return collection


def _fallback_text_search(query: str, top_k: int = TOP_K_SELECT) -> list:
    """
    Fallback: keyword search qua data/docs/*.txt khi ChromaDB không khả dụng.
    Dùng để đảm bảo search_kb luôn trả về kết quả có ý nghĩa.
    """
    import glob
    import re

    docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "docs")
    txt_files = glob.glob(os.path.join(docs_dir, "*.txt"))

    # Chuẩn hóa query thành tập từ khóa
    query_words = set(re.sub(r"[^\w\s]", "", query.lower()).split())

    results = []
    for filepath in txt_files:
        source = os.path.basename(filepath)
        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue

        # Tách thành các đoạn theo dòng trống
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        for para in paragraphs:
            para_lower = para.lower()
            hits = sum(1 for w in query_words if w in para_lower)
            if hits == 0:
                continue
            score = round(hits / max(len(query_words), 1), 4)
            results.append({
                "text": para[:500],
                "source": source,
                "score": score,
                "metadata": {"source": source},
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def retrieve_dense(
    query: str,
    top_k_search: int = TOP_K_SEARCH,
    top_k_select: int = TOP_K_SELECT,
) -> list:
    """
    Dense retrieval: embed query → query ChromaDB → lọc threshold → trả top_k_select chunks.

    Two-stage:
    - Bước 1: Query ChromaDB với n_results=top_k_search (mặc định 10)
    - Bước 2: Lọc bỏ chunk có score < ABSTAIN_THRESHOLD (0.3)
    - Bước 3: Trả về tối đa top_k_select (mặc định 3) chunks còn lại

    Fallback: Nếu ChromaDB không khả dụng → keyword search qua data/docs/*.txt

    Returns:
        list of {"text": str, "source": str, "score": float, "metadata": dict}
    """
    try:
        embed = _get_embedding_fn()
        query_embedding = embed(query)

        collection = _get_collection()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k_search,
            include=["documents", "distances", "metadatas"]
        )

        chunks = []
        for doc, dist, meta in zip(
            results["documents"][0],
            results["distances"][0],
            results["metadatas"][0]
        ):
            score = round(1 - dist, 4)  # cosine similarity
            if score < ABSTAIN_THRESHOLD:
                continue  # Lọc bỏ chunk dưới threshold
            chunks.append({
                "text": doc,
                "source": meta.get("source", "unknown"),
                "score": score,
                "metadata": meta,
            })

        return chunks[:top_k_select]

    except Exception as e:
        print(f"⚠️  ChromaDB query failed: {e}. Falling back to text search.")
        return _fallback_text_search(query, top_k=top_k_select)


def run(state: dict) -> dict:
    """
    Worker entry point — gọi từ graph.py.

    Args:
        state: AgentState dict

    Returns:
        Updated AgentState với retrieved_chunks và retrieved_sources
    """
    task = state.get("task", "")
    top_k_search = state.get("retrieval_top_k_search", TOP_K_SEARCH)
    top_k_select = state.get("retrieval_top_k", TOP_K_SELECT)

    state.setdefault("workers_called", [])
    state.setdefault("history", [])

    state["workers_called"].append(WORKER_NAME)

    # Log worker IO (theo contract)
    worker_io = {
        "worker": WORKER_NAME,
        "input": {"task": task, "top_k_search": top_k_search, "top_k_select": top_k_select},
        "output": None,
        "error": None,
    }

    try:
        chunks = retrieve_dense(task, top_k_search=top_k_search, top_k_select=top_k_select)

        sources = list({c["source"] for c in chunks})

        state["retrieved_chunks"] = chunks
        state["retrieved_sources"] = sources

        worker_io["output"] = {
            "chunks_count": len(chunks),
            "sources": sources,
        }
        state["history"].append(
            f"[{WORKER_NAME}] retrieved {len(chunks)} chunks from {sources}"
        )

    except Exception as e:
        worker_io["error"] = {"code": "RETRIEVAL_FAILED", "reason": str(e)}
        state["retrieved_chunks"] = []
        state["retrieved_sources"] = []
        state["history"].append(f"[{WORKER_NAME}] ERROR: {e}")

    # Ghi worker IO vào state để trace
    state.setdefault("worker_io_logs", []).append(worker_io)

    return state


# ─────────────────────────────────────────────
# Test độc lập
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("Retrieval Worker — Standalone Test")
    print("=" * 50)

    test_queries = [
        "SLA ticket P1 là bao lâu?",
        "Điều kiện được hoàn tiền là gì?",
        "Ai phê duyệt cấp quyền Level 3?",
    ]

    for query in test_queries:
        print(f"\n▶ Query: {query}")
        result = run({"task": query})
        chunks = result.get("retrieved_chunks", [])
        print(f"  Retrieved: {len(chunks)} chunks")
        for c in chunks[:2]:
            print(f"    [{c['score']:.3f}] {c['source']}: {c['text'][:80]}...")
        print(f"  Sources: {result.get('retrieved_sources', [])}")

    print("\n✅ retrieval_worker test done.")
