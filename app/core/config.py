from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    chroma_persist_dir: str = "chroma_db"
    model_name: str = "gpt-4.1-mini"
    debug: bool = False
    run_ingest_on_startup: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()