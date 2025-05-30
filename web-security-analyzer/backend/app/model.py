from transformers import pipeline

# Carrega o pipeline de Named Entity Recognition com o modelo
ner_pipeline = pipeline("ner", model="dslim/bert-large-NER", aggregation_strategy="simple")
