"""
Transform

Note:
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
