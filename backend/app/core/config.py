from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Agent Native AI Coding IDE"
    llm_model: str = "gpt-4.1-mini"
    chroma_path: str = "./.chroma"
    workspace_path: str = "./workspace"


settings = Settings()
