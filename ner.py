MEDICAL_KEYWORDS = [
    "diabetes",
    "hypertension",
    "glucose",
    "blood pressure",
    "cholesterol",
    "fever",
    "infection",
    "cancer",
    "asthma",
    "anemia",
    "obesity"
]

def extract_terms(text):
    text = text.lower()
    found_terms = []

    for keyword in MEDICAL_KEYWORDS:
        if keyword in text:
            found_terms.append(keyword)

    return list(set(found_terms))