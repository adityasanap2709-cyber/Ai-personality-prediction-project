import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Create Output Folder
# -----------------------------
OUTPUT_FOLDER = "eda_output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# Load Dataset
# -----------------------------
DATASET_PATH = "dataset/OCEAN-synthetic.csv"

print("Loading Dataset...")
df = pd.read_csv(DATASET_PATH)

# -----------------------------
# Clean Dataset for Visualization
# -----------------------------
df = df.dropna()

traits = [
    "Openness",
    "Conscientiousness",
    "Extraversion",
    "Agreeableness",
    "Neuroticism"
]

# Keep valid values only
for col in traits:
    df = df[(df[col] >= 1) & (df[col] <= 5)]

df = df.reset_index(drop=True)

# -----------------------------
# Text Length
# -----------------------------
df["Text_Length"] = df["Text"].astype(str).apply(len)

# -----------------------------
# Create Dashboard
# -----------------------------
fig, axes = plt.subplots(4, 2, figsize=(18, 20))
fig.suptitle(
    "OCEAN Personality Dataset - EDA Dashboard",
    fontsize=22,
    fontweight="bold"
)

# -----------------------------
# Histograms
# -----------------------------
sns.histplot(df["Openness"], kde=True, ax=axes[0, 0], color="blue")
axes[0, 0].set_title("Openness")

sns.histplot(df["Conscientiousness"], kde=True, ax=axes[0, 1], color="green")
axes[0, 1].set_title("Conscientiousness")

sns.histplot(df["Extraversion"], kde=True, ax=axes[1, 0], color="orange")
axes[1, 0].set_title("Extraversion")

sns.histplot(df["Agreeableness"], kde=True, ax=axes[1, 1], color="purple")
axes[1, 1].set_title("Agreeableness")

sns.histplot(df["Neuroticism"], kde=True, ax=axes[2, 0], color="red")
axes[2, 0].set_title("Neuroticism")

# -----------------------------
# Correlation Heatmap
# -----------------------------
sns.heatmap(
    df[traits].corr(),
    annot=True,
    cmap="coolwarm",
    ax=axes[2, 1]
)
axes[2, 1].set_title("Correlation Heatmap")

# -----------------------------
# Boxplot
# -----------------------------
sns.boxplot(
    data=df[traits],
    ax=axes[3, 0]
)
axes[3, 0].set_title("OCEAN Traits Boxplot")

# -----------------------------
# Text Length Distribution
# -----------------------------
sns.histplot(
    df["Text_Length"],
    bins=20,
    kde=True,
    ax=axes[3, 1],
    color="teal"
)
axes[3, 1].set_title("Text Length Distribution")

# -----------------------------
# Save Dashboard
# -----------------------------
plt.tight_layout(rect=[0, 0, 1, 0.97])

dashboard_path = os.path.join(
    OUTPUT_FOLDER,
    "eda_dashboard.png"
)

plt.savefig(
    dashboard_path,
    dpi=300
)

plt.close()

print("\n===================================")
print("EDA Dashboard Created Successfully!")
print("Saved at:")
print(dashboard_path)
print("===================================")