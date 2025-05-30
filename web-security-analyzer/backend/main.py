from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.model import ner_pipeline  # ✅ Importa com "app.model"
import uvicorn


# Importa o pipeline do modelo NER
#from model import ner_pipeline#

# Criar aplicação FastAPI
app = FastAPI(
    title="Web Security Analyzer API",
    description="API para análise de segurança web automatizada com Hugging Face NER",
    version="1.0.0"
)

# Configurar CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model para o endpoint /analyze
class AnalyzeRequest(BaseModel):
    text: str  # Ajustado para texto genérico, não apenas URL

@app.get("/")
async def root():
    return {
        "message": "🔐 Web Security Analyzer API",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Web Security Analyzer"
    }

# Endpoint básico para testar scan
@app.post("/api/v1/scan/quick")
async def quick_scan(url: str):
    """Scan rápido para testar a API"""
    return {
        "url": url,
        "status": "completed",
        "results": {
            "security_score": 75,
            "vulnerabilities_found": 3,
            "recommendations": [
                "Adicionar cabeçalho HSTS",
                "Implementar CSP",
                "Atualizar certificado SSL"
            ]
        }
    }

# Novo endpoint /analyze usando o modelo de NER
@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    # Roda inferência do modelo no texto enviado
    result = ner_pipeline(request.text)
    return {"result": result}

# --- PARTE OPCIONAL ---
# Importe condicional para evitar erro caso o módulo não esteja no PYTHONPATH durante execução direta
try:
    from app.api.log_analysis import router as log_analysis_router
    app.include_router(log_analysis_router, prefix="/api/v1")
except ImportError as e:
    print(f"[ERROR] Não foi possível importar log_analysis: {e}")
# --- FIM DA PARTE OPCIONAL ---

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
