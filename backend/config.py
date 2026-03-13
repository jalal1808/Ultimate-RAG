from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache

class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent
DATA_DIR: Path = Path("data")
UPLOAD_DIR: Path = DATA_DIR / "uploads"
CHROMA_DIR: Path = DATA_DIR / "chroma"
SUMMARY_DIR: Path = DATA_DIR / "summaries"

    EMBEDDING_PROVIDER: str = "local"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    LLM_PROVIDER: str = "google-genai"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    TOP_K_RETRIEVAL: int = 20
    TOP_K_RERANK: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
@lru_cache()
def get_settings() -> Settings:
    return Settings()

