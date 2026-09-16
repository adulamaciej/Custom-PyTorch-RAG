from dataclasses import dataclass


@dataclass
class Document:
    source: str
    title: str
    html: str