from app.models.chunk import Chunk
from app.models.search_result import SearchResult
from app.retrieval.rrf import reciprocal_rank_fusion


def test_rrf():

    chunk1 = Chunk(
        source="a.html",
        title="A",
        section="Test",
        content="First"
    )

    chunk2 = Chunk(
        source="b.html",
        title="B",
        section="Test",
        content="Second"
    )

    list1 = [
        SearchResult(chunk1, 0.9),
        SearchResult(chunk2, 0.8)
    ]

    list2 = [
        SearchResult(chunk1, 10),
        SearchResult(chunk2, 5)
    ]

    results = reciprocal_rank_fusion(
        [list1, list2]
    )

    assert results[0].chunk == chunk1