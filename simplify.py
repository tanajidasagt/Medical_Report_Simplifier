from transformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st

@st.cache_resource
def load_model():
    model_name = "microsoft/phi-2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model


def simplify_text(text):
    tokenizer, model = load_model()

    prompt = f"""
Rewrite the following medical sentence in simple and clear language.

Rules:
- Only output ONE sentence
- Do NOT add explanation
- Do NOT add extra text
- Do NOT repeat the input

Sentence:
{text}

Simplified:
"""

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=100,   # 🔥 better than max_length
        temperature=0.2,     # 🔥 less randomness
        do_sample=True
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # 🔥 Clean output (important)
    result = result.split("Simplified:")[-1].strip()
    result = result.split("\n")[0]   # remove extra lines

    return result
