import numpy as np
from src.utils.embeddings import get_embedding


class SemanticCache:

    def __init__(self, threshold=0.9):
        self.cache = []
        self.threshold = threshold

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get(self, query):

        query_emb = get_embedding(query)

        for item in self.cache:

            score = self.cosine_similarity(query_emb, item["embedding"])

            if score > self.threshold:
                return item["answer"]

        return None

    def set(self, query, answer):

        emb = get_embedding(query)

        self.cache.append({
            "query": query,
            "embedding": emb,
            "answer": answer
        })