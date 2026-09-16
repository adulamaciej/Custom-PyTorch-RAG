from dataclasses import dataclass


@dataclass
class Chunk:
    source: str
    title: str
    section: str
    content: str