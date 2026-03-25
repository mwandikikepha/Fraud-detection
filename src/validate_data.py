import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TRAIN_DATA_PATH

# Load the data
df = pd.read_csv(TRAIN_DATA_PATH)

# Shape of dataset
print("Dataset shape:", df.shape)

# Column info
df.info()

# Check missing values
print(df.isnull().sum())