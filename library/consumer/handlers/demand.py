"""
Event handlers related to library demand.

Handles events representing user intent to access unavailable resources, such as:
* Reservation requests
"""

import os
import psycopg2

from config.paths import CONSUMER_SQL_DIR
from utilities import execute_query

from library.service.redis.keys import RedisKeys
from library.service.redis.service import RedisClient