import pandas as pd

# Load chunks dataset
df = pd.read_csv("data/processed/rtc_chunks.csv")

print("Columns:")
print(df.columns)

print("\nShape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())