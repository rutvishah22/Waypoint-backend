"""
Configuration settings for the application.

This file loads environment variables and makes them
available throughout the app.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Application settings.
    
    Attributes get loaded from environment variables.
    """
    
    # MongoDB settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "waypoint_db")
    
    # Gemini API settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Product Hunt API
    PRODUCTHUNT_API_TOKEN: str = os.getenv("PRODUCTHUNT_API_TOKEN", "")

    # TAVILY API
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    #SerpAPI api
    SERPAPI_KEY: str = os.getenv("SERPAPI_KEY", "")
    
    # App settings
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # API settings
    API_TITLE: str = "Waypoint API"
    API_VERSION: str = "1.0.0"


# Create settings instance
settings = Settings()