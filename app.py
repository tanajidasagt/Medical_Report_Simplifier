import streamlit as st
from simplify import simplify_text
from ner import extract_terms

medical_dict = {
    "hypertension": "high blood pressure",
    "diabetes": "a condition where blood sugar levels are too high",
    "glucose": "a type of sugar in the blood",
    "fever": "an increase in body temperature",
    "infection": "when harmful microorganisms enter the body",
    "cancer": "uncontrolled growth of abnormal cells",
    "cholesterol": "a fatty substance in the blood",
    "asthma": "a condition that affects breathing",
    "anemia": "low red blood cells causing weakness",
    "obesity": "excess body fat that may affect health"
}

advice_dict = {
    "hypertension": ["Reduce salt intake", "Exercise regularly", "Manage stress"],
    "diabetes": ["Maintain a low sugar diet", "Exercise regularly", "Monitor blood sugar levels"],
    "glucose": ["Maintain a balanced diet", "Avoid excessive sugar intake", "Monitor blood sugar levels"],
    "fever": ["Stay hydrated", "Take proper rest", "Consult a doctor if it persists"],
    "infection": ["Maintain proper hygiene", "Wash hands regularly", "Avoid contaminated food and water"],
    "cancer": ["Follow regular medical checkups", "Avoid tobacco and alcohol", "Maintain a healthy lifestyle"],
    "cholesterol": ["Avoid fatty and fried foods", "Exercise regularly", "Eat more fruits and vegetables"],
    "asthma": ["Avoid dust and pollution", "Practice breathing exercises", "Use inhalers if prescribed"],
    "anemia": ["Consume iron-rich foods", "Maintain a nutritious diet", "Consult a doctor if needed"],
    "obesity": ["Maintain a balanced diet", "Exercise regularly", "Avoid junk food"]
}

default_advice = [
    "Maintain a healthy lifestyle",
    "Exercise regularly",
    "Eat a balanced diet",
    "Consult a doctor if needed"
]

st.set_page_config(page_title="Medical Report Simplifier")

st.markdown("""
<style>

/* Background */
body {
    background-color: #0e1117;
}

/* Title */
h1 {
    font-size: 42px !important;
    font-weight: 700 !important;
    text-align: center;
    margin-bottom: 10px;
}

/* Label */
.custom-label {
    font-size: 22px;
    font-weight: 500;
    margin-top: 20px;
}

/* Text area */
textarea {
    border-radius: 12px !important;
    padding: 15px !important;
    font-size: 16px !important;
    background-color: #1c1f26 !important;
    color: white !important;
    border: 1px solid #2c2f36 !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    font-size: 16px;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    transition: 0.3s ease;
}

/* Button hover */
.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #0072ff, #00c6ff);
}

/* Result box */
.result-box {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    font-size: 18px;
    color: #00ff9f;
    border: 1px solid #2c2f36;
    margin-top: 10px;
}

/* Section spacing */
h2, h3 {
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)

st.title("🏥 Patient-Centric Medical Report Simplifier")

#st.markdown("<p class='custom-label'>Enter Medical Report:</p>", unsafe_allow_html=True)

st.markdown(
    "<p style='font-size:22px; font-weight:600;'>Enter Medical Report:</p>",
    unsafe_allow_html=True
)

text = st.text_area("", height=300)

if st.button("Simplify Report"):

    if text.strip() == "":
        st.warning("Please Enter your report.")
    else:
    
        st.subheader("Simplified Report")
        simplified = simplify_text(text)

        st.markdown(
            f"<div class='result-box'>{simplified}</div>",
            unsafe_allow_html=True
        )

        terms = extract_terms(text)

        filtered_terms = []
        for term in terms:
            clean_term = term.lower().rstrip("s")
            if clean_term in medical_dict:
                filtered_terms.append(clean_term)

        filtered_terms = list(set(filtered_terms))

        st.subheader("Medical Term Explanations")

        if not filtered_terms:
            st.write("No medical terms detected.")
        else:
            for term in filtered_terms:
                explanation = medical_dict[term]
                st.write(f"🔹 {term.capitalize()} → {explanation}")

        st.subheader("General Advice")

        if filtered_terms:
            for term in filtered_terms:
                advice_list = advice_dict.get(term, default_advice)

                st.write(f"🔹 {term.capitalize()}:")
                for adv in advice_list:
                    st.write(f"- {adv}")
