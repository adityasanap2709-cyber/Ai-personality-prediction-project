import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Create output folder
# -----------------------------
OUTPUT_FOLDER = "eda_output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# Load Dataset
# -----------------------------
DATASET_PATH = "dataset/OCEAN-synthetic.csv"

print("Loading Dataset...\n")

df = pd.read_csv(DATASET_PATH)

print("Dataset Loaded Successfully!\n")

# -----------------------------
# Dataset Shape
# -----------------------------
print("=" * 50)
print("DATASET SHAPE")
print("=" * 50)

print(df.shape)

# -----------------------------
# Dataset Info
# -----------------------------
print("\n" + "=" * 50)
print("DATASET INFORMATION")
print("=" * 50)

print(df.info())

# -----------------------------
# Missing Values
# -----------------------------
print("\n" + "=" * 50)
print("MISSING VALUES")
print("=" * 50)

print(df.isnull().sum())

# -----------------------------
# Statistical Summary
# -----------------------------
print("\n" + "=" * 50)
print("STATISTICAL SUMMARY")
print("=" * 50)

print(df.describe())

# -----------------------------
# OCEAN Columns
# -----------------------------
traits = [
    "Openness",
    "Conscientiousness",
    "Extraversion",
    "Agreeableness",
    "Neuroticism",
]

# -----------------------------
# Histograms
# -----------------------------
for trait in traits:

    plt.figure(figsize=(7,5))

    sns.histplot(
        df[trait],
        bins=15,
        kde=True
    )

    plt.title(f"{trait} Distribution")

    plt.savefig(
        f"{OUTPUT_FOLDER}/{trait}_distribution.png"
    )

    plt.close()

print("\nTrait Distribution Graphs Saved.")

# -----------------------------
# Correlation Heatmap
# -----------------------------
plt.figure(figsize=(8,6))

sns.heatmap(
    df[traits].corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")

plt.savefig(
    f"{OUTPUT_FOLDER}/correlation_heatmap.png"
)

plt.close()

print("Correlation Heatmap Saved.")

# -----------------------------
# Boxplots
# -----------------------------
plt.figure(figsize=(10,6))

sns.boxplot(data=df[traits])

plt.title("OCEAN Traits Boxplot")

plt.savefig(
    f"{OUTPUT_FOLDER}/boxplot.png"
)

plt.close()

print("Boxplot Saved.")

# -----------------------------
# Text Length Distribution
# -----------------------------
df["Text_Length"] = df["Text"].astype(str).apply(len)

plt.figure(figsize=(8,5))

sns.histplot(
    df["Text_Length"],
    bins=20,
    kde=True
)

plt.title("Text Length Distribution")

plt.savefig(
    f"{OUTPUT_FOLDER}/text_length_distribution.png"
)

plt.close()

print("Text Length Distribution Saved.")

# -----------------------------
# Finish
# -----------------------------
print("\n" + "=" * 50)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 50)

print(f"\nGraphs saved inside '{OUTPUT_FOLDER}' folder.")