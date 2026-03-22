import spacy

nlp = spacy.load("en_core_sci_sm")

MEDICAL_KEYWORDS = [
    "diabetes", "hypertension", "glucose",
    "blood pressure", "cholesterol", "fever",
    "infection", "cancer"
]

def extract_terms(text):
    doc = nlp(text)
    
    terms = []

    for ent in doc.ents:
        terms.append(ent.text.lower())

    for word in text.lower().split():
        if word in MEDICAL_KEYWORDS:
            terms.append(word)

    stop_words = ["patient", "suffering", "problem"]
    
    cleaned_terms = [
        term for term in terms 
        if term not in stop_words and len(term) > 2
    ]

    return list(set(cleaned_terms))
