"""
Utilities for generating Redis database inspection reports,
including key statistics, memory usage, and data distribution.
"""

from library.service.redis.client import RedisClient
from library.service.redis.inspectors import RedisInspector

# Setting up redis client
redis = RedisClient()

# Setting up the inspector
inspector = RedisInspector(redis)

# Print the report
print(
    inspector.report(
        summary_by_type=True,
        details=True
    )
)
