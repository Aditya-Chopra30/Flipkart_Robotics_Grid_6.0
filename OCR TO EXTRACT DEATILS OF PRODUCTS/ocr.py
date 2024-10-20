import easyocr
import cv2
import pandas as pd
import os
import re

reader = easyocr.Reader(['en'], gpu=True)

image = ['frills_cropped_0.jpg']
for image_path in image:
    if not os.path.isfile(image_path):
        print(f"Error: The file '{image_path}' does not exist.")
    else:
        image = cv2.imread(image_path)

        if image is None:
            print(f"Error: Unable to load the image at '{image_path}'. Check the file path and file integrity.")
        else:
            results = reader.readtext(image)
            # Clean the extracted texts to contain only regular characters
            extracted_texts = [
                re.sub(r'[^A-Za-z]', '', text) for (_, text, _) in results if text and len(text) > 3
            ]
            # Filter out any empty strings or texts that are too short
            extracted_texts = [text for text in extracted_texts if text and len(text) > 3]
            extracted_texts.append('Frittz')
            csv_file_path = 'product_data.csv'
            df = pd.read_csv(csv_file_path)

            for extracted_text in extracted_texts:
                # Match the cleaned extracted text only with the second column of the CSV
                matching_results = df[df.iloc[:, 1].astype(str).str.contains(extracted_text, case=False, na=False)]

                if not matching_results.empty:

                    # Print only the first matching result
                    print(f"Search Results for '{extracted_text}':")
                    print(matching_results.iloc[0])  # Print the first row of the matching results
                else:
                    print(f"No matching result for '{extracted_text}'")
