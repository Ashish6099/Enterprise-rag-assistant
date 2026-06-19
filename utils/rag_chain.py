from utils.llm import get_llm


def generate_answer(question, docs):

    llm = get_llm()

    context = "\n\n".join(
        [doc.page_content for doc, score in docs]
    )

    prompt = f"""
You are an enterprise AI assistant.

Answer ONLY using the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content