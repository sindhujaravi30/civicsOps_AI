
from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.app.models.documents import (
    DocumentChunkResponse,
    DocumentIngestionResponse,
)
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
