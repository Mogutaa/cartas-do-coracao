import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI = os.getenv("MONGO_URI")
    OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
    PIX_KEY = os.getenv("PIX_KEY")
    BASE_URL = os.getenv("BASE_URL")
    
    @classmethod
    def validate(cls):
        if not all([cls.MONGO_URI, cls.OPENROUTER_KEY, cls.PIX_KEY]):
            raise ValueError("Missing environment variables")

settings = Settings()