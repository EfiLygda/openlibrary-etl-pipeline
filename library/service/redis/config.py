"""
Configuration of Redis
"""
import os
from dotenv import load_dotenv

# Loading variables from .env
load_dotenv()

# Redis configuration
REDIS_HOST = str(os.getenv('REDIS_HOST'))
REDIS_PORT = int(os.getenv('REDIS_PORT'))
