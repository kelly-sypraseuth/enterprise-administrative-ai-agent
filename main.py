import json
from matcher import get_answer
from document_search import search_document
from semantic_search import semantic_search


def load_knowledge():
    with open("knowledge.json", "r") as file:
        return json.load(file)


print("MISSO AI Agent")
print("System started successfully.")

knowledge_base = load_knowledge()

while True:
    question = input("\nWhat S-1 question can I help you with? ")

    if question.lower() == "exit":
        print("MISSO AI Agent shutting down.")
        break

    answer = search_document(question)

    if not answer:
        answer = get_answer(question, knowledge_base)

    if not answer:
        answer = semantic_search(question, knowledge_base)

    if answer:
        print(answer)
    else:
        print("I don't know that answer yet.")