Below is a **clean, professional `README.md`** you can directly place in your repository.
It matches your project and the assignment requirements.

Copy this into:

```text
README.md
```

---

# Production-Grade RAG Pipeline with Advanced Chunking & Multi-Tier Caching

This project implements a **production-grade Retrieval-Augmented Generation (RAG) pipeline** that improves retrieval quality and system efficiency using intelligent chunking strategies and a three-tier caching architecture.

The system uses **vector search + LLM generation** to answer user queries based on ingested documents.

Key technologies include:

* Embeddings and LLM generation via OpenAI
* Vector search via Pinecone
* Modular Python architecture designed for production environments.

---

# Features

## 1. Parent–Child Chunking

Documents are split into:

**Parent chunks**

* Large contextual segments

**Child chunks**

* Smaller segments used for vector retrieval

During retrieval:

1. Child chunks are searched
2. Their parent chunks are sent to the LLM

This ensures **precise retrieval with sufficient context**.

---

## 2. Sliding Window Chunking

An additional chunking strategy implemented using overlapping windows.

Example configuration:

```
Window Size: 400
Stride: 200
```

Advantages:

* Preserves context across boundaries
* Improves semantic retrieval accuracy

---

# Three-Tier Caching System

To reduce unnecessary vector searches and LLM calls, the system implements **three caching layers**.

## Tier 1 — Exact Cache

If a query has been asked before:

```
User Query → Exact Cache → Return Response
```

No retrieval or LLM call occurs.

---

## Tier 2 — Semantic Cache

If an exact match is not found:

1. Query embedding is computed
2. Compared with cached query embeddings using cosine similarity

If similarity exceeds a threshold:

```
Similarity > 0.90 → Return Cached Answer
```

This avoids repeated LLM calls for semantically similar queries.

---

## Tier 3 — Retrieval Cache

If semantic cache misses:

The system checks whether relevant document chunks were already retrieved.

If yes:

```
Cached Chunks → LLM → Response
```

This skips the vector database query.

---

# System Architecture

```
User Query
     │
     ▼
Exact Cache
     │
     ▼
Semantic Cache
     │
     ▼
Retrieval Cache
     │
     ▼
Pinecone Vector Search
     │
     ▼
LLM Generation (OpenAI)
     │
     ▼
Final Response
```

---

# Project Structure

```
rag-project2/
│
├── README.md
├── requirements.txt
├── config.yaml
├── .env.example
│
├── main.py
│
├── scripts/
│   └── ingest.py
│
├── src/
│   ├── chunking/
│   │   ├── parent_child.py
│   │   └── sliding_window.py
│   │
│   ├── caching/
│   │   ├── exact_cache.py
│   │   ├── semantic_cache.py
│   │   └── retrieval_cache.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── generation/
│   │   └── generator.py
│   │
│   └── utils/
│       └── embeddings.py
│
├── data/
│
└── docs/
    └── architecture.md
```

---

# Installation

## 1. Clone Repository

```
git clone <your_repo_url>
cd rag-project2
```

---

## 2. Create Virtual Environment

```
python -m venv rag_env
source rag_env/bin/activate
```

Windows:

```
rag_env\Scripts\activate
```

---

## 3. Install Dependencies

```
pip install -r requirements.txt
```

---

# Environment Setup

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=us-east-1
PINECONE_INDEX_NAME=rag-index
```

---

# Pinecone Setup

Create an index in Pinecone with:

```
Index Name: rag-index
Dimension: 1536
Metric: cosine
Region: us-east-1
```

Dimension **1536** is required for OpenAI embeddings.

---

# Data Ingestion

Place documents in the `data/` folder.

Supported formats:

* `.txt`
* `.pdf`

Run ingestion:

```
python scripts/ingest.py
```

This step:

1. Loads documents
2. Applies parent-child chunking
3. Generates embeddings
4. Uploads vectors to Pinecone

---

# Running the RAG System

Start the system:

```
python main.py
```

You will see:

```
Ask a question:
```

Example:

```
What is hybrid search?
```

---

# Demonstrating the Cache

Run these queries:

```
What is hybrid search?
What is hybrid search?
Explain hybrid search
```

Expected behavior:

```
Vector search
Exact cache hit
Semantic cache hit
```

This confirms that the **three-tier caching architecture is functioning correctly**.

---

# Design Decisions

### Pinecone

Chosen for scalable and fast vector search.

### OpenAI Embeddings

Selected for high semantic accuracy.

### Parent-Child Chunking

Provides both:

* retrieval precision
* contextual completeness.

---

# Future Improvements

Possible enhancements include:

* Redis distributed caching
* Query normalization
* Hybrid sparse+dense retrieval
* Observability and cache analytics
* Streamlit or Gradio interface

---

# Conclusion

This project demonstrates how a production RAG system can be optimized using:

* hierarchical chunking
* multi-layer caching
* vector search
* LLM generation

The result is a **scalable and efficient retrieval system suitable for real-world applications**.

---


## OUTPUT - 

