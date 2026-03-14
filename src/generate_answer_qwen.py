# src/generate_answer_qwen.py

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from query import query_collection
import time

# Model ID from your research
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

print(f"Loading {MODEL_NAME}... (this may take a minute on first run)")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,  # Explicitly use float32 for CPU
    low_cpu_mem_usage=True
)

print("Model loaded successfully!")

def generate_answer(question: str, top_k: int = 3) -> str:
    """
    Generates answer using Qwen2.5-1.5B grounded in retrieved document chunks.
    
    Args:
        question (str): User's question
        top_k (int): Number of chunks to retrieve
        
    Returns:
        str: Generated answer based only on document context
    """
    
    # Step 1: Retrieve relevant chunks
    print(f"Retrieving chunks for: '{question}'")
    results = query_collection(question)
    context_chunks = results["documents"][0][:top_k]
    
    # Step 2: Combine chunks into context
    context = "\n\n".join(context_chunks)
    
    # Step 3: Format prompt for Qwen (uses chat template)
    messages = [
        {
            "role": "system", 
            "content": "You are a document QA assistant. Answer ONLY using the provided context. If the answer cannot be found in the context, say 'I cannot find this information in the document.'"
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }
    ]
    
    # Applying chat template
    prompt = tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
    )
    
    # Step 4: Generate answer
    print("Generating answer...")
    inputs = tokenizer(prompt, return_tensors="pt")
    
    with torch.no_grad():  # No gradients needed for inference
        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.1,  # Low temperature for factual answers
            do_sample=True,
            top_p=0.9
        )
    
    # Step 5: Decode and clean answer
    full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract only the assistant's response (after the last "assistant")
    if "assistant" in full_output:
        answer = full_output.split("assistant")[-1].strip()
    else:
        answer = full_output.replace(prompt, "").strip()
    
    return answer


def quick_test():
    """Quick test function"""
    test_questions = [
        "What is this document about?",
        "What is the main problem discussed?",
        "Who is the author?"
    ]
    
    for q in test_questions:
        print("\n" + "="*50)
        print(f"Q: {q}")
        print("-"*50)
        answer = generate_answer(q)
        print(f"A: {answer}")
        print("="*50)


    start = time.time()
    answer = generate_answer("What is this document about?")
    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")    


if __name__ == "__main__":
    quick_test()