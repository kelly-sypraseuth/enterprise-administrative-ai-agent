import streamlit as st

from agent import run_agent


st.set_page_config(
    page_title="Enterprise Administrative AI Agent",
    page_icon="🤖",
    layout="centered"
)


st.title("Enterprise Administrative AI Agent")

st.caption(
    "AI-assisted administrative reference system "
    "using approved project documents."
)

st.markdown(
    "**Capabilities:** RAG • Semantic Search • Tool Calling • "
    "Guardrails • Audit Logging"
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )


question = st.chat_input(
    "Ask an administrative question..."
)


if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner(
            "Searching approved references..."
        ):
            answer = run_agent(
                question
            )

        if "\n\nSources:\n" in answer:
            main_answer, sources = answer.split(
                "\n\nSources:\n",
                1
            )

            st.markdown(main_answer)

            with st.expander(
                "View source references"
            ):
                st.markdown(sources)

        else:
            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )