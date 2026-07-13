# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    IBM_CLOUD_API_KEY: str
    WATSONX_SPACE_ID: str
    WATSONX_URL: str = "https://au-syd.ml.cloud.ibm.com"
    CLOUDANT_URL: str
    CLOUDANT_API_KEY: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()