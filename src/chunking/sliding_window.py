def sliding_window_chunking(text, window_size=400, stride=200):

    chunks = []

    for i in range(0, len(text), stride):

        chunk = text[i:i + window_size]

        if chunk.strip():
            chunks.append(chunk)

    return chunks