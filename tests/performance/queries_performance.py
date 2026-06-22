"""
Script for extracting execution times from queries
"""

import os
import re
import pandas as pd
from api.repository.base import execute_query
from utilities.database import DB_NAME, db_connection

# Whether non-primary key indexes exist in the queries or not
INDEX = True

# SQL queries' parameters
edition_key = 'OL37490633M'
search_query = 'pride prejudice'
limit=20
offset=0

# Maximum repetitions for querying database
max_reps = 100

# Performance results directory
results_dir = os.path.join('./', 'results')
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Execution time pattern
execution_time_pattern = r'([\d.]+)\s*ms'

# Query modules and queries that have non-primary key indexes
query_modules = {
    'editions': [
        'get_edition.sql',
        'get_contributors.sql',
        'get_details.sql',
        'get_publishing.sql',
    ],
    'search': [
        'search_works.sql',
    ]
}

# Final data list, that will contain tuples of rows
execution_times_data = []

# Setting up a connection with the database
connection = db_connection(database=DB_NAME)

# For each query module extract the execution times for maximum number of repetitions
for query_module in query_modules.keys():

    # Make the query parameters depending on the current query module
    if query_module == 'editions':
        params = {
            'filter_key': edition_key
        }
    elif query_module == 'search':
        params = {
            'query': search_query
        }
    else:
        params = {}

    # Add limit and offset
    params['limit'] = limit
    params['offset'] = offset

    # For each SQL file query the database maximum number of repetitions and
    # extract execution times
    for query_filename in query_modules[query_module]:

        for i in range(max_reps):

            # Execute the current query for maximum number of repetitions
            data, column_names = execute_query(
                connection,
                params=params,
                query_module=query_module,
                query_filename=query_filename,
                performance=True
            )

            # Find the current execution time via regex
            execution_time_match = re.search(execution_time_pattern, data[-1][0])

            # If a match is found then add the current repetitions data to 'execution_times_data'
            if execution_time_match:
                time_ms = float(execution_time_match.group(1))

                execution_times_data.append(
                    (query_filename, i+1, time_ms)
                )

# Close the connection
connection.close()

# Make a dataframe from all data
df = pd.DataFrame(
    execution_times_data,
    columns=['query_file', 'rep', 'execution_time_ms']
)

# If current tables had index or not use the proper filename for the dataset
if INDEX:
    filename = 'index.csv'
else:
    filename = 'no_index.csv'

# Save the dataset with the proper name
df.to_csv(os.path.join(results_dir, filename), index=False)
