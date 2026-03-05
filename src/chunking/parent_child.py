from langchain_text_splitters import RecursiveCharacterTextSplitter


def parent_child_chunking(text):

    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=40
    )

    parents = parent_splitter.split_text(text)

    parent_chunks = []
    child_chunks = []

    for i, parent in enumerate(parents):

        parent_id = f"parent_{i}"

        parent_chunks.append({
            "parent_id": parent_id,
            "text": parent
        })

        children = child_splitter.split_text(parent)

        for child in children:
            child_chunks.append({
                "parent_id": parent_id,
                "text": child
            })

    return parent_chunks, child_chunks