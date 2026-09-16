from app.models.search_result import SearchResult


def reciprocal_rank_fusion(
    result_lists,
    k=60
):
    scores = {}
    chunks = {}

    for results in result_lists:

        for rank, result in enumerate(
            results,
            start=1
        ):
            key = (
                result.chunk.source,
                result.chunk.section,
                result.chunk.content
            )

            if key not in scores:
                scores[key] = 0.0
                chunks[key] = result.chunk

            scores[key] += 1 / (k + rank)

    fused = [
        SearchResult(
            chunk=chunks[key],
            score=score
        )
        for key, score in scores.items()
    ]

    return sorted(
        fused,
        key=lambda result: result.score,
        reverse=True
    )