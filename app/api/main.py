from functools import lru_cache
from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import PyTorchRAG


app = FastAPI(
    title="PyTorch RAG API"
)


class QuestionRequest(BaseModel):
    question: str


@lru_cache
def get_rag():
    return PyTorchRAG()


@app.get("/")
def root():
    return {
        "message": "PyTorch RAG API"
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    rag = get_rag()

    return rag.ask(
        request.question
    )