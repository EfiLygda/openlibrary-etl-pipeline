"""
Runs the library simulation pipeline.

Starts the system consumer followed by the events producer, keeping the
simulation running until interrupted by the user.
"""

import sys
import subprocess
from utilities.logger import set_logger

logger = set_logger('SIMULATE_EVENTS')

def run(display_events: bool = False):
    """
    Runs the library simulation.

    Starts the library system consumer before launching the events producer to
    ensure events are consumed as they are produced. The simulation continues
    until interrupted.

    :display_events: bool, whether to display the events or not

    :return: None
    """

    logger.info('STAGE_START')

    # Initializing the consumers and producer
    library_system_consumer = None
    producer = None

    try:
        # Start library's system consumer subprocess
        system_consumer_command = [
            sys.executable,
            "-m",
            "library.consumers.system.consumer"
        ]

        if display_events:
            system_consumer_command.append("--display-events")

        # Start library's system consumer subprocess
        library_system_consumer = subprocess.Popen(system_consumer_command)

        # Start library's system producer subprocess
        producer_command = [
            sys.executable,
            "-m",
            "library.producer.producer"
        ]

        if display_events:
            producer_command.append("--display-events")

        # Start library's events producer subprocess
        producer = subprocess.Popen(producer_command)

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
