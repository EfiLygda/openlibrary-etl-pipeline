"""
Configuration of Kafka via .env
"""

import os
from dotenv import load_dotenv

# Loading variables from .env
load_dotenv()

# Get Kafka variables
TOPIC = str(os.getenv('TOPIC'))
BOOTSTRAP = str(os.getenv('BOOTSTRAP'))
KAFKA_CONTAINER = str(os.getenv('KAFKA_CONTAINER'))
KAFKA_TOPICS = str(os.getenv('KAFKA_TOPICS'))
CONSUMER_GROUP_ID = str(os.getenv('CONSUMER_GROUP_ID'))
AUTO_OFFSET_RESET = str(os.getenv('AUTO_OFFSET_RESET'))
