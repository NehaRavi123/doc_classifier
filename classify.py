from transformers import pipeline

# Load a zero-shot classification model from HuggingFace Hub (free and local-capable)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

CATEGORIES = [
    "Stock Purchase Agreement",
    "Certificate of Incorporation",
    "Investors' Rights Agreement"
]

def classify_text(text):
    result = classifier(text, CATEGORIES)
    return result['labels'][0] 