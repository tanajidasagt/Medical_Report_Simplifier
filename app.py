from simplify import simplify_text
from ner import extract_terms

medical_dict = {
    "hypertension": "high blood pressure",
    "diabetes": "a condition where blood sugar levels are too high",
    "glucose": "a type of sugar in the blood"
}

# Take user input
text = input("Enter medical report:\n")

print("\n--- Original Report ---")
print(text)

print("\n--- Simplified Report ---")
simplified = simplify_text(text)
print(simplified)

print("\n--- Medical Term Explanations ---")
terms = extract_terms(text)

if not terms:
    print("No medical terms detected.")
else:
    for term, label in terms:
        explanation = medical_dict.get(term.lower(), "No simple explanation available")
        print(f"{term} → {explanation}")
