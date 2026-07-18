"""
Simple pipeline execution utility.

Runs a sequence of Python task scripts in order using subprocess execution,
allowing lightweight orchestration of ETL stages without integrated logging.
"""

import os
import subprocess
import sys

def run_pipeline(tasks_dir: str, tasks: list[str]) -> None:
    """
    Function for running a pipeline without logging
    :param tasks_dir: str, the directory containing the task py files
    :param tasks: list[str], the list/sequency of py task files
    :return: None
    """

    # The filepaths for each file
    filepaths = [
        os.path.join(tasks_dir, task)
        for task in tasks
    ]

    # Running the pipeline
    for task, filename in zip(tasks, filepaths):
        print(f"{task.removesuffix('.py').replace('_', " ").title()}...")
        subprocess.run([sys.executable, filename], check=True)