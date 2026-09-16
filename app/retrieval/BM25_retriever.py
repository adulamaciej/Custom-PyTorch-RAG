class BM25Retriever:

    def __init__(self, bm25_index):
        self.bm25_index = bm25_index

    def search(self, query, top_k=10):

        return self.bm25_index.search(
            query,
            top_k=top_k
        )