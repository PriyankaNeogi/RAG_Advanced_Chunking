class RetrievalCache:

    def __init__(self):
        self.cache = {}

    def get(self, query):
        return self.cache.get(query)

    def set(self, query, chunks):
        self.cache[query] = chunks