import streamlit as st
import pandas as pd
from simplify import simplify_text
from ner import extract_terms
from deep_translator import GoogleTranslator
from src.ocr_engine import extract_text_from_image


# =========================
# TRANSLATION FUNCTION
# =========================

def translate_text(text, target_lang):

    return GoogleTranslator(
        source='auto',
        target=target_lang
    ).translate(text)


# =========================
# LOAD DATASETS
# =========================

description_df = pd.read_csv(
    "symptom_Description.csv"
)

precaution_df = pd.read_csv(
    "symptom_precaution.csv"
)


# =========================
# MEDICAL DESCRIPTION DICTIONARY
# =========================

medical_dict = dict(

    zip(

        description_df["Disease"]
        .str.lower()
        .str.strip(),

        description_df["Description"]
    )
)


# =========================
# PRECAUTION DICTIONARY
# =========================

advice_dict = {}

for _, row in precaution_df.iterrows():

    disease = row["Disease"].lower().strip()

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


# =========================
# DEFAULT ADVICE
# =========================

default_advice = [

    "Maintain a healthy lifestyle",
    "Exercise regularly",
    "Eat a balanced diet",
    "Consult a doctor if needed"

]


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Medical Report Simplifier"
)


# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

body {
    background-color: #0e1117;
}

h1 {
    font-size: 42px !important;
    font-weight: 700 !important;
    text-align: center;
    margin-bottom: 10px;
}

.custom-label {
    font-size: 22px;
    font-weight: 500;
    margin-top: 20px;
}

textarea {
    border-radius: 12px !important;
    padding: 15px !important;
    font-size: 16px !important;
    background-color: #1c1f26 !important;
    color: white !important;
    border: 1px solid #2c2f36 !important;
}

.stButton > button {
    background: linear-gradient(
        135deg,
        #00c6ff,
        #0072ff
    );

    color: white;
    font-size: 16px;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    transition: 0.3s ease;
    width: 100%;
}

.stButton > button:hover {

    transform: scale(1.05);

    background: linear-gradient(
        135deg,
        #0072ff,
        #00c6ff
    );
}

.result-box {

    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    font-size: 18px;
    color: #00ff9f;
    border: 1px solid #2c2f36;
    margin-top: 10px;
}

h2, h3 {
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# TITLE
# =========================

st.title(
    "🏥 Patient-Centric Medical Report Simplifier"
)


# =========================
# SESSION STATE
# =========================

if 'report_text' not in st.session_state:

    st.session_state['report_text'] = ""


# =========================
# INPUT TITLE
# =========================

st.markdown(

    "<p style='font-size:22px; font-weight:600;'>Enter Medical Report:</p>",

    unsafe_allow_html=True
)


# =========================
# TABS
# =========================

tab1, tab2 = st.tabs(

    [
        "💬 Manual Text",
        "📸 Upload Image"
    ]
)


# =========================
# MANUAL TEXT TAB
# =========================

with tab1:

    text = st.text_area(

        "",

        value=st.session_state['report_text'],

        height=300,

        key="manual_input"
    )


# =========================
# IMAGE OCR TAB
# =========================

with tab2:

    uploaded_file = st.file_uploader(

        "Upload a photo of the report",

        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        st.image(

            uploaded_file,

            caption="Uploaded Image",

            width=300
        )

        if st.button("Extract Text from Image"):

            with st.spinner("🔍 Reading report..."):

                extracted = extract_text_from_image(
                    uploaded_file
                )

                st.session_state['report_text'] = extracted

                st.success(
                    "Text extracted successfully!"
                )

                st.rerun()


# =========================
# LANGUAGE DROPDOWN
# =========================

lang_map = {

    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te"
}

selected_lang = st.selectbox(

    "🌐 Select Language",

    list(lang_map.keys())
)

language = lang_map[selected_lang]


# =========================
# MAIN BUTTON
# =========================

if st.button("Simplify Report"):

    final_text = st.session_state.get(
        'manual_input',
        ""
    )

    if final_text.strip() == "":

        st.warning(
            "Please enter your report or upload an image."
        )

    else:

        # =========================
        # SIMPLIFICATION
        # =========================

        st.subheader("Simplified Report")

        with st.spinner("🤖 AI is simplifying..."):

            simplified = simplify_text(final_text)

        if language != "en":

            simplified = translate_text(
                simplified,
                language
            )

        st.markdown(

            f"<div class='result-box'>{simplified}</div>",

            unsafe_allow_html=True
        )


        # =========================
        # TERM EXTRACTION
        # =========================

        terms = extract_terms(final_text)

        filtered_terms = []

        for term in terms:

            term_lower = term.lower()

            for disease in medical_dict.keys():

                if disease in term_lower:

                    filtered_terms.append(disease)

        filtered_terms = list(
            set(filtered_terms)
        )


        # =========================
        # EXPLANATIONS
        # =========================

        st.subheader(
            "Medical Term Explanations"
        )

        if not filtered_terms:

            st.write(
                "No medical terms detected."
            )

        else:

            for term in filtered_terms:

                explanation = medical_dict.get(

                    term,

                    "No explanation available."
                )

                if language != "en":

                    explanation = translate_text(
                        explanation,
                        language
                    )

                st.write(

                    f"🔹 {term.capitalize()} → {explanation}"
                )


        # =========================
        # ADVICE
        # =========================

        st.subheader("General Advice")

        if filtered_terms:

            for term in filtered_terms:

                advice_list = advice_dict.get(

                    term,

                    default_advice
                )

                st.write(
                    f"🔹 {term.capitalize()}:"
                )

                for adv in advice_list:

                    if language != "en":

                        adv = translate_text(
                            adv,
                            language
                        )

                    st.write(f"- {adv}")
