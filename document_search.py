def search_document(question):
    with open("documents/s1_reference.txt", "r") as file:
        document_text = file.read()

    normalized_question = question.lower()

    for line in document_text.splitlines():
        normalized_line = line.lower()

        if "dla" in normalized_question and "dla" in normalized_line:
            return line

        if "tad" in normalized_question and "tad" in normalized_line:
            return line

        if "pcs" in normalized_question and "pcs" in normalized_line:
            return line

        if "mctfs" in normalized_question and "mctfs" in normalized_line:
            return line

    return None