from flask import Flask, render_template, request
import joblib
import os
import re
from PIL import Image
import pytesseract # type: ignore

# Tesseract OCR Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print("Current Folder :", os.getcwd())
print("App Location   :", __file__)
print("Templates Path :", os.path.join(os.getcwd(), "templates"))

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Load Model
model = joblib.load("saved_model/ocean_model.pkl")
vectorizer = joblib.load("saved_model/vectorizer.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # Get text from textarea
    text = request.form.get("text", "").strip()

    # Get uploaded image
    image = request.files.get("image")

    # If image is uploaded, extract text using OCR
    if image and image.filename != "":
        try:
            img = Image.open(image)

            text = pytesseract.image_to_string(
                img,
                lang="eng",
                config="--oem 3 --psm 6"
            ).strip()

            # Clean extracted text
            text = re.sub(r'http\S+', '', text)          # Remove URLs
            text = re.sub(r'@\w+', '', text)             # Remove usernames
            text = re.sub(r'#[A-Za-z0-9_]+', '', text)   # Remove hashtags
            text = re.sub(r'[^\w\s.,!?]', ' ', text)     # Remove special characters
            text = re.sub(r'\s+', ' ', text).strip()     # Remove extra spaces

        except Exception as e:
            return f"OCR Error: {e}"

    # If both text and image are empty
    if text == "":
        return "Please enter text or upload a screenshot."

    # Convert text to TF-IDF
    text_vector = vectorizer.transform([text])

    # Predict
    prediction = model.predict(text_vector)[0]

    # Store results
    result = {
        "Openness": round(prediction[0], 2),
        "Conscientiousness": round(prediction[1], 2),
        "Extraversion": round(prediction[2], 2),
        "Agreeableness": round(prediction[3], 2),
        "Neuroticism": round(prediction[4], 2)
    }

    return render_template(
        "result.html",
        result=result,
        extracted_text=text
    )


if __name__ == "__main__":
    app.run(debug=True)