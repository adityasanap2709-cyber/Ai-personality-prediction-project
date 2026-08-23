import os
import pandas as pd
import matplotlib.pyplot as plt # type: ignore

# Load dataset
df = pd.read_csv("dataset/OCEAN-synthetic.csv")

# Create output folder
os.makedirs("eda_output", exist_ok=True)

print("=" * 50)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 50)

# 1. Dataset Shape
print("\n1. Dataset Shape")
print(df.shape)

# 2. Dataset Information
print("\n2. Dataset Information")
df.info()

# 3. First Five Rows
print("\n3. First Five Rows")
print(df.head())

# 4. Last Five Rows
print("\n4. Last Five Rows")
print(df.tail())

# 5. Missing Values
print("\n5. Missing Values")
print(df.isnull().sum())

# 6. Duplicate Rows
print("\n6. Duplicate Rows")
print(df.duplicated().sum())

# 7. Statistical Summary
print("\n7. Statistical Summary")
print(df.describe())

# OCEAN Traits
traits = [
    "Openness",
    "Conscientiousness",
    "Extraversion",
    "Agreeableness",
    "Neuroticism"
]

# 8. Histograms
for trait in traits:
    plt.figure(figsize=(6,4))
    plt.hist(df[trait], bins=10)
    plt.title(f"{trait} Distribution")
    plt.xlabel(trait)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"eda_output/{trait}_histogram.png")
    plt.close()

# 9. Boxplots
for trait in traits:
    plt.figure(figsize=(4,6))
    plt.boxplot(df[trait])
    plt.title(f"{trait} Boxplot")
    plt.tight_layout()
    plt.savefig(f"eda_output/{trait}_boxplot.png")
    plt.close()

# 10. Correlation Matrix
correlation = df[traits].corr()

print("\n8. Correlation Matrix")
print(correlation)

plt.figure(figsize=(8,6))
plt.imshow(correlation, interpolation="nearest")
plt.colorbar()

plt.xticks(range(len(traits)), traits, rotation=45)
plt.yticks(range(len(traits)), traits)

plt.title("Correlation Heatmap")
plt.tight_layout()

plt.savefig("eda_output/correlation_heatmap.png")
plt.close()

print("\nEDA Completed Successfully!")
print("Graphs saved inside 'eda_output' folder.")