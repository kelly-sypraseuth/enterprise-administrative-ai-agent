def get_answer(question, knowledge_base):
    normalized_question = question.lower().strip()

    for topic, details in knowledge_base.items():
        for keyword in details["keywords"]:
            if keyword in normalized_question:
                return details["answer"]

    return None