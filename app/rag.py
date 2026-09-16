from app.config import (
    EMBEDDING_MODEL,
    RERANKER_MODEL,
    OPENAI_MODEL,
    HYBRID_TOP_K,
    FINAL_TOP_K
)

from app.ingestion.html_loader import HTMLLoader
from app.ingestion.cleaner import HTMLCleaner
from app.ingestion.html_parser import HTMLParser
from app.ingestion.chunker import StructureChunker

from app.indexing.embeddings import EmbeddingModel
from app.indexing.vector_index import VectorIndex
from app.indexing.bm25_index import BM25Index

from app.retrieval.vector_retriever import VectorRetriever
from app.retrieval.BM25_retriever import BM25Retriever
from app.retrieval.hybrid_retriever import HybridRetriever
from app.retrieval.reranker import Reranker

from app.generation.context_builder import ContextBuilder
from app.generation.generator import Generator


class PyTorchRAG:

    def __init__(self):
        print("Loading PyTorch documentation...")

        loader = HTMLLoader()
        cleaner = HTMLCleaner()
        parser = HTMLParser()
        chunker = StructureChunker()

        documents = loader.load()

        self.chunks = []

        for document in documents:
            soup = cleaner.clean(
                document.html
            )

            elements = parser.parse(soup)

            chunks = chunker.chunk(
                document,
                elements
            )

            self.chunks.extend(chunks)

        print(
            f"Documents: {len(documents)}"
        )

        print(
            f"Chunks: {len(self.chunks)}"
        )

        print("Creating embeddings...")

        self.embedding_model = EmbeddingModel(
            EMBEDDING_MODEL
            )


        texts = [
            f"{chunk.section}\n{chunk.content}"
            for chunk in self.chunks
        ]

        embeddings = (
            self.embedding_model.encode(texts)
        )

        self.vector_index = VectorIndex()

        self.vector_index.build(
            self.chunks,
            embeddings
        )

        self.bm25_index = BM25Index()

        self.bm25_index.build(
            self.chunks
        )

        dense = VectorRetriever(
            self.embedding_model,
            self.vector_index
        )

        sparse = BM25Retriever(
            self.bm25_index
        )

        self.hybrid = HybridRetriever(
            dense,
            sparse
        )

        self.reranker = Reranker(
            RERANKER_MODEL
        )

        self.context_builder = (
            ContextBuilder()
        )

        self.generator = None

        print("RAG ready.")

    def retrieve(self, question):

        candidates = self.hybrid.search(
            question,
            top_k=HYBRID_TOP_K
        )

        results = self.reranker.rerank(
            question,
            candidates,
            top_k=FINAL_TOP_K
        )

        return results

    def ask(self, question):

        results = self.retrieve(question)

        context, sources = (
            self.context_builder.build(
                results
            )
        )

        if self.generator is None:
            self.generator = Generator(
                OPENAI_MODEL
            )

        answer = self.generator.generate(
            question,
            context
        )

        return {
            "answer": answer,
            "sources": sources
        }