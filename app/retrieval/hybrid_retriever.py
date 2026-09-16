from app.retrieval.rrf import reciprocal_rank_fusion


class HybridRetriever:

    def __init__(
        self,
        vector_retriever,
        bm25_retriever
    ):
        self.vector_retriever = vector_retriever
        self.bm25_retriever = bm25_retriever

    def search(
        self,
        query,
        top_k=20
    ):
        vector_results = self.vector_retriever.search(
            query,
            top_k=top_k
        )

        bm25_results = self.bm25_retriever.search(
            query,
            top_k=top_k
        )

        results = reciprocal_rank_fusion(
            [
                vector_results,
                bm25_results
            ]
        )

        return results[:top_k]