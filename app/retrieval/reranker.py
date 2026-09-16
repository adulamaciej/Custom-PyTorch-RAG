from sentence_transformers import CrossEncoder

from app.models.search_result import SearchResult


class Reranker:

    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        self.model = CrossEncoder(
            model_name
        )

    def rerank(
        self,
        query,
        results,
        top_k=5
    ):
        pairs = [
            [
                query,
                result.chunk.content
            ]
            for result in results
        ]

        scores = self.model.predict(pairs)

        reranked = [
            SearchResult(
                chunk=result.chunk,
                score=float(score)
            )
            for result, score in zip(
                results,
                scores
            )
        ]

        reranked.sort(
            key=lambda result: result.score,
            reverse=True
        )

        return reranked[:top_k]