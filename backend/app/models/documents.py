
from pydantic import BaseModel, Field


class DocumentChunkResponse(BaseModel):
    chunk_id: str
    text: str
    source: str
    file_type: str
    location: str
    chunk_index: int


class DocumentIngestionResponse(BaseModel):
    filename: str
    chunks_created: int
    chunks_preview: list[DocumentChunkResponse] = Field(default_factory=list)
    persisted: bool = False
    message: str


class SemanticSearchRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=20)


class SearchResultResponse(BaseModel):
    chunk_id: str
    text: str
    source: str
    file_type: str
    location: str
    score: float


class SemanticSearchResponse(BaseModel):
    question: str
    results: list[SearchResultResponse]
    indexed_chunks: int