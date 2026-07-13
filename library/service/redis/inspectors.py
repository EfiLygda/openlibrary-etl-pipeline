"""

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
            "registered_users": redis_client.get_set_size(RedisKeys.Sets.USER_IDS),
            "hired_librarians": redis_client.get_set_size(RedisKeys.Sets.LIBRARIAN_IDS),

            # Copies
            "available_copies": redis_client.get_set_size(RedisKeys.Sets.AVAILABLE_COPIES_IDS),
            "unavailable_copies": redis_client.get_set_size(RedisKeys.Sets.UNAVAILABLE_COPIES_IDS),

            # Loans
            "active_loans": redis_client.get_set_size(RedisKeys.Sets.ACTIVE_LOANS_IDS),
            "returned_loans": redis_client.get_set_size(RedisKeys.Sets.RETURNED_LOANS_IDS),

            # Reservations
            "active_reservations": redis_client.get_set_size(RedisKeys.Sets.ACTIVE_RESERVATIONS_IDS),
            "fulfilled_reservations": redis_client.get_set_size(RedisKeys.Sets.FULFILLED_RESERVATIONS_IDS),
            "cancelled_reservations": redis_client.get_set_size(RedisKeys.Sets.CANCELLED_RESERVATIONS_IDS),
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

        library_stats = self._stats()

        summary = self._overview(stats=library_stats)

        if details:
            summary += 2*'\n' + self._details(stats=library_stats)


        return f"""
============= Library Summary =============

Generated: {timestamp}

{summary}

===========================================
"""

