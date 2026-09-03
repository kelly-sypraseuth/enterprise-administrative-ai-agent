from agent import run_agent


print("AI AGENT TEST")
print("=============")

question = input(
    "Ask the AI agent a question: "
)

answer = run_agent(
    question
)

print("\nAgent response:")
print(answer)