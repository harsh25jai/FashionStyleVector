# app/core/config.py
import os
import sys
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")

# Validate required configuration at startup
missing_vars = []
if not OPENAI_API_KEY:
    missing_vars.append("OPENAI_API_KEY")
if not QDRANT_URL:
    missing_vars.append("QDRANT_URL")
if not COLLECTION_NAME:
    missing_vars.append("COLLECTION_NAME")

if missing_vars:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(missing_vars)}. "
        "Please set these in your .env file or environment."
    )