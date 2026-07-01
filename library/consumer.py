"""

Run: python -m library.consumer.py
"""

import json

from kafka import KafkaConsumer

from utilities.database import execute_query, db_connection, DB_NAME

from library.kafka_config import TOPIC, BOOTSTRAP, CONSUMER_GROUP_ID, AUTO_OFFSET_RESET

# Establish database connection
connection = db_connection(database=DB_NAME)

# Setting up consumer of events
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset=AUTO_OFFSET_RESET,
    group_id=CONSUMER_GROUP_ID
)

# For each message/event in the topic
# the consumer fetches the event message
# and loads data in the database
for msg in consumer:

    # Save the event's message
    event = msg.value

    # Print basic event metadata
    print("EVENT RECEIVED:")
    print(event["event_type"], event["data"], event['timestamp'])

    # In case the event is 'LIBRARIAN_HIRED' then load the new data to
    # the 'librarians' table
    if event["event_type"] == 'LIBRARIAN_HIRED':

        # Setting up the loading query
        query = """
        INSERT INTO librarians (
            first_name,
            last_name,
            email,
            registered_at
        )
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(registered_at)s)
        RETURNING librarian_id;
        """

        # Execute the query
        total_librarians, _ = execute_query(
            connection=connection,
            query=query,
            params={
                'first_name': event["data"]['first_name'],
                'last_name': event["data"]['last_name'],
                'email': event["data"]['email'],
                'registered_at': event["timestamp"],
            }
        )
