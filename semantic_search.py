from difflib import SequenceMatcher


def similarity_score(text1, text2):
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def semantic_search(question, knowledge_base):
    best_score = 0
    best_answer = None

    for topic, details in knowledge_base.items():
        for keyword in details["keywords"]:
            score = similarity_score(question, keyword)

            if score > best_score:
                best_score = score
                best_answer = details["answer"]

    if best_score >= 0.40:
        return best_answer

    return None