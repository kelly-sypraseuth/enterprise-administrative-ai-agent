import os

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from the .env file
load_dotenv()


# Create the OpenAI client using the API key stored in .env
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def ask_llm(question, context=None):
    if context:
        prompt = f"""
Use only the reference information below to answer the question.

Reference information:
{context}

Question:
{question}

If the reference information does not support the answer, say:
"I cannot determine that from the provided reference."
"""
    else:
        prompt = question

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions=(
            "You are a training assistant for MISSO and unit S-1 personnel. "
            "Do not assume access to any Marine Corps system. "
            "Do not request or process real PII, CUI, credentials, or operational records. "
            "Provide clear educational explanations."
        ),
        input=prompt,
    )

    return response.output_text