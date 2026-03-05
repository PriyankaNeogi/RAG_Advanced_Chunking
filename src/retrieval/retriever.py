import os
from pinecone import Pinecone
from src.utils.embeddings import get_embedding

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))


def retrieve(query, top_k=5):

    embedding = get_embedding(query)

    results = index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True
    )

    chunks = []

    for match in results["matches"]:
        chunks.append(match["metadata"]["parent_text"])

    return chunks