class VectorRetriever:

    def __init__(self, embedding_model, vector_index):
        self.embedding_model = embedding_model
        self.vector_index = vector_index

    def search(self, query, top_k=10):

        query_embedding = self.embedding_model.encode(
            [query]
        )[0]

        return self.vector_index.search(
            query_embedding,
            top_k=top_k
        )