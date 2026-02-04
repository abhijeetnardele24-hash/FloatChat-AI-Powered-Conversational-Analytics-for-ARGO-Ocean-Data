"""
Configuration management for FloatChat Ultra
Loads settings from environment variables and .env file
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # ============================================
    # Application Info
    # ============================================
    app_name: str = Field(default="FloatChat Ultra", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    app_environment: str = Field(default="development", env="APP_ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # ============================================
    # Database Configuration
    # ============================================
    database_url: str = Field(
        default="postgresql://floatchat_user:password@localhost:5432/floatchat",
        env="DATABASE_URL"
    )
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="floatchat", env="DB_NAME")
    db_user: str = Field(default="floatchat_user", env="DB_USER")
    db_password: str = Field(default="password", env="DB_PASSWORD")
    
    # ============================================
    # Redis Configuration
    # ============================================
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    
    # ============================================
    # Ollama LLM Configuration
    # ============================================
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="mistral:7b-instruct", env="OLLAMA_MODEL")
    ollama_temperature: float = Field(default=0.1, env="OLLAMA_TEMPERATURE")
    ollama_num_ctx: int = Field(default=8192, env="OLLAMA_NUM_CTX")
    
    # ============================================
    # ChromaDB Configuration
    # ============================================
    chroma_persist_directory: str = Field(default="./data/chromadb", env="CHROMA_PERSIST_DIRECTORY")
    chroma_collection_name: str = Field(default="argo_metadata", env="CHROMA_COLLECTION_NAME")
    
    # ============================================
    # Embedding Model Configuration
    # ============================================
    embedding_model: str = Field(
        default="sentence-transformers/all-mpnet-base-v2",
        env="EMBEDDING_MODEL"
    )
    embedding_dimension: int = Field(default=768, env="EMBEDDING_DIMENSION")
    
    # ============================================
    # Data Paths
    # ============================================
    data_raw_dir: str = Field(default="./data/raw", env="DATA_RAW_DIR")
    data_processed_dir: str = Field(default="./data/processed", env="DATA_PROCESSED_DIR")
    data_logs_dir: str = Field(default="./data/logs", env="DATA_LOGS_DIR")
    
    # ============================================
    # ARGO Data Sources
    # ============================================
    argo_gdac_ftp: str = Field(default="ftp.ifremer.fr", env="ARGO_GDAC_FTP")
    argo_gdac_path: str = Field(default="/ifremer/argo", env="ARGO_GDAC_PATH")
    argo_index_url: str = Field(
        default="https://data-argo.ifremer.fr/ar_index_global_prof.txt",
        env="ARGO_INDEX_URL"
    )
    
    # ============================================
    # API Configuration
    # ============================================
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_reload: bool = Field(default=True, env="API_RELOAD")
    api_workers: int = Field(default=4, env="API_WORKERS")
    
    # ============================================
    # Streamlit Configuration
    # ============================================
    streamlit_server_port: int = Field(default=8501, env="STREAMLIT_SERVER_PORT")
    streamlit_server_address: str = Field(default="0.0.0.0", env="STREAMLIT_SERVER_ADDRESS")
    
    # ============================================
    # Logging Configuration
    # ============================================
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(
        default="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        env="LOG_FORMAT"
    )
    
    # ============================================
    # Performance Settings
    # ============================================
    max_workers: int = Field(default=10, env="MAX_WORKERS")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")
    query_timeout: int = Field(default=30, env="QUERY_TIMEOUT")
    max_results: int = Field(default=10000, env="MAX_RESULTS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings


def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        settings.data_raw_dir,
        settings.data_processed_dir,
        settings.data_logs_dir,
        settings.chroma_persist_directory,
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


# Ensure directories exist on import
ensure_directories()
