stats = {
    "exact_hits": 0,
    "semantic_hits": 0,
    "retrieval_hits": 0,
    "vector_searches": 0
}

def print_stats():
    print("\nCache Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")