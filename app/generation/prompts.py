SYSTEM_PROMPT = """
You are a PyTorch documentation assistant.

Answer only using the provided PyTorch documentation context.

If the context does not contain enough information,
say that you do not have enough information.

Use citations such as [1], [2] when referring to sources.
Do not invent PyTorch APIs or behavior.
"""


def build_prompt(
    question,
    context
):
    return f"""
CONTEXT:

{context}

QUESTION:

{question}

Answer the question using only the context above.
"""