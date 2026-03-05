from pinecone import Pinecone
import os
from src.utils.embeddings import get_embedding

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))


def retrieve(query, top_k=5):

    vector = get_embedding(query)

    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )

    return results["matches"]