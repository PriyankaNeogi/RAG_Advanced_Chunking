from dotenv import load_dotenv
load_dotenv()

import time

from src.caching import exact_cache
from src.caching import semantic_cache
from src.caching import retrieval_cache

from src.retrieval.retriever import retrieve
from src.retrieval.reranker import rerank

from src.generation.generator import generate_answer

from src.utils.logger import get_logger
from src.utils.cache_stats import stats, print_stats

logger = get_logger()


def rag_pipeline(query):

    start_time = time.time()

    # Tier 1 Exact Cache
    response = exact_cache.get(query)

    if response:
        logger.info("Tier 1 Exact Cache Hit")
        stats["exact_hits"] += 1

        print_stats()
        return response

    # Tier 2 Semantic Cache
    response = semantic_cache.check(query)

    if response:
        logger.info("Tier 2 Semantic Cache Hit")
        stats["semantic_hits"] += 1

        print_stats()
        return response

    # Tier 3 Retrieval Cache
    chunks = retrieval_cache.get(query)

    if chunks:
        logger.info("Tier 3 Retrieval Cache Hit")
        stats["retrieval_hits"] += 1

    else:
        logger.info("Cache miss → querying Pinecone")
        stats["vector_searches"] += 1

        chunks = retrieve(query)
        chunks = rerank(query, chunks)

        retrieval_cache.set(query, chunks)

    # Parent context for LLM
    context = "\n".join(
        [c["metadata"]["parent_text"] for c in chunks]
    )

    # show document sources
    sources = "\n".join(
        [
            f'Source: {c["metadata"].get("source")} Page: {c["metadata"].get("page")}'
            for c in chunks
        ]
    )

    answer = generate_answer(query, context)

    exact_cache.set(query, answer)
    semantic_cache.store(query, answer)

    end_time = time.time()

    print(f"\nResponse time: {end_time - start_time:.2f} seconds")

    print_stats()

    return f"{answer}\n\nSources:\n{sources}"


if __name__ == "__main__":

    while True:

        query = input("\nAsk a question: ")

        if query.lower() in ["exit", "quit"]:
            print("Exiting RAG system.")
            break

        answer = rag_pipeline(query)

        print("\nAnswer:\n", answer)