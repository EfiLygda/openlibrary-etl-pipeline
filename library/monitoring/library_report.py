"""
Utilities for generating library state reports, including users,
copies, loans, and reservation statistics.
"""

from library.service.redis.client import RedisClient
from library.service.redis.inspectors import LibraryInspector

# Setting up redis client
redis = RedisClient()

# Setting up the inspector
inspector = LibraryInspector(redis)

# Print the report
print(
    inspector.report(
        details=True
    )
)