import pandas as pd
import re

df = pd.read_csv("dataset/OCEAN-synthetic.csv")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["Text"] = df["Text"].apply(clean_text)

df.to_csv("dataset/cleaned_dataset.csv", index=False)

print("Dataset Cleaned Successfully")