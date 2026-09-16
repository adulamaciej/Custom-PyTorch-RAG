import numpy as np

from app.models.search_result import SearchResult


class VectorIndex:

    def __init__(self):
        self.embeddings = None
        self.chunks = []

    def build(self, chunks, embeddings):
        self.chunks = chunks
        self.embeddings = np.array(embeddings)

    def search(self, query_embedding, top_k=10):

        scores = self.embeddings @ query_embedding

        indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for index in indices:
            results.append(
                SearchResult(
                    chunk=self.chunks[index],
                    score=float(scores[index])
                )
            )

        return results