import streamlit as st
from simplify import simplify_text
from simplify import simplify_text
from ner import extract_terms
from deep_translator import GoogleTranslator
from src.ocr_engine import extract_text_from_image


def translate_text(text, target_lang):
    return GoogleTranslator(
        source='auto',
        target=target_lang
    ).translate(text)


description_df = pd.read_csv("symptom_Description.csv")

precaution_df = pd.read_csv("symptom_precaution.csv")

medical_dict = dict(
    zip(
        description_df["Disease"].str.lower(),
        description_df["Description"]
    )
)

advice_dict = {}

for _, row in precaution_df.iterrows():

    disease = row["Disease"].lower()

precautions = [

    str(p).strip()

    for p in [
        row["Precaution_1"],
        row["Precaution_2"],
        row["Precaution_3"],
        row["Precaution_4"]
    ]

    if pd.notna(p)
]

advice_dict[disease] = precautions

default_advice = [
    "Maintain a healthy lifestyle",
    "Exercise regularly",
    "Eat a balanced diet",
    "Consult a doctor if needed"
]

st.set_page_config(
    page_title="Medical Report Simplifier"
)



# --- Page Config ---
st.set_page_config(page_title="Medical Report Simplifier")

# --- Custom Styling ---
st.markdown("""
<style>
body { background-color: #0e1117; }
h1 { font-size: 42px !important; font-weight: 700 !important; text-align: center; margin-bottom: 10px; }
.custom-label { font-size: 22px; font-weight: 500; margin-top: 20px; }
textarea { border-radius: 12px !important; padding: 15px !important; font-size: 16px !important; background-color: #1c1f26 !important; color: white !important; border: 1px solid #2c2f36 !important; }
.stButton > button { background: linear-gradient(135deg, #00c6ff, #0072ff); color: white; font-size: 16px; border-radius: 10px; padding: 10px 20px; border: none; transition: 0.3s ease; width: 100%; }
.stButton > button:hover { transform: scale(1.05); background: linear-gradient(135deg, #0072ff, #00c6ff); }
.result-box { background-color: #1c1f26; padding: 20px; border-radius: 12px; font-size: 18px; color: #00ff9f; border: 1px solid #2c2f36; margin-top: 10px; }
h2, h3 { margin-top: 25px; }
</style>
""", unsafe_allow_html=True)

st.title("🏥 Patient-Centric Medical Report Simplifier")

# --- Session State Logic ---
# This ensures that when we extract text from an image, it stays in the text box
if 'report_text' not in st.session_state:
    st.session_state['report_text'] = ""

# --- Input Section with Tabs ---
st.markdown("<p style='font-size:22px; font-weight:600;'>Enter Medical Report:</p>", unsafe_allow_html=True)

# We create two tabs: one for typing and one for uploading an image
tab1, tab2 = st.tabs(["💬 Manual Text", "📸 Upload Image"])

with tab1:
    # The value is linked to session_state so OCR results appear here automatically
    text = st.text_area("", value=st.session_state['report_text'], height=300, key="manual_input")

with tab2:
    uploaded_file = st.file_uploader("Upload a photo of the report", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", width=300)
        if st.button("Extract Text from Image"):
            with st.spinner("🔍 Reading report..."):
                extracted = extract_text_from_image(uploaded_file)
                st.session_state['report_text'] = extracted
                st.success("Text extracted! Now click 'Simplify Report' below.")
                st.rerun()

# --- Processing Logic ---
if st.button("Simplify Report"):
    # We use the text currently in the manual input box
    final_text = st.session_state.get('manual_input', "")

    if final_text.strip() == "":
        st.warning("Please enter your report or upload an image.")
    else:
        st.subheader("Simplified Report")
        with st.spinner("🤖 AI is simplifying..."):
            simplified = simplify_text(final_text)

        st.markdown(
            f"<div class='result-box'>{simplified}</div>",
            unsafe_allow_html=True
        )

        terms = extract_terms(final_text)
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
