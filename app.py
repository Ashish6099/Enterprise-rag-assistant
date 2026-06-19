# ==========================================
# Enterprise RAG Knowledge Assistant
# Production MVP Version
# ==========================================

import streamlit as st
import os
import uuid

from utils.pdf_loader import load_and_chunk_pdf
from utils.vector_store import create_vector_store
from utils.retriever import get_relevant_chunks
from utils.rag_chain import generate_answer

# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="Enterprise RAG Assistant",
    page_icon="📚",
    layout="wide"
)

# ==========================================
# Session State Initialization
# ==========================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "vector_ready" not in st.session_state:
    st.session_state.vector_ready = False

if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None

# Multi Chat Support

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}

if "current_chat" not in st.session_state:

    first_chat = str(uuid.uuid4())

    st.session_state.current_chat = first_chat

    st.session_state.chat_sessions[first_chat] = {
        "title": "New Chat",
        "messages": []
    }

# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.title("📚 RAG Assistant")

    # New Chat

    if st.button("➕ New Chat"):

        new_chat_id = str(uuid.uuid4())

        st.session_state.chat_sessions[new_chat_id] = {
            "title": "New Chat",
            "messages": []
        }

        st.session_state.current_chat = new_chat_id

        # Reset vector session

        st.session_state.vector_ready = False
        st.session_state.last_uploaded_file = None
        st.session_state.session_id = str(uuid.uuid4())

        st.rerun()
    

    st.divider()

    st.subheader("Chat History")

    for chat_id, chat_data in st.session_state.chat_sessions.items():

        if st.button(
            chat_data["title"],
            key=chat_id
        ):
            st.session_state.current_chat = chat_id
            st.rerun()
           
    st.divider()

    st.subheader("📊 System Status")

    st.write(
            f"Vector Ready: {'✅' if st.session_state.vector_ready else '❌'}"
        )

    if st.session_state.last_uploaded_file:
            st.write(
                f"📄 {st.session_state.last_uploaded_file}"
            )
    else:
            st.write("No PDF uploaded")
# ==========================================
# Main Page
# ==========================================

st.title("📚 Enterprise RAG Knowledge Assistant")
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.metric(
#         "Chats",
#         len(st.session_state.chat_sessions)
#     )

# with col2:
#     st.metric(
#         "Vector Store",
#         "Ready" if st.session_state.vector_ready else "Not Ready"
#     )

# with col3:
#     st.metric(
#         "Model",
#         "GPT"
#     )

st.markdown(
    """
Upload a PDF, create embeddings, and chat with your documents using RAG.
"""
)

# ==========================================
# Upload Folder
# ==========================================

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

# ==========================================
# PDF Upload
# ==========================================
with st.container():

    # st.subheader("📄 Upload Knowledge Base")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

# ==========================================
# Process PDF
# ==========================================

if uploaded_file is not None:

    if uploaded_file.name != st.session_state.last_uploaded_file:

        st.session_state.last_uploaded_file = uploaded_file.name

        file_path = os.path.join(
            UPLOAD_DIR,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(
            f"Successfully uploaded: {uploaded_file.name}"
        )

        try:

            chunks = load_and_chunk_pdf(
                file_path
            )

            st.subheader(
                "📄 Document Statistics"
            )

            st.write(
                f"Total Chunks Created: {len(chunks)}"
            )

            if chunks:

                with st.expander(
                    "Preview First Chunk"
                ):
                    st.write(
                        chunks[0].page_content[:1000]
                    )

                with st.spinner(
                    "Creating embeddings..."
                ):

                    vector_db, path = create_vector_store(
                        chunks,
                        st.session_state.session_id
                    )

                st.session_state.vector_ready = True

                st.success(
                    "Embeddings created successfully"
                )

                st.write(
                    f"Vector Store Path: {path}"
                )

        except Exception as e:

            st.error(str(e))

# ==========================================
# Load Current Chat
# ==========================================

current_messages = st.session_state.chat_sessions[
    st.session_state.current_chat
]["messages"]

# ==========================================
# Display Conversation
# ==========================================

if current_messages:

    st.subheader("Conversation")

    for msg in current_messages:

        # -------------------------
        # User Message
        # -------------------------

        with st.chat_message("user"):
            st.write(msg["question"])

        # -------------------------
        # Assistant Message
        # -------------------------

        with st.chat_message("assistant"):

            st.write(msg["answer"])
            st.success(
                    "Answer generated successfully"
                )
            # -------------------------
            # Retrieved Sources
            # -------------------------

            if "sources" in msg and msg["sources"]:

                with st.expander("📚 Sources Used"):

                    for i, source in enumerate(
                        msg["sources"],
                        start=1
                    ):

                        st.markdown(
                            f"### Source {i} (Rank #{i})"
                        )

                        if "score" in source:

                            st.write(
                                f"Retrieval Score: {source['score']:.4f}"
                            )

                        st.write(
                            source["content"]
                        )

            st.divider()
# ==========================================
# Chat Input
# ==========================================

question = st.chat_input(
    "Ask something about your document..."
)

# ==========================================
# Ask Question
# ==========================================

if question:

    if not st.session_state.vector_ready:

        st.warning(
            "Please upload a PDF first."
        )

    else:

        try:

            # Retrieve Context

            with st.spinner(
                "Searching knowledge base..."
            ):

                results = get_relevant_chunks(
                    question,
                    st.session_state.session_id,
                    k=3
                )

            # Generate Answer

            with st.spinner(
                "Generating answer..."
            ):

                answer = generate_answer(
                    question,
                    results
                )

            # Auto Rename Chat

            if st.session_state.chat_sessions[
                st.session_state.current_chat
            ]["title"] == "New Chat":

                st.session_state.chat_sessions[
                    st.session_state.current_chat
                ]["title"] = question[:30]

            # Store Sources

            stored_sources = []

            for doc, score in results:

                stored_sources.append(
                    {
                        "content": doc.page_content,
                        "score": float(score)
                    }
                )

            # Save Message

            st.session_state.chat_sessions[
                st.session_state.current_chat
            ]["messages"].append(
                {
                    "question": question,
                    "answer": answer,
                    "sources": stored_sources
                }
            )

            # Current Exchange

            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):

                st.write(answer)

                with st.expander(
    "📚 Sources Used"
):

                    for i, source in enumerate(
                        stored_sources,
                        start=1
                    ):

                        st.markdown(
                            f"### Source {i} (Rank #{i})"
                        )

                        # Raw vector distance score
                        if "score" in source:

                            st.write(
                                f"Retrieval Score: {source['score']:.4f}"
                            )

                        st.write(
                            source["content"]
                        )

                        st.divider()

        except Exception as e:

            st.error(str(e))