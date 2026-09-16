# PyTorch Documentation RAG

A custom Retrieval-Augmented Generation (RAG) system for answering questions about the official PyTorch documentation.

The project implements the retrieval pipeline without LangChain or LangGraph to demonstrate the internal mechanics of modern RAG systems.

## Architecture

```text
PyTorch HTML Documentation
        ↓
HTML Loading & Cleaning
        ↓
HTML Parsing
        ↓
Structure-Aware Chunking
        ↓
 ┌───────────────────────┐
 ↓                       ↓
Vector Search          BM25 Search
 ↓                       ↓
 └───────────┬───────────┘
             ↓
     Reciprocal Rank Fusion
             ↓
     Cross-Encoder Reranker
             ↓
         Top-K Context
             ↓
             LLM
             ↓
      Answer + Sources
```

## Features

- Ingestion of rendered PyTorch HTML documentation
- HTML cleaning and structure-aware parsing
- Structure-aware chunking based on document hierarchy
- Local dense embeddings with BGE
- Semantic vector search
- BM25 keyword retrieval
- Hybrid retrieval
- Reciprocal Rank Fusion (RRF)
- Cross-encoder reranking
- Top-K context construction
- Source citations
- OpenAI-based answer generation
- FastAPI REST API
- Streamlit interface
- Pytest tests

## Tech Stack

- Python
- BeautifulSoup
- Sentence Transformers
- BGE embeddings
- NumPy
- rank-bm25
- Cross-Encoder
- OpenAI API
- FastAPI
- Pydantic
- Streamlit
- Pytest
- Docker

## Project Structure

```text
app/
├── api/
│   └── main.py
├── generation/
│   ├── context_builder.py
│   ├── prompts.py
│   └── generator.py
├── indexing/
│   ├── embeddings.py
│   ├── vector_index.py
│   └── bm25_index.py
├── ingestion/
│   ├── html_loader.py
│   ├── cleaner.py
│   ├── html_parser.py
│   └── chunker.py
├── models/
│   ├── document.py
│   ├── chunk.py
│   └── search_result.py
├── retrieval/
│   ├── vector_retriever.py
│   ├── bm25_retriever.py
│   ├── hybrid_retriever.py
│   ├── rrf.py
│   └── reranker.py
├── config.py
└── rag.py

scripts/
├── download_docs.py
└── build_index.py

tests/
ui/
data/
```

## Retrieval Pipeline

The system combines two retrieval methods:

1. **Vector retrieval** for semantic similarity.
2. **BM25 retrieval** for exact terminology and PyTorch API names.

The rankings are combined using **Reciprocal Rank Fusion (RRF)**.

The fused candidates are then scored by a **cross-encoder reranker**, and the final Top-K chunks are passed to the LLM as context.

## Installation

Clone the repository:

```bash
git clone https://github.com/adulamaciej/Semantic-Retrieval-RAG-Evaluation-System.git
cd Semantic-Retrieval-RAG-Evaluation-System
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a local `.env` file:

```bash
cp .env.example .env
```

Then add your API key:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=your_model_name
```

Do not commit `.env`.

## Download PyTorch Documentation

```bash
python scripts/download_docs.py
```

## Test the Retrieval Pipeline

```bash
python -m scripts.build_index
```

## Run Tests

```bash
python -m pytest -v
```

## Run Streamlit

```bash
python -m streamlit run ui/streamlit_app.py
```

## Run FastAPI

```bash
python -m uvicorn app.api.main:app --reload
```

FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

## Example Query

```text
How do I disable gradient computation?
```

The system retrieves relevant sections from the PyTorch documentation, combines BM25 and vector search results, reranks the candidates, builds the final context, and generates an answer with sources.

## Why This Project?

The goal of this project is to demonstrate the internal mechanics of a production-style RAG pipeline instead of relying on high-level orchestration frameworks.

It includes custom document ingestion, hybrid retrieval, rank fusion, reranking, context construction, answer generation, API access, and a simple UI.
