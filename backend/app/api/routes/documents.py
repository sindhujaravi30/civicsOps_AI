
from fastapi import APIRouter, File, HTTPException, UploadFile, Body

from backend.app.models.documents import (
    DocumentChunkResponse,
    DocumentIngestionResponse,
)
from backend.app.models.documents import (
    SemanticSearchRequest,
    SemanticSearchResponse,
    SearchResultResponse,
)
from backend.app.rag.retrieval import index_chunks, search_chunks, indexed_chunk_count
from backend.app.rag.ingestion import MAX_FILE_BYTES, ingest_document


router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("/ingest", response_model=DocumentIngestionResponse)
async def ingest_uploaded_document(
    file: UploadFile = File(...),
) -> DocumentIngestionResponse:
    filename = file.filename or "unnamed"

    try:
        content = await file.read(MAX_FILE_BYTES + 1)

        chunks = ingest_document(filename, content)

        return DocumentIngestionResponse(
            filename=filename,
            chunks_created=len(chunks),
            chunks_preview=[
                DocumentChunkResponse(**chunk.__dict__)
                for chunk in chunks[:3]
            ],
            persisted=False,
            message=(
                "Document extracted and chunked successfully. "
                "Database persistence will be enabled after Milestone 4 "
                "is verified."
            ),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await file.close()


@router.post("/index")
async def index_uploaded_document(
    file: UploadFile = File(...),
):
    filename = file.filename or "unnamed"

    try:
        content = await file.read(MAX_FILE_BYTES + 1)
        chunks = ingest_document(filename, content)

        count = index_chunks(chunks)

        return {
            "filename": filename,
            "chunks_indexed": count,
            "persisted": False,
            "message": (
                "Chunks embedded and indexed in memory. "
                "The index is cleared when the backend restarts."
            ),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await file.close()


@router.post("/search", response_model=SemanticSearchResponse)
def semantic_search(
    request: SemanticSearchRequest = Body(...),
):
    try:
        results = search_chunks(
            question=request.question,
            top_k=request.top_k,
        )

        return SemanticSearchResponse(
            question=request.question,
            indexed_chunks=indexed_chunk_count(),
            results=[
                SearchResultResponse(
                    chunk_id=item["chunk"].chunk_id,
                    text=item["chunk"].text,
                    source=item["chunk"].source,
                    file_type=item["chunk"].file_type,
                    location=item["chunk"].location,
                    score=round(item["score"], 4),
                )
                for item in results
            ],
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc