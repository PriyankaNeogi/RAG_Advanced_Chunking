class Reranker:

    def rerank(self, query, chunks):

        # simple scoring placeholder
        scored = sorted(chunks, key=lambda x: len(x), reverse=True)

        return scored[:3]