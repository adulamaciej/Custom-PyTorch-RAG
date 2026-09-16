from app.models.document import Document
from app.ingestion.chunker import StructureChunker


def test_chunker():

    document = Document(
        source="test.html",
        title="Test",
        html=""
    )

    elements = [
        {
            "type": "h1",
            "text": "PyTorch"
        },
        {
            "type": "h2",
            "text": "Autograd"
        },
        {
            "type": "p",
            "text": "Automatic differentiation."
        }
    ]

    chunker = StructureChunker()

    chunks = chunker.chunk(
        document,
        elements
    )

    assert len(chunks) == 1

    assert (
        chunks[0].section
        == "PyTorch > Autograd"
    )