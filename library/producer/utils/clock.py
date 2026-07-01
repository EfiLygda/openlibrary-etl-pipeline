"""
Clock used for producing event timestamps that simulate time passing in different speeds
"""

import time
from datetime import datetime, timedelta
from library.producer.config import START_DATE, END_DATE

SIM_SPEED = 1 # 365 * 24 * 60 * 60  # 1 year per second

class SimClock:
    """
    Class the simulates a clock that spans a year in a second
    by passing the starting date

    :param start: datetime.datetime
    """

    def __init__(self, start: datetime = START_DATE, end: datetime = END_DATE):

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

        if sim_time < self.end_sim:
            return sim_time
        else:
            raise ValueError('Simulation is done')
