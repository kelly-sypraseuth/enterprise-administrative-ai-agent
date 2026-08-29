from llm import ask_llm


question = input("Ask the AI a test question: ")

answer = ask_llm(question)

print("\nAI response:")
print(answer)