"""
Configuration settings
"""
import os
from dotenv import load_dotenv

load_dotenv(".env.local")
load_dotenv(".env")

SECRET_KEY = os.getenv('SECRET_KEY') or 'dev'

QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
if not QDRANT_API_KEY:
    raise ValueError("Missing Key in the environment: QDRANT_API_KEY")

QDRANT_ENDPOINT = os.getenv('QDRANT_ENDPOINT')
if not QDRANT_ENDPOINT:
    raise ValueError("Missing Endpoint in the environment: QDRANT_ENDPOINT")