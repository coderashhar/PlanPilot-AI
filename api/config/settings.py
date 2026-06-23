from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = ""
    GOOGLE_PLACES_API_KEY: str = ""
    TAVILY_API_KEY: str = ""
    OPENWEATHERMAP_API_KEY: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
