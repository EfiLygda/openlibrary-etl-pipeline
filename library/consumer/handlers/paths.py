"""
Directory paths for SQL statements executed by consumer event handlers.
"""

import os
from config.paths import CONSUMER_SQL_DIR

PEOPLE_SQL_DIR = os.path.join(CONSUMER_SQL_DIR, 'people')
INVENTORY_SQL_DIR = os.path.join(CONSUMER_SQL_DIR, 'inventory')
CIRCULATION_SQL_DIR = os.path.join(CONSUMER_SQL_DIR, 'circulation')
DEMAND_SQL_DIR = os.path.join(CONSUMER_SQL_DIR, 'demand')
