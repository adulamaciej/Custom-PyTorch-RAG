import os
from dotenv import load_dotenv


load_dotenv()


EMBEDDING_MODEL = (
    "BAAI/bge-small-en-v1.5"
)

RERANKER_MODEL = (
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna"
)

DENSE_TOP_K = 20
HYBRID_TOP_K = 20
FINAL_TOP_K = 5