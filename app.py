import streamlit as st
from simplify import simplify_text
from ner import extract_terms

medical_dict = {
    "hypertension": "high blood pressure",
    "diabetes": "a condition where blood sugar levels are too high",
    "glucose": "a type of sugar in the blood"
}

st.set_page_config(page_title="Medical Report Simplifier")

st.title("🏥 Patient-Centric Medical Report Simplifier")

text = st.text_area("Enter Medical Report:", height=200)

if st.button("Simplify Report"):

    if text.strip() == "":
        st.warning("Please enter some medical text.")
    else:
        st.subheader("Simplified Report")
        simplified = simplify_text(text)
        st.success(simplified)

        st.subheader("Medical Term Explanations")
        terms = extract_terms(text)

        if not terms:
            st.write("No medical terms detected.")
        else:
            for term, label in terms:
                explanation = medical_dict.get(term.lower(), "No simple explanation available")
                st.write(f"**{term}** → {explanation}")
