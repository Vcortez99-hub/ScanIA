from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# Carregar o modelo e o tokenizador
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

# Criar a pipeline para NER
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

def extract_iocs(log_text):
    """
    Extrai Indicators of Compromise (IOC) de um texto de log usando NER.
    
    Args:
        log_text (str): Texto do log a ser analisado.
    
    Returns:
        dict: Dicionário contendo IOC categorizados.
    """
    # Processar o texto com a pipeline NER
    ner_results = nlp(log_text)
    
    # Organizar os resultados por categoria
    iocs = {
        "IPs": [],
        "Domínios": [],
        "Arquivos": [],
        "Outros": []
    }
    
    for entity in ner_results:
        if "IP" in entity["entity_group"]:
            iocs["IPs"].append(entity["word"])
        elif "URL" in entity["entity_group"] or "DOMAIN" in entity["entity_group"]:
            iocs["Domínios"].append(entity["word"])
        elif "FILE" in entity["entity_group"]:
            iocs["Arquivos"].append(entity["word"])
        else:
            iocs["Outros"].append(entity["word"])
    
    return iocs