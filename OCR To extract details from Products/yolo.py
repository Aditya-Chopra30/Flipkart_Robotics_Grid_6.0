import cv2
from ultralytics import YOLO
import torch
import os
import easyocr
import pandas as pd
import re
def ocrreader(framez,labelz):
    reader = easyocr.Reader(['en'], gpu=True)

    image_path = framez
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
model = YOLO('best.pt')#this is the model we(Invincible Titans) trained using yolov8 

camera = cv2.VideoCapture(1)#camera device we used phone camera using droid camera

if not camera.isOpened():
    print("Error: Could not access the camera.")
else:
    print("Press 's' to capture a photo. Press 'q' to exit.")

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Error: Unable to capture a frame from the camera.")
            break
        cv2.imshow("Camera Feed", frame)        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):

            results = model.predict(source=frame, device='cuda', save=True, show=True)#here the prediction will be done using our model for the photo clicked using phone and captured in the frame variable
            image = frame
            cropped_dir = 'cropped_images'
            if not os.path.exists(cropped_dir):
                os.makedirs(cropped_dir) 
            target_labels = ['frills', 'natkhat', 'tedhe_medhe','curlz','cheese_balls_crax','crax']
            for idx, (box, cls) in enumerate(zip(results[0].boxes.xyxy, results[0].boxes.cls)):
                label = results[0].names[int(cls)]  
                if label in target_labels:
                    x1, y1, x2, y2 = map(int, box)
                    cropped_image = image[y1:y2, x1:x2]
                    ocrreader(cropped_image,label)
                    cropped_image_path = os.path.join(cropped_dir, f'{label}_cropped_{idx}.jpg')
                    cv2.imwrite(cropped_image_path, cropped_image)
                    
            print(f'Cropped images for {target_labels} saved in {cropped_dir}')   

        elif key == ord('q'):
            print("Exiting...")
            break


camera.release()
cv2.destroyAllWindows()
