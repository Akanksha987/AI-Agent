"""Configuration management for HealthSense."""
import os
from typing import Optional
from core.exceptions import ConfigurationError


class Config:
    """Application configuration."""
    
    def __init__(self):
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.timeout: int = int(os.getenv("GEMINI_TIMEOUT", "30"))
        self.max_retries: int = int(os.getenv("GEMINI_MAX_RETRIES", "3"))
        self.rag_top_k: int = int(os.getenv("RAG_TOP_K", "5"))
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.enable_web: bool = os.getenv("ENABLE_WEB", "false").lower() == "true"
        self.web_port: int = int(os.getenv("WEB_PORT", "5000"))
        
        if not self.gemini_api_key:
            raise ConfigurationError(
                "GEMINI_API_KEY environment variable is not set. "
                "Please set it using: export GEMINI_API_KEY='your_key_here'"
            )
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        return cls()

