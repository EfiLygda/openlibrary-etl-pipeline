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
import subprocess
import sys
from config.paths import ROOT_DIR

# Set up directory containing the pipeline py files
tasks_dir = os.path.join(ROOT_DIR, 'transform')

# The pipeline's py filenames for extracting JSON files via the API
tasks = [
    "author_tables.py",
    "editions_tables.py",
    "works_tables.py",
]

# The filepaths for each file
filepaths = [
    os.path.join(tasks_dir, task)
    for task in tasks
]

# Running the pipeline
for task, filename in zip(tasks, filepaths):
    print(f"{task.removesuffix('.py').replace('_', " ").title()}...")
    subprocess.run([sys.executable, filename], check=True)
