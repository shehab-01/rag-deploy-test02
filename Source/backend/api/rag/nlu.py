from transformers import pipeline
from langdetect import detect
import torch

def get_language_specific_models(language):
    device = 0 if torch.cuda.is_available() else -1
    
    try:
        if language == 'ko':
            ner = pipeline("ner", model="kykim/bert-kor-base", device=device)
            classifier = pipeline("text-classification", model="seongju/klue-tc-bert-base-multilingual-cased", device=device)
        else:  # default to English
            ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", device=device)
            classifier = pipeline("text-classification", model="facebook/bart-large-mnli", device=device)
        print("NLU Model loaded successfully")
        return ner, classifier
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        raise

def process_query_nlu(query: str, question_language: str):
    # language = detect(query)
    language = question_language
    ner, classifier = get_language_specific_models(language)
    
    entities = ner(query)
    intent = classifier(query)[0]['label']
    
    expanded_query = query + " " + " ".join([entity['word'] for entity in entities])
    
    return {
        "original_query": query,
        "expanded_query": expanded_query,
        "entities": entities,
        "intent": intent,
        "language": language
    }