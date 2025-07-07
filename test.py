import pandas as pd
import numpy as np

# Load CSV
df = pd.read_csv("iris.csv")

# For each column, randomly set 30% of values to NaN
for col in df.columns:
    mask = np.random.rand(len(df)) < 0.3  # 30% True
    df.loc[mask, col] = np.nan

# Save the modified CSV
df.to_csv("iris.csv", index=False)
