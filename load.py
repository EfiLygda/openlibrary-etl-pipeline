"""
Load tables to romance_fiction PostgreSQL database
"""

import os
from config.paths import ROOT_DIR
from utilities.pipeline import run_pipeline

# Set up directory containing the pipeline py files
tasks_dir = os.path.join(ROOT_DIR, 'load')

# The pipeline's py filenames for extracting JSON files via the API
tasks = [
    'create_database.py',
    'create_tables.py',
    'load_tables.py'
]

# Run the pipeline
run_pipeline(
    tasks_dir=tasks_dir,
    tasks=tasks
)
