import pytesseract
from PIL import Image
import os

# ----------------------------------------------------
# Tesseract OCR Path (Windows)
# ----------------------------------------------------
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(image_path):
    """
    Extract text from an uploaded image.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    image = Image.open(image_path)

    text = pytesseract.image_to_string(
        image,
        lang="eng"
    )

    # Clean extracted text
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = " ".join(text.split())

    return text


# ----------------------------------------------------
# Testing
# ----------------------------------------------------
if __name__ == "__main__":

    image = input("Enter image path: ")

    extracted = extract_text(image)

    print("\n==============================")
    print("Extracted Text")
    print("==============================\n")
    print(extracted)