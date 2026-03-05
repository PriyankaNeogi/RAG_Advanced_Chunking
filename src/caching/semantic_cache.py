from sklearn.metrics.pairwise import cosine_similarity
from src.utils.embeddings import get_embedding

semantic_cache = []

THRESHOLD = 0.90


def check(query):

    query_embedding = get_embedding(query)

    for item in semantic_cache:

        sim = cosine_similarity(
            [query_embedding],
            [item["embedding"]]
        )[0][0]

        if sim >= THRESHOLD:

            return item["response"]

    return None


def store(query, response):

    semantic_cache.append({
        "embedding": get_embedding(query),
        "response": response
    })