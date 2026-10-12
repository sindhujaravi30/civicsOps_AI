
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
