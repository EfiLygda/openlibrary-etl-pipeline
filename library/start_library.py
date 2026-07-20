"""
Runs the library simulation pipeline.

Starts the system consumer followed by the events producer, keeping the
simulation running until interrupted by the user.
"""

import sys
import subprocess
from utilities.rate_limit import wait
from utilities.logging import set_logger

logger = set_logger('LIBRARY_SIMULATION')

def run():
    """
    Runs the library simulation.

    Starts the library system consumer before launching the events producer to
    ensure events are consumed as they are produced. The simulation continues
    until interrupted.

    :return: None
    """

    logger.info('STAGE_START')

    # Initializing the consumers and producer
    library_system_consumer = None
    producer = None

    try:
        # Start library's system consumer subprocess
        library_system_consumer = subprocess.Popen([
            sys.executable,
            "-m",
            "library.consumers.system.consumer"
        ])

        # Wait more than 10 seconds
        wait(10)

        # Start library's events producer subprocess
        producer = subprocess.Popen([
            sys.executable,
            "-m",
            "library.producer.producer"
        ])

        # Producer's subprocess alive in order
        # to use KeyboardInterrupt in console
        producer.wait()

    except KeyboardInterrupt:

        # Terminate both producer and consumer
        if producer:
            producer.terminate()
            producer.wait()

        if library_system_consumer:
            library_system_consumer.terminate()
            library_system_consumer.wait()

        logger.info('PIPELINE_STOPPED')

    logger.info('STAGE_COMPLETE')
