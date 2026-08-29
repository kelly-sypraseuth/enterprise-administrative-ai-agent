def chunk_text(text, chunk_size=500, overlap=100):
    words = text.split()

    chunks = []

    start = 0
    chunk_number = 1

    while start < len(words):
        end = start + chunk_size

        chunk_words = words[start:end]

        chunk_text_value = " ".join(chunk_words)

        chunks.append(
            {
                "chunk_number": chunk_number,
                "text": chunk_text_value
            }
        )

        chunk_number += 1

        start += chunk_size - overlap

    return chunks