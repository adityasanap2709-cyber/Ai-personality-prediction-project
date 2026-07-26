import pandas as pd
import nltk # type: ignore

from nltk.corpus import stopwords # type: ignore
from nltk.stem import WordNetLemmatizer # type: ignore

nltk.download("stopwords")
nltk.download("wordnet")

df = pd.read_csv("dataset/cleaned_dataset.csv")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess(text):

    words = text.split()

    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)

df["Text"] = df["Text"].apply(preprocess)

df.to_csv("dataset/processed_dataset.csv", index=False)

print("Preprocessing Completed")