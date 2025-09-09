"""Configuration management for the localization tool."""

import os
from dataclasses import dataclass
from typing import List, Optional

try:
    from dotenv import load_dotenv
except ImportError:

    def load_dotenv(*args, **kwargs):
        """Fallback if python-dotenv is not installed."""
        pass


@dataclass
class Config:
    """Configuration settings for the localization tool."""

    # Google Sheets API Configuration
    google_credentials_path: Optional[str] = None
    google_sheet_id: Optional[str] = None

    # Translation Settings
    default_source_language: str = "en"
    default_target_languages: List[str] = None

    # Translation Service API Keys
    google_translate_api_key: Optional[str] = None
    deepl_api_key: Optional[str] = None
    azure_translator_key: Optional[str] = None
    azure_translator_region: Optional[str] = None

    # Output Configuration
    output_format: str = "json"
    output_directory: str = "./locales"

    # Logging
    log_level: str = "INFO"
    log_file: str = "localization.log"

    # Rate Limiting
    translation_delay_seconds: float = 0.1
    max_retries: int = 3

    # Cache Settings
    enable_cache: bool = True
    cache_directory: str = ".cache"

    def __post_init__(self):
        """Initialize default values after dataclass creation."""
        if self.default_target_languages is None:
            self.default_target_languages = ["es", "fr", "de", "it"]


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from environment variables and .env file.

    Args:
        config_path: Optional path to a specific .env file

    Returns:
        Config object with loaded settings
    """
    if config_path:
        load_dotenv(config_path)
    else:
        load_dotenv()

    # Parse target languages from comma-separated string
    target_langs_str = os.getenv("DEFAULT_TARGET_LANGUAGES", "es,fr,de,it")
    target_languages = [lang.strip() for lang in target_langs_str.split(",")]

    config = Config(
        google_credentials_path=os.getenv("GOOGLE_CREDENTIALS_PATH"),
        google_sheet_id=os.getenv("GOOGLE_SHEET_ID"),
        default_source_language=os.getenv("DEFAULT_SOURCE_LANGUAGE", "en"),
        default_target_languages=target_languages,
        google_translate_api_key=os.getenv("GOOGLE_TRANSLATE_API_KEY"),
        deepl_api_key=os.getenv("DEEPL_API_KEY"),
        azure_translator_key=os.getenv("AZURE_TRANSLATOR_KEY"),
        azure_translator_region=os.getenv("AZURE_TRANSLATOR_REGION"),
        output_format=os.getenv("OUTPUT_FORMAT", "json"),
        output_directory=os.getenv("OUTPUT_DIRECTORY", "./locales"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=os.getenv("LOG_FILE", "localization.log"),
        translation_delay_seconds=float(os.getenv("TRANSLATION_DELAY_SECONDS", "0.1")),
        max_retries=int(os.getenv("MAX_RETRIES", "3")),
        enable_cache=os.getenv("ENABLE_CACHE", "true").lower() == "true",
        cache_directory=os.getenv("CACHE_DIRECTORY", ".cache"),
    )

    return config
