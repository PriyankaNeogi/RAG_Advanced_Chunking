

## Production-Grade RAG Pipeline with Advanced Chunking & Multi-Tier Caching

## 1. System Overview

This project implements a **production-grade Retrieval-Augmented Generation (RAG) pipeline** designed to improve both efficiency and response quality in LLM-powered applications.

Traditional RAG pipelines perform retrieval and generation for every query, which leads to:

* Increased latency
* Higher API costs
* Redundant computation

To solve this, the system introduces:

* **Parent-Child Chunking**
* **Sliding Window Chunking**
* **Three-Tier Caching System**

The pipeline uses:

* Embeddings via OpenAI
* Vector search via Pinecone
* LLM response generation via OpenAI models.

---

# 2. System Architecture

```
                ┌───────────────────┐
                │     User Query     │
                └─────────┬─────────┘
                          │
                          ▼
                 ┌────────────────┐
                 │ Exact Cache     │
                 │ (Tier 1)        │
                 └────────┬───────┘
                          │ miss
                          ▼
                 ┌────────────────┐
                 │ Semantic Cache  │
                 │ (Tier 2)        │
                 └────────┬───────┘
                          │ miss
                          ▼
                 ┌────────────────┐
                 │ Retrieval Cache │
                 │ (Tier 3)        │
                 └────────┬───────┘
                          │ miss
                          ▼
                ┌────────────────────┐
                │ Pinecone Retrieval │
                └────────┬───────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │ Reranking       │
                 └────────┬───────┘
                          │
                          ▼
                 ┌────────────────┐
                 │ LLM Generation  │
                 │ (OpenAI)        │
                 └────────┬───────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   Response   │
                   └─────────────┘
```

---

# 3. Chunking Strategy

## Parent-Child Chunking

Parent-child chunking preserves document context.

### Parent Chunks

Large chunks representing broader document sections.

Example configuration:

```
Parent Chunk Size: 1000 characters  
Parent Overlap: 100
```

### Child Chunks

Smaller chunks used for vector search.

```
Child Chunk Size: 200 characters  
Child Overlap: 40
```

### Workflow

1. Documents are split into **parent chunks**.
2. Each parent chunk is further split into **child chunks**.
3. Child chunks are embedded and stored in the vector database.
4. During retrieval:

   * Child chunks are searched.
   * Their parent chunks are returned to the LLM.

This ensures **precise retrieval with full context**.

---

# 4. Second Chunking Strategy: Sliding Window

A sliding window approach was implemented as an additional chunking strategy.

Example configuration:

```
Window Size: 400
Stride: 200
```

### How it works

Instead of splitting text into fixed chunks, overlapping windows slide through the text.

Example:

```
Chunk 1 → characters 0–400  
Chunk 2 → characters 200–600  
Chunk 3 → characters 400–800
```

### Benefits

* Maintains context across chunk boundaries
* Reduces information loss
* Improves semantic retrieval accuracy

### Comparison

| Strategy       | Strength                        |
| -------------- | ------------------------------- |
| Parent-Child   | Best for hierarchical documents |
| Sliding Window | Best for continuous text        |

---

# 5. Three-Tier Caching Architecture

To reduce redundant computation, the system implements **three caching layers**.

---

## Tier 1 — Exact Cache

Checks if the query has been asked before.

Example:

```
Query: "What is hybrid search?"
```

If an exact match exists, the cached answer is returned immediately.

Benefits:

* Zero retrieval
* Zero LLM calls
* Lowest latency

---

## Tier 2 — Semantic Cache

If no exact match exists, the query embedding is compared against cached queries.

Similarity is measured using **cosine similarity**.

If similarity exceeds threshold:

```
Threshold: 0.90
```

the cached response is returned.

Example:

```
Query 1: "What is hybrid search?"
Query 2: "Explain hybrid search"
```

These are semantically similar and can reuse cached answers.

---

## Tier 3 — Retrieval Cache

Stores previously retrieved document chunks.

If similar queries occur again:

* Pinecone retrieval is skipped
* Cached chunks are used directly

This saves vector search time.

---

# 6. Cache Storage

For this implementation, caching uses **in-memory dictionaries**.

Example:

```
Exact Cache → {query: response}
Semantic Cache → {embedding: response}
Retrieval Cache → {query: retrieved_chunks}
```

### Why In-Memory Cache?

Advantages:

* Extremely fast
* Simple implementation
* No external dependency

Trade-off:

* Cache resets when the application restarts.

In production systems, Redis could be used instead.

---

# 7. Query Flow Walkthrough

Example query:

```
User: What is hybrid search?
```

### Step 1 — Exact Cache

System checks if the query already exists.

If yes → return cached response.

If no → continue.

---

### Step 2 — Semantic Cache

Query embedding is compared with cached queries.

If similarity > threshold → return cached response.

If not → continue.

---

### Step 3 — Retrieval Cache

System checks if document chunks were previously retrieved.

If yes → reuse cached chunks.

If not → continue.

---

### Step 4 — Vector Search

Query embedding is sent to Pinecone.

Top-K relevant chunks are retrieved.

---

### Step 5 — LLM Generation

Retrieved parent chunks are passed to the LLM.

The model generates the final answer.

---

### Step 6 — Cache Update

The result is stored in:

* Exact cache
* Semantic cache
* Retrieval cache

for future queries.

---

# 8. Design Decisions

### Why Pinecone?

Chosen for:

* Fast vector search
* Scalability
* Managed infrastructure

### Why OpenAI Embeddings?

Chosen because:

* High semantic accuracy
* Compatible with Pinecone
* Easy API integration

### Why Parent-Child Chunking?

Because it balances:

* Retrieval precision
* Context preservation

---

# 9. Future Improvements

Possible improvements include:

* Redis-based distributed caching
* Query normalization
* Streaming responses
* Hybrid sparse + dense retrieval
* Monitoring and cache analytics

---

# Conclusion

This system demonstrates how modern RAG pipelines can be optimized through:

* Intelligent chunking
* Multi-tier caching
* Efficient retrieval

The result is a **scalable, cost-efficient, production-ready RAG architecture**.

---


If you want, I can also show you **one small improvement that makes your GitHub repo look much more “production-grade” to evaluators**.
