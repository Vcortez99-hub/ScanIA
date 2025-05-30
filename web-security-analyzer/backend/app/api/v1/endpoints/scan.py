from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional
from app.services.scanner.headers_scanner import scan_website_security

router = APIRouter()

class ScanRequest(BaseModel):
    url: str
    scan_type: Optional[str] = "basic"

class ScanResponse(BaseModel):
    success: bool
    data: dict
    message: str

@router.post("/scan", response_model=ScanResponse)
async def perform_security_scan(request: ScanRequest):
    """Endpoint principal para realizar scan de segurança"""
    try:
        # Validar URL básica
        url = request.url.strip()
        if not url:
            raise HTTPException(status_code=400, detail="URL é obrigatória")
        
        # Realizar scan
        results = scan_website_security(url)
        
        return ScanResponse(
            success=True,
            data=results,
            message="Scan realizado com sucesso"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "Erro interno do servidor",
                "details": str(e)
            }
        )

@router.get("/scan/example")
async def get_scan_example():
    """Retorna exemplo de resultado de scan"""
    return {
        "example_result": {
            "url": "https://example.com",
            "security_score": 85,
            "headers_found": 4,
            "vulnerabilities": 2,
            "recommendations": [
                "Implementar HSTS",
                "Adicionar CSP header"
            ]
        }
    }