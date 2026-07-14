"""
Library inspection utilities for generating reports about library and Redis state
"""

from library.service.redis.keys import RedisKeys
from library.service.redis.client import RedisClient

from library.producer.producer_config import CLOCK

class Inspector:

    def __init__(self, client: RedisClient):
        """
        Initialize an inspector

        :param client: RedisClient, Redis client used for retrieving library data
        """
        self.client = client
        self.number_format = '>10,'

    def format_memory(
            self,
            bytes: int,
            digits: int,
            decimals: int,
            right_justified: bool = True
    ) -> str:
        """
        Format a memory size in bytes as a human-readable megabyte string

        :param bytes: int, memory size in bytes
        :param digits: int, total field width used for formatting
        :param decimals: int, number of decimal places to display
        :param right_justified: bool, whether the formatted value should be right justified
        :return: str, formatted memory size in megabytes
        """

        # Setting up the alignment
        if right_justified:
            alignment = '>'
        else:
            alignment = '<'

        return f'{bytes / (1024 * 1024):{alignment}{digits}.{decimals}f} MB'

    def format_percent(self, percent: float) -> str:
        """
        Format a decimal ratio as a human-readable percentage.

        Values below 0.1% are represented as '<0.1%' to avoid displaying
        insignificant rounded values as 0.00%.

        :param percent: float, percentage value represented as a ratio
                        (for example, 0.534 means 53.4%)
        :return: str, formatted percentage string
        """

        if percent*100 < 0.1:
            return '<0.1%'

        return f'{percent*100:.2f}%'

class LibraryInspector(Inspector):

    def _stats(self) -> dict:
        """
        Retrieve current library statistics from Redis

        :return: dict, dictionary containing current library state values
        """

        # The current redit client used
        redis_client = self.client

        return {
            # People
            "registered_users": redis_client.sets.get_size(RedisKeys.Sets.USER_IDS),
            "hired_librarians": redis_client.sets.get_size(RedisKeys.Sets.LIBRARIAN_IDS),

            # Copies
            "available_copies": redis_client.sets.get_size(RedisKeys.Sets.AVAILABLE_COPIES_IDS),
            "unavailable_copies": redis_client.sets.get_size(RedisKeys.Sets.UNAVAILABLE_COPIES_IDS),

            # Loans
            "active_loans": redis_client.sets.get_size(RedisKeys.Sets.ACTIVE_LOANS_IDS),
            "returned_loans": redis_client.sets.get_size(RedisKeys.Sets.RETURNED_LOANS_IDS),

            # Reservations
            "active_reservations": redis_client.sets.get_size(RedisKeys.Sets.ACTIVE_RESERVATIONS_IDS),
            "fulfilled_reservations": redis_client.sets.get_size(RedisKeys.Sets.FULFILLED_RESERVATIONS_IDS),
            "cancelled_reservations": redis_client.sets.get_size(RedisKeys.Sets.CANCELLED_RESERVATIONS_IDS),
        }

    def _overview(self, stats: dict) -> str:
        """
        Generate a short overview of the current library state

        :param stats: dict, library statistics retrieved from Redis
        :return: str, formatted library overview
        """

        # Use the predetermined number format
        value_format = self.number_format

        return f"""
Overview
--------
Active Users:           {stats["registered_users"]:{value_format}}
Available Copies:       {stats["available_copies"]:{value_format}}
Active Loans:           {stats["active_loans"]:{value_format}}
Active Reservations:    {stats["active_reservations"]:{value_format}}
""".strip()

    def _details(self, stats: dict) -> str:
        """
        Generate a detailed report of the current library state

        :param stats: dict, library statistics retrieved from Redis
        :return: str, formatted detailed library report
        """

        # Use the predetermined number format
        value_format = self.number_format

        return f"""
Details        
-------
Users
-----
Registered Users:        {stats["registered_users"]:{value_format}}
Librarians:              {stats["hired_librarians"]:{value_format}}

Copies
------
Available:               {stats["available_copies"]:{value_format}}
Unavailable:             {stats["unavailable_copies"]:{value_format}}
Total Copies:            {stats["available_copies"] + stats["unavailable_copies"]:{value_format}}

Loans
-----
Active Loans:            {stats["active_loans"]:{value_format}}
Returned Loans:          {stats["returned_loans"]:{value_format}}
Total Loans:             {stats["active_loans"] + stats["returned_loans"]:{value_format}}

Reservations
------------
Active Reservations:     {stats["active_reservations"]:{value_format}}
Fulfilled Reservations:  {stats["fulfilled_reservations"]:{value_format}}
Cancelled Reservations:  {stats["cancelled_reservations"]:{value_format}}
""".strip()

    def report(
            self,
            details: bool = True
    ) -> str:
        """
        Generate a formatted library report

        :param details: bool, whether to include detailed library statistics
        :return: str, formatted library report containing current library state
        """

        # Timestamp of report
        timestamp = CLOCK.now()

        # Calculate library's statistics
        library_stats = self._stats()

        # Format the overview
        summary = self._overview(stats=library_stats)

        # If details are to be added then add them to the summary
        # after the overview
        if details:
            summary += 2*'\n' + self._details(stats=library_stats)

        # Return formatted result
        return f"""
============= Library Summary =============

Generated: {timestamp}

{summary}

===========================================
"""


class RedisInspector(Inspector):

    def _stats(self) -> dict:
        """
        Retrieve Redis database statistics

        :return: dict, Redis statistics including key counts and memory usage
        """

        # Setting up the redis client
        redis_client = self.client

        # Setting up the stats used
        stats = {
            "total_keys": 0,
            "total_memory": 0,
            "keys": []
        }

        # For each redis key finds its stats
        for key in redis_client.inspection.get_all_keys():

            # Find the redis key type and its memory usage
            key_type = redis_client.inspection.get_type(key).upper()
            memory = redis_client.inspection.get_memory_usage(key) or 0

            # Add to the keys counters
            stats["total_keys"] += 1

            # Add to total memory usage
            stats["total_memory"] += memory

            if key_type == 'SET':
                items = redis_client.sets.get_size(key)
            elif key_type == 'HASH':
                items = redis_client.hashes.get_length(key)
            elif key_type == 'LIST':
                items = redis_client.queues.get_length(key)
            elif key_type == 'STRING':
                items = redis_client.strings.get_length(key)
            else:
                items = '-'

            # Add the kye, its type and memory usage to the list
            stats["keys"].append(
                {
                    "key": key,
                    "type": key_type,
                    "memory": memory,
                    'items': items,
                }
            )

        # Sort redis keys' metadata by descenting memory usage
        stats["keys"] = sorted(
            stats["keys"],
            key=lambda d: d['memory'],
            reverse=True
        )

        # Calculate total memory percent used by each redis key
        for key in stats['keys']:
            key['memory_percent'] = key['memory'] / stats['total_memory']

        return stats

    def _overview(self, stats: dict) -> str:
        """
        Generate a short overview of Redis database statistics

        :param stats: dict, Redis statistics retrieved from the database
        :return: str, formatted Redis overview
        """

        return f"""
Database
--------
Total Keys:     {stats["total_keys"]}
Total Memory:   {self.format_memory(stats["total_memory"], 5, 2, right_justified=False)}
"""

    def _details(self, stats: dict) -> str:
        """
        Generate a detailed summary of Redis keys and their memory usage

        :param stats: dict, Redis statistics retrieved from the database
        :return: str, formatted Redis key summary
        """

        # List that will contain all the redis keys lines for the details
        lines = []

        # For each redis key add a formatted line to the lines list
        for item in stats["keys"]:
            lines.append(
                f"{item['key']:<40}"
                f"{item['type']:<10}"
                f"{self.format_memory(item['memory'], 7, 2):>10}"
                f"{self.format_percent(item['memory_percent']):>15}"
                f"{item['items']:>15,}"
            )

        return f"""
Details
-------
KEY                                     TYPE         MEMORY         MEMORY %        ITEMS
------------------------------------------------------------------------------------------
{"\n".join(lines)}
------------------------------------------------------------------------------------------
""".strip()


    def report(
            self,
            details: bool = True
    ) -> str:
        """
        Generate a formatted Redis database report

        :param details: bool, whether to include per-key Redis statistics
        :return: str, formatted Redis report containing current database statistics
        """

        # Timestamp of report
        timestamp = CLOCK.now()

        # Calculate redis' statistics
        redis_stats = self._stats()

        # Add the overview to the redis report
        summary = self._overview(stats=redis_stats)

        # If details are chosen to be displayed then add them
        # to the report
        if details:
            summary += 2*'\n' + self._details(stats=redis_stats)

        return f"""
===================================== Redis Summary ======================================

Generated: {timestamp}

{summary}

==========================================================================================
"""
