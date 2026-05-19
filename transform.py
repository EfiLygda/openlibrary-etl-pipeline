"""
Transform JSON files to tables (CSV files)
1. authors.csv
2. authors_alternative_names.csv
3. authors_statistics.csv
4. authors_works.csv
5. editions.csv
6. editions_contents.csv
7. editions_contributors.csv
8. editions_details.csv
9. editions_publishing.csv
10. works.csv
11. works_availability.csv
12. works_people.csv
13. works_places.csv
14. works_series.csv
15. works_subjects.csv
16. works_time_periods.csv
"""

import os
from config.paths import ROOT_DIR
from utilities.pipeline import run_pipeline

# Set up directory containing the pipeline py files
tasks_dir = os.path.join(ROOT_DIR, 'transform')

# The pipeline's py filenames for preprocessing and saving to CSV tables
tasks = [
    "author_tables.py",
    "editions_tables.py",
    "works_tables.py",
]

# Run the pipeline
run_pipeline(
    tasks_dir=tasks_dir,
    tasks=tasks
)
