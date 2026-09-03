ALLOWED_TOPICS = [
    "administration",
    "administrative",
    "personnel",
    "s-1",
    "s1",
    "marine corps",
    "mctfs",
    "tfas",
    "dla",
    "pcs",
    "tad",
    "reference",
    "references",
    "document",
    "documents",
]


def is_allowed_question(question):
    normalized_question = question.lower()

    for topic in ALLOWED_TOPICS:
        if topic in normalized_question:
            return True

    return False


def guardrail_message():
    return (
        "I can only assist with questions related to the "
        "approved S-1 and administrative reference documents "
        "available in this system."
    )