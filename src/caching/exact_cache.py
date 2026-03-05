exact_cache = {}

def get(query):

    return exact_cache.get(query)

def set(query, response):

    exact_cache[query] = response