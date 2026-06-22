"""
Script for calculating % improvements and speedup factors after creating indexes
"""

import os
import pandas as pd

# Setting up the results directory where the data are located
results_dir = os.path.join('./','results')

# Reading both files
no_index = pd.read_csv(os.path.join(results_dir, 'no_index.csv'))
index = pd.read_csv(os.path.join(results_dir, 'index.csv'))

# Calculating mean execution times for each file
mean_exec_time_no_index = no_index.groupby('query_file')['execution_time_ms'].mean()
mean_exec_time_index = index.groupby('query_file')['execution_time_ms'].mean()

# Calculating % boost and speed up
boosts = (mean_exec_time_no_index - mean_exec_time_index) / mean_exec_time_no_index * 100
speed_up = mean_exec_time_no_index / mean_exec_time_index

# Displaying results
print(f'% improvement (boost): \n\n{boosts}\n', end=100*'-' + '\n')
print(f'Speedup factors: \n\n{speed_up}\n')
