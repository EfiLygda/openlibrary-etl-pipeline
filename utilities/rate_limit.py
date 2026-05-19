from time import sleep
from random import uniform

def wait(seconds: float = 3) -> None:
    """
    Function for politely waiting more than 3 seconds for each request
    :param seconds: float, the minimum seconds to wait
    :return: None
    """
    sleep(seconds + uniform(0, 1.5))