import re

from rank_bm25 import BM25Okapi

from app.models.search_result import SearchResult


class BM25Index:

    def __init__(self):
        self.index = None
        self.chunks = []

    def tokenize(self, text):
        return re.findall(
            r"[a-zA-Z0-9_.]+",
            text.lower()
        )

    def build(self, chunks):
        self.chunks = chunks

        corpus = [
            self.tokenize(
                f"{chunk.section} {chunk.content}"
            )
            for chunk in chunks
        ]

        self.index = BM25Okapi(corpus)

    def search(
        self,
        query,
        top_k=10
    ):
        query_tokens = self.tokenize(query)

        scores = self.index.get_scores(
            query_tokens
        )

        indices = scores.argsort()[::-1][:top_k]

        return [
            SearchResult(
                chunk=self.chunks[index],
                score=float(scores[index])
            )
            for index in indices
        ]