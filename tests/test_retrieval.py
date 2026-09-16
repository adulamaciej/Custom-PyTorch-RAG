from app.models.chunk import Chunk
from app.indexing.bm25_index import BM25Index


def test_bm25():

    chunks = [
        Chunk(
            source="compile.html",
            title="Compile",
            section="torch.compile",
            content="torch.compile optimizes PyTorch models"
        ),
        Chunk(
            source="autograd.html",
            title="Autograd",
            section="Autograd",
            content="Automatic differentiation and gradients"
        ),
        Chunk(
            source="dataloader.html",
            title="DataLoader",
            section="DataLoader",
            content="DataLoader loads training data in batches"
        )
    ]

    index = BM25Index()
    index.build(chunks)

    results = index.search(
        "torch.compile",
        top_k=1
    )

    assert results[0].chunk.source == "compile.html"