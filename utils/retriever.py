import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_DIR = "vectorstore"


def get_relevant_chunks(query, session_id: str, k=3):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    session_path = os.path.join(DB_DIR, session_id)

    vector_db = Chroma(
        persist_directory=session_path,
        embedding_function=embeddings
    )

    results = vector_db.similarity_search_with_score(
    query=query,
    k=k
    )

    return results