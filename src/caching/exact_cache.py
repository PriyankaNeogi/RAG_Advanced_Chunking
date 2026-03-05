class ExactCache:

    def __init__(self):
        self.cache = {}

    def get(self, query):
        return self.cache.get(query)

    def set(self, query, answer):
        self.cache[query] = answer