import pandas as pd

df = pd.read_csv("dataset/OCEAN-synthetic.csv")

print("Duplicate Rows :", df.duplicated().sum())

df = df.drop_duplicates()

print("Dataset Shape After Removing Duplicates :", df.shape)

df.to_csv("dataset/ocean_no_duplicates.csv", index=False)

print("Duplicate-free dataset saved.")