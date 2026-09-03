import streamlit as st

from agent import run_agent


st.set_page_config(
    page_title="MISSO AI Agent",
    page_icon="🤖",
    layout="centered"
)


st.title("MISSO AI Agent")

st.caption(
    "AI-assisted administrative reference system "
    "using approved project documents."
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

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )