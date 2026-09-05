import json

from guardrails import (
    guardrail_message,
    is_allowed_question,
)
from llm import client
from logger import write_log
from tools import (
    list_available_references,
    search_knowledge,
)


AGENT_MODEL = "gpt-5.6-luna"


TOOLS = [
    {
        "type": "function",
        "name": "search_knowledge",
        "description": (
            "Search the approved reference document knowledge base "
            "for information needed to answer an S-1 or administrative "
            "question."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": (
                        "The question to search for in the "
                        "reference knowledge base."
                    )
                }
            },
            "required": [
                "question"
            ],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "list_available_references",
        "description": (
            "List the reference documents currently available "
            "to the assistant."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    }
]


def execute_tool(tool_name, arguments):
    write_log(
        "tool_call",
        {
            "tool_name": tool_name,
            "arguments": arguments
        }
    )

    if tool_name == "search_knowledge":
        result = search_knowledge(
            arguments["question"]
        )

    elif tool_name == "list_available_references":
        result = list_available_references()

    else:
        result = "Unknown tool."

    write_log(
        "tool_result",
        {
            "tool_name": tool_name,
            "result": result
        }
    )

    return result


def run_agent(user_question):
    write_log(
        "user_question",
        {
            "question": user_question
        }
    )

    if not is_allowed_question(user_question):
        blocked_response = guardrail_message()

        write_log(
            "guardrail_block",
            {
                "question": user_question,
                "response": blocked_response
            }
        )

        return blocked_response

    response = client.responses.create(
    model=AGENT_MODEL,
    instructions=(
        "You are an S-1 administrative AI assistant. "
        "Use the available tools when the user asks about "
        "administrative reference information or available "
        "reference documents. "
        "Do not invent information that is not supported "
        "by the tools."
    ),
    input=user_question,
    tools=TOOLS,
    tool_choice="required"
)

    tool_outputs = []

    for item in response.output:
        if item.type != "function_call":
            continue

        arguments = json.loads(
            item.arguments
        )

        result = execute_tool(
            item.name,
            arguments
        )

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": result
            }
        )

    if not tool_outputs:
        fallback_response = (
            "I could not answer that question using the "
            "approved reference tools."
        )

        write_log(
            "no_tool_selected",
            {
                "question": user_question,
                "response": fallback_response
            }
        )

        return fallback_response

    final_answer = "\n\n".join(
        item["output"]
        for item in tool_outputs
    )

    write_log(
        "final_response",
        {
            "question": user_question,
            "response": final_answer
        }
    )

    return final_answer