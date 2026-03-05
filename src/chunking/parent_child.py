def parent_child_chunking(text, parent_size=2000, child_size=400):

    parents = []
    children = []

    for i in range(0, len(text), parent_size):

        parent_text = text[i:i+parent_size]
        parent_id = f"parent_{i}"

        parents.append({
            "parent_id": parent_id,
            "text": parent_text
        })

        for j in range(0, len(parent_text), child_size):

            child = parent_text[j:j+child_size]

            children.append({
                "text": child,
                "parent_id": parent_id
            })

    return parents, children