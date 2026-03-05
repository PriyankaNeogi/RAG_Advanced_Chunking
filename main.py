from src.caching.exact_cache import ExactCache
from src.caching.semantic_cache import SemanticCache
from src.caching.retrieval_cache import RetrievalCache
from src.retrieval.retriever import retrieve
from src.generation.generator import generate_answer

exact_cache = ExactCache()
semantic_cache = SemanticCache()
retrieval_cache = RetrievalCache()


def ask(query):

    exact = exact_cache.get(query)

    if exact:
        print("Exact cache hit")
        return exact

    semantic = semantic_cache.get(query)

    if semantic:
        print("Semantic cache hit")
        return semantic

    chunks = retrieval_cache.get(query)

    if not chunks:
        print("Vector search")
        chunks = retrieve(query)
        retrieval_cache.set(query, chunks)

    answer = generate_answer(query, chunks)

    exact_cache.set(query, answer)
    semantic_cache.set(query, answer)

    return answer


if __name__ == "__main__":

    while True:

        q = input("Ask a question: ")

        print(ask(q))