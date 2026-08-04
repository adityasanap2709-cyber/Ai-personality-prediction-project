
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

from training.predict import predict_personality
from utils.ocr import extract_text

app = Flask(__name__)

# -----------------------------
# Upload Folder
# -----------------------------
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template(
        "index.html",
        prediction=None,
        input_text=""
    )


# -----------------------------
# Predict Personality
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    text = request.form.get("text", "").strip()

    image = request.files.get("image")

    # Screenshot Upload
    if image and image.filename != "":

        filename = secure_filename(image.filename)

        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        image.save(image_path)

        text = extract_text(image_path)

    # No Input
    if text == "":

        return render_template(
            "index.html",
            prediction=None,
            input_text="",
            error="Please enter text or upload a screenshot."
        )

    # Prediction
    
    result = predict_personality(text)

    print("\n========== RESULT ==========")
    for key, value in result.items():
        print(key, type(value), value)
    print("============================")

    return render_template(
        "index.html",
        prediction=result,
        input_text=text,
        error=None
    )
    # -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)