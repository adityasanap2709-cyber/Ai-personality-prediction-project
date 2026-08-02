import torch
from transformers import BertTokenizer

from training.model import OceanBERT
from training.config import (
    MODEL_NAME,
    MODEL_SAVE_PATH,
    MAX_LENGTH,
    DEVICE,
)

# Load BERT Tokenizer
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

# Load Trained Model
model = OceanBERT()
model.load_state_dict(
    torch.load(
        MODEL_SAVE_PATH + "ocean_bert.pth",
        map_location=DEVICE,
    )
)
model.to(DEVICE)
model.eval()


def predict_personality(text):
    """
    Predict OCEAN personality scores from input text.
    """

    encoding = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )

    input_ids = encoding["input_ids"].to(DEVICE)
    attention_mask = encoding["attention_mask"].to(DEVICE)

    with torch.no_grad():
        output = model(input_ids, attention_mask)

    scores = output.squeeze().cpu().numpy()

    prediction = {
        "Openness": round(float(scores[0]), 2),
        "Conscientiousness": round(float(scores[1]), 2),
        "Extraversion": round(float(scores[2]), 2),
        "Agreeableness": round(float(scores[3]), 2),
        "Neuroticism": round(float(scores[4]), 2),
    }

    return prediction


if __name__ == "__main__":

    sample = input("Enter a social media post:\n\n")

    result = predict_personality(sample)

    print("\nPredicted OCEAN Scores\n")

    for trait, score in result.items():
        print(f"{trait}: {score}")