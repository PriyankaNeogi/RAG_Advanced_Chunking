retrieval_cache = {}

def get(query):

    return retrieval_cache.get(query)


def set(query, chunks):

    retrieval_cache[query] = chunks