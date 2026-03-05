def rerank(query, chunks):

    ranked = sorted(
        chunks,
        key=lambda x: len(x["metadata"]["child_text"]),
        reverse=True
    )

    return ranked[:5]