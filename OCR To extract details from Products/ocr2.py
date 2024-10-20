import easyocr
import cv2
import pandas as pd
import os
import re
from fuzzywuzzy import process

reader = easyocr.Reader(['en'], gpu=True)

image_paths = ['frills_cropped_0.jpg']
for image_path in image_paths:
    if not os.path.isfile(image_path):
        print(f"Error: The file '{image_path}' does not exist.")
        continue

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load the image at '{image_path}'. Check the file path and file integrity.")
        continue

    # Preprocess image for better OCR results (grayscale and denoising)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised_image = cv2.fastNlMeansDenoising(gray_image, None, 30, 7, 21)
    _, threshold_image = cv2.threshold(denoised_image, 128, 255, cv2.THRESH_BINARY)

    results = reader.readtext(threshold_image)
    # Clean the extracted texts
    extracted_texts = [
        re.sub(r'[^A-Za-z]', '', text).upper() for (_, text, _) in results if text and len(text) > 3
    ]
    extracted_texts = [text for text in extracted_texts if text and len(text) > 3]


    csv_file_path = 'product_data.csv'
    if not os.path.isfile(csv_file_path):
        print(f"Error: The file '{csv_file_path}' does not exist.")
        continue

    df = pd.read_csv(csv_file_path)
    df.iloc[:, 1] = df.iloc[:, 1].str.upper()  # Normalize CSV data

    # Fuzzy matching for better results
    for extracted_text in extracted_texts:
        best_match = process.extractOne(extracted_text, df.iloc[:, 1].tolist(), score_cutoff=70)
        if best_match:
            print(f"Best match for '{extracted_text}': {best_match[0]}")
        else:
            print(f"No matching result for '{extracted_text}'")
