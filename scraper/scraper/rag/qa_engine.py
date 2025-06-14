# rag/qa_engine.py
def get_answer(question, knowledge_base):
    # Embed Q, search similar chunks, feed to LLM for answer
    return {
        "answer": "Pandas is a Python library for tabular data.",
        "links": ["https://tds.s-anand.net/#/2025-01/"]
    }
