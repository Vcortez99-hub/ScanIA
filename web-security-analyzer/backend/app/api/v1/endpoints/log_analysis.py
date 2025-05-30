from fastapi import APIRouter, HTTPException
from app.services.ner_service import extract_iocs

router = APIRouter()

@router.post("/analyze-log/")
async def analyze_log(log_text: str):
    """
    Analisa um log de segurança e extrai Indicators of Compromise (IOC).
    
    Args:
        log_text (str): Texto do log a ser analisado.
    
    Returns:
        dict: Dicionário contendo IOC categorizados.
    """
    if not log_text:
        raise HTTPException(status_code=400, detail="Log text is required.")
    
    try:
        # Chama o serviço de NER para extrair IOC
        iocs = extract_iocs(log_text)
        return {"ioc_results": iocs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing log: {str(e)}")