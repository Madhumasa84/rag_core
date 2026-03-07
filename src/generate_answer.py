from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from query import query_collection


model_name = "microsoft/Phi-3-mini-4k-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)


def generate_answer(question: str):
    """
    Generates an answer grounded in retrieved document context.

    Steps:
    1. Retrieve relevant document chunks using vector search.
    2. Construct a prompt containing context + question.
    3. Use a decoder model to generate the answer.

    Args:
        question (str): User question.

    Returns:
        str: Generated answer based only on document context.
    """

    results = query_collection(question)
    context_chunks = results["documents"][0]

    context = "\n".join(context_chunks)

    prompt = f"""
You are a document QA assistant.
Answer the question ONLY using the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.2
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return answer


if __name__ == "__main__":
    question = "What is this document about?"
    response = generate_answer(question)

    print("\nGenerated Answer:\n")
    print(response)