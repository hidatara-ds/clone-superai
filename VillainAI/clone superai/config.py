import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Model configurations using OpenRouter
AI_MODELS = {
    "auto": {
        "name": "Auto (Default ke Mistral)",
        "description": "Pilih model secara otomatis (saat ini Mistral 7B).",
        # This will be handled in app.py to default to a specific OpenRouter model
    },
    "openrouter/mistralai/mistral-7b-instruct": {
        "name": "Mistral 7B Instruct",
        "description": "Model serbaguna dari MistralAI via OpenRouter.",
        "api_provider": "openrouter",
        "openrouter_model_id": "mistralai/mistral-7b-instruct",
        "pricing_tier": "various" # Pricing depends on OpenRouter's rates
    },
    "openrouter/meta-llama/llama-3-8b-instruct": {
        "name": "Llama 3 8B Instruct",
        "description": "Model Llama 3 8B dari Meta via OpenRouter.",
        "api_provider": "openrouter",
        "openrouter_model_id": "meta-llama/llama-3-8b-instruct",
        "pricing_tier": "various"
    },
    "openrouter/openchat/openchat-3.5": {
        "name": "OpenChat 3.5",
        "description": "Model OpenChat 3.5 via OpenRouter.",
        "api_provider": "openrouter",
        "openrouter_model_id": "openchat/openchat-3.5",
        "pricing_tier": "various"
    },
    "openrouter/nousresearch/nous-capybara-7b": {
        "name": "Nous Capybara 7B",
        "description": "Model Capybara 7B dari Nous Research via OpenRouter.",
        "api_provider": "openrouter",
        "openrouter_model_id": "nousresearch/nous-capybara-7b",
        "pricing_tier": "various"
    }
    # Tambahkan model OpenRouter gratis lainnya di sini jika diinginkan
}

def get_openrouter_api_key() -> str | None:
    """Gets the OpenRouter API key from environment variables."""
    return OPENROUTER_API_KEY

# --- Add other configurations if needed ---
# Example: Redis config (if you plan to use it later)
# REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
# REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Example: Database config
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///mydatabase.db") # Example using SQLite