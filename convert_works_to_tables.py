import os
import json
import numpy as np
import pandas as pd
from dataset_initilize import RAW_PAGES_DIR

GENRE = 'romance_fiction'
DIR = os.path.join(RAW_PAGES_DIR, GENRE)

for file in os.listdir(DIR):

    filename = os.path.join(DIR,file)

    with open(filename, mode='r') as j:
        data = json.load(j)
        print(data)
