"""
Directory paths for SQL statements executed by system event handlers.
"""

import os
from config.paths import SYSTEM_CONSUMER_SQL_DIR

PEOPLE_SQL_DIR = os.path.join(SYSTEM_CONSUMER_SQL_DIR, 'people')
INVENTORY_SQL_DIR = os.path.join(SYSTEM_CONSUMER_SQL_DIR, 'inventory')
CIRCULATION_SQL_DIR = os.path.join(SYSTEM_CONSUMER_SQL_DIR, 'circulation')
DEMAND_SQL_DIR = os.path.join(SYSTEM_CONSUMER_SQL_DIR, 'demand')
