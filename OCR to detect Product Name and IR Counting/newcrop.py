import cv2
from ultralytics import YOLO
import os
import easyocr
import pandas as pd
import re

def ocrreader(image_path, label):
    reader = easyocr.Reader(['en'], gpu=True)

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
            extracted_texts.append(label)
        
            csv_file_path = 'product_data1.csv'
            
            if not os.path.isfile(csv_file_path):
                print(f"Error: The CSV file '{csv_file_path}' does not exist.")
                return
            
            df = pd.read_csv(csv_file_path)

            for extracted_text in extracted_texts:
                # Match the cleaned extracted text only with the second column of the CSV
                matching_results = df[df.iloc[:, 1].astype(str).str.contains(extracted_text, case=False, na=False)]
                    
                if not matching_results.empty:
                    # Print only specific columns from the first matching result
                    print(f"Search Results for '{extracted_text}':")
                    print(matching_results.iloc[0][['product', 'category', 'sub_category', 'brand', 'type', 'rating']])
                else:
                    print(f"No matching result for '{extracted_text}'")

# Initialize the YOLO model
model = YOLO('best.pt') # This is the model we (Invincible Titans) trained using YOLOv8

# Set up camera (adjust index if needed)
camera = cv2.VideoCapture(1) # Camera device, using phone camera via DroidCam

if not camera.isOpened():
    print("Error: Could not access the camera.")
else:
    print("Press 's' to capture a photo. Press 'q' to exit.")

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Error: Unable to capture a frame from the camera.")
            break
        
        # Display the camera feed
        cv2.imshow("Camera Feed", frame)        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            # Predict using YOLO model
            results = model.predict(source=frame, device='cuda', save=True, show=True)
            image = frame
            cropped_dir = 'cropped_images'
            if not os.path.exists(cropped_dir):
                os.makedirs(cropped_dir) 
            target_labels = ['frills', 'natkhat', 'tedhe_medhe', 'curlz', 'cheese_balls_crax', 'crax']
            
            # Process each detected object
            for idx, (box, cls) in enumerate(zip(results[0].boxes.xyxy, results[0].boxes.cls)):
                label = results[0].names[int(cls)]  # Get the label name from target labels
                if label in target_labels:
                    x1, y1, x2, y2 = map(int, box)
                    cropped_image = image[y1:y2, x1:x2]
                    
                    # Save the cropped image temporarily
                    temp_cropped_image_path = os.path.join(cropped_dir, f'{label}_cropped_{idx}.jpg')
                    cv2.imwrite(temp_cropped_image_path, cropped_image)
                    if target_labels == 'frills':
                        label = 'Frittz'
                    elif target_labels == 'natkhat':
                        label = 'Natkhat'
                    elif target_labels == 'tedhe_medhe':
                        label = 'Tedhe Medhe - Masala Tadka'
                    elif target_labels == 'curlz':
                        label = 'No Rulz Masala Curlz Corn Puffs'
                    elif target_labels == 'cheese_balls_crax':
                        label = 'Cheese Balls'
                    elif target_labels == 'crax':
                        label = 'Corn Rings - Tangy Tomato'
                    # Perform OCR on the saved cropped image
                    ocrreader(temp_cropped_image_path, label)
                    
            print(f'Cropped images for {target_labels} saved in {cropped_dir}')   

        elif key == ord('q'):
            print("Exiting...")
            break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
