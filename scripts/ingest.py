import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()

from pinecone import Pinecone
from tqdm import tqdm
from pypdf import PdfReader

from src.chunking.parent_child import parent_child_chunking
from src.utils.embeddings import get_embedding


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(INDEX_NAME)


def load_documents(folder):

    docs = []

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if file.endswith(".txt"):

            with open(path) as f:
                docs.append({
                    "text": f.read(),
                    "source": file
                })

        elif file.endswith(".pdf"):

            reader = PdfReader(path)

            for i, page in enumerate(reader.pages):

                text = page.extract_text()

                if text:
                    docs.append({
                        "text": text,
                        "source": file,
                        "page": i + 1
                    })

    return docs


def ingest():

    print("Loading documents...")

    documents = load_documents("data")

    for doc in documents:

        parents, children = parent_child_chunking(doc["text"])

        vectors = []

        for child in tqdm(children):

            embedding = get_embedding(child["text"])

            parent_text = next(
                p["text"] for p in parents if p["parent_id"] == child["parent_id"]
            )

            metadata = {
                "child_text": child["text"],
                "parent_text": parent_text,
                "source": doc["source"],
                "page": doc.get("page", -1)
            }

            vectors.append({
                "id": f'{child["parent_id"]}_{len(child["text"])}',
                "values": embedding,
                "metadata": metadata
            })

        index.upsert(vectors=vectors)

    print("Ingestion complete.")


if __name__ == "__main__":
    ingest()