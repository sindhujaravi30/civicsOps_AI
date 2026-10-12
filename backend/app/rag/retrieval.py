
from dataclasses import asdict

import numpy as np
from fastembed import TextEmbedding

from backend.app.rag.ingestion import DocumentChunk


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

_embedding_model: TextEmbedding | None = None

# Temporary in-memory index. This is lost when the backend restarts.
# Keyed by chunk ID; values contain chunk metadata and its embedding.
_index: dict[str, dict] = {}


def get_embedding_model() -> TextEmbedding:
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = TextEmbedding(model_name=MODEL_NAME)

    return _embedding_model


def embed_documents(chunks: list[DocumentChunk]) -> list[list[float]]:
    if not chunks:
        return []

    model = get_embedding_model()
    texts = [chunk.text for chunk in chunks]

    return [vector.tolist() for vector in model.embed(texts)]


def embed_query(question: str) -> list[float]:
    model = get_embedding_model()
    vector = next(model.query_embed(question))
    return vector.tolist()


def index_chunks(chunks: list[DocumentChunk]) -> int:
    """Embed chunks and replace previously indexed chunks for the same file."""
    if not chunks:
        return 0

    source = chunks[0].source

    # Replace this file's previous entries if it is re-indexed.
    stale_ids = [
        chunk_id
        for chunk_id, item in _index.items()
        if item["chunk"].source == source
    ]
    for chunk_id in stale_ids:
        del _index[chunk_id]

    vectors = embed_documents(chunks)

    for chunk, vector in zip(chunks, vectors):
        _index[chunk.chunk_id] = {
            "chunk": chunk,
            "vector": vector,
        }

    return len(chunks)


def search_chunks(
    question: str,
    top_k: int = 5,
) -> list[dict]:
    """Return the most semantically similar indexed chunks."""
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if top_k < 1 or top_k > 20:
        raise ValueError("top_k must be between 1 and 20.")

    if not _index:
        return []

    query_vector = np.asarray(embed_query(question), dtype=np.float32)
    query_norm = np.linalg.norm(query_vector)

    results = []

    for item in _index.values():
        vector = np.asarray(item["vector"], dtype=np.float32)
        denominator = query_norm * np.linalg.norm(vector)

        score = (
            float(np.dot(query_vector, vector) / denominator)
            if denominator > 0
            else 0.0
        )

        results.append({
            "chunk": item["chunk"],
            "score": score,
        })

    results.sort(key=lambda result: result["score"], reverse=True)

    return results[:top_k]


def clear_index() -> None:
    """Clear the in-memory index. Useful for development and tests."""
    _index.clear()

def indexed_chunk_count() -> int:
    return len(_index)