from tools import (
    list_available_references,
    search_knowledge,
)


print("TEST 1: LIST REFERENCES")
print("=======================")

references = list_available_references()

print(references)


print("\nTEST 2: SEARCH KNOWLEDGE")
print("========================")

answer = search_knowledge(
    "What system manages Marine Corps total force information?"
)

print(answer)