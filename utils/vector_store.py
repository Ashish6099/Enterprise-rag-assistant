import os
import uuid
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_DIR = "vectorstore"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vector_store(chunks, session_id: str):

    embeddings = get_embeddings()

    session_path = os.path.join(DB_DIR, session_id)

    # Create only ONCE per session
    if not os.path.exists(session_path):

        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=session_path
        )

    else:
        vector_db = Chroma(
            persist_directory=session_path,
            embedding_function=embeddings
        )

    return vector_db, session_path