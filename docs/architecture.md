# Production-Grade RAG Pipeline Architecture

## System Overview

This project implements a production-style Retrieval-Augmented Generation (RAG) pipeline with intelligent chunking and a three-tier caching system.

The goal is to reduce redundant LLM calls, improve retrieval quality, and simulate a scalable architecture used in real-world AI systems.

---

# High Level Architecture

User Query
↓
Tier 1 Cache (Exact Match)
↓
Tier 2 Cache (Semantic Cache)
↓
Tier 3 Cache (Retrieval Cache)
↓
Vector Database (Pinecone)
↓
Reranker
↓
LLM Generator
↓
Final Answer

---

# Chunking Strategy

## Parent-Child Chunking

Documents are first split into large **parent chunks** and then into smaller **child chunks**.

Example structure:

Document  
├── Parent Chunk 1  
│   ├── Child Chunk 1  
│   ├── Child Chunk 2  
│   └── Child Chunk 3  

Retrieval happens at the **child chunk level**, while the **parent chunk provides full context to the LLM**.

Benefits:

- Higher retrieval precision
- Better contextual understanding
- Reduced hallucination

---

## Sliding Window Chunking

The second chunking strategy used is **sliding window chunking with overlap**.

Example:

Chunk 1 → tokens 0–500  
Chunk 2 → tokens 400–900  
Chunk 3 → tokens 800–1300  

Advantages:

- Maintains context across chunk boundaries
- Prevents information loss between chunks
- Improves retrieval quality

---

# Three-Tier Caching Architecture

To reduce redundant LLM calls and improve performance, three caching layers are implemented.

---

## Tier 1: Exact Cache

Stores:

Query → Response

If the same query is asked again, the cached response is returned immediately without retrieval or LLM calls.

Example:

"What is RAG?"  
→ Cached response returned instantly.

---

## Tier 2: Semantic Cache

Stores:

Query Embedding → Response

If a new query is **semantically similar** to a previous query (based on cosine similarity), the cached response is reused.

Example:

"What is RAG?"  
"Explain Retrieval Augmented Generation"

Both queries return the same cached answer.

---

## Tier 3: Retrieval Cache

Stores:

Query → Retrieved Chunks

If the retrieval results for a similar query already exist, the system skips the vector database and directly passes cached chunks to the LLM.

Benefits:

- Reduces vector DB calls
- Improves latency

---

# Query Flow

Example Query:

"What is Retrieval Augmented Generation?"

Pipeline Execution:

1. Exact cache checked
2. Semantic cache checked
3. Retrieval cache checked
4. Pinecone vector search
5. Reranking
6. Context sent to LLM
7. Final answer generated
8. Result stored in cache

---

# Design Decisions

### Vector Database

Pinecone was selected due to:

- Fast similarity search
- Managed infrastructure
- Production scalability

### Embeddings

OpenAI embeddings were used because they provide strong semantic representation for text retrieval tasks.

### Caching Backend

An in-memory dictionary cache was used for simplicity and fast lookups.

In production environments, Redis or Memcached would be preferred.

---

# Trade-offs

Pros:

- Modular architecture
- Reduced LLM cost through caching
- Better retrieval quality through parent-child chunking

Limitations:

- In-memory cache does not persist across restarts
- No distributed scaling

---

# Conclusion

This architecture demonstrates how a traditional RAG pipeline can be improved using intelligent chunking and multi-layer caching to achieve better performance, scalability, and cost efficiency.