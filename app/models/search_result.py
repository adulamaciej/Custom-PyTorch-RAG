from dataclasses import dataclass

from app.models.chunk import Chunk


@dataclass
class SearchResult:
    chunk: Chunk
    score: float