# import os
#
# import streamlit as st
# from langchain_openai import OpenAI, OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from main import make_chat, build_vector_store, load_and_split
#
# st.set_page_config(page_title="PDF Chatbot",page_icon = "📂")
# st.title("PDF Chatbot")
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# @st.cache_resource
# def get_chain():
#     vectordb = FAISS.load_local("faiss_store",OpenAIEmbeddings(), allow_dangerous_deserialization=True)
#     return make_chat(vectordb)
# chain = get_chain()
# chat_history = st.session_state.setdefault("history",[])
# user_input = st.chat_input("Ask about your notes... ")
#
# if user_input:
#     response = chain({"question":user_input})
#     chat_history.append(("user",user_input))
#     chat_history.append("bot",response["answer"])
#
# for role, msg in chat_history:
#     st.chat_message(role).write(msg)
#

"""
Streamlit GUI for the PDF chatbot.
Run with:  streamlit run ui.py
"""

import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from main import make_chat_chain, get_vector_store, VECTOR_STORE

st.set_page_config(page_title="PDF Chatbot", page_icon="📂")
st.title("PDF Chatbot")

# ------------------------------------------------------------------
# Build / load the FAISS index once per session
# ------------------------------------------------------------------
@st.cache_resource
def load_chain():
    vectordb = FAISS.load_local(
        VECTOR_STORE,
        OpenAIEmbeddings(),
        allow_dangerous_deserialization=True,
    )
    return make_chat_chain(vectordb)


# first run: make sure the store exists (build if necessary)
get_vector_store()   # creates VECTOR_STORE if missing

chain = load_chain()

# ------------------------------------------------------------------
# Chat loop
# ------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []  # list of (role, message) tuples

user_input = st.chat_input("Ask about your notes …")

if user_input:
    result = chain({"question": user_input})
    st.session_state.history.extend(
        [
            ("user", user_input),
            ("assistant", result["answer"]),
        ]
    )

# Display the full conversation
for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)
