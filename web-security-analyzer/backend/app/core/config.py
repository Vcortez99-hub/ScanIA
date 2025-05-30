from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Config
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Web Security Analyzer"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # External APIs (opcionais por enquanto)
    VIRUSTOTAL_API_KEY: Optional[str] = os.getenv("VIRUSTOTAL_API_KEY")
    SHODAN_API_KEY: Optional[str] = os.getenv("SHODAN_API_KEY")
    
    # Scan Settings
    MAX_SCAN_TIMEOUT: int = 300  # 5 minutos
    MAX_CONCURRENT_SCANS: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()