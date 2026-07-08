"""
Clock used for producing event timestamps that simulate time passing in different speeds
"""

import time
from datetime import datetime, timedelta

SIM_SPEED = 24 * 60 * 60 # 365 * 24 * 60 * 60  # 1 year per second

class SimClock:
    """
    Class the simulates a clock that spans a year in a second
    by passing the starting date

    :param start: datetime.datetime
    """

    def __init__(self, start: datetime, end: datetime):

        self.start_real = time.time()

        self.start_sim = start
        self.end_sim = end

        self.speed = SIM_SPEED

    def now(self) -> datetime:
        """
        Function for fetching the simulated time's current timestamp
        """
        elapsed_real = time.time() - self.start_real
        elapsed_sim = elapsed_real * self.speed

        sim_time = self.start_sim + timedelta(seconds=elapsed_sim)

        return sim_time
