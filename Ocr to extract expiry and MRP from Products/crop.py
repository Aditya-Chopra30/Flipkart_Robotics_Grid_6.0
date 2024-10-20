import torch
from ultralytics import YOLO
import cv2
import os
import easyocr
import matplotlib.pyplot as plt

def process_images(folder_path):
    # Load the trained YOLO model
    model = YOLO('Trained Model/best.pt')

    # Directory to save cropped images
    cropped_dir = 'cropped_images'
    if not os.path.exists(cropped_dir):
        os.makedirs(cropped_dir)

    # Define target labels for cropping
    target_labels = ['expiry', 'price']

    # Iterate through all images in the folder
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)

        # Perform detection on the image
        results = model.predict(source=image_path, save=True, show=True)

        # Load the original image
        image = cv2.imread(image_path)

        if image is None:
            print(f"Error: Could not read {image_name}")
            continue

        # Iterate through results and save cropped bounding boxes for target labels
        for idx, (box, cls) in enumerate(zip(results[0].boxes.xyxy, results[0].boxes.cls)):
            label = results[0].names[int(cls)]  # Get the label name

            # Check if the detected label is in the target list
            if label in target_labels:
                x1, y1, x2, y2 = map(int, box)

                # Crop the image
                cropped_image = image[y1:y2, x1:x2]

                # Save the cropped image
                cropped_image_path = os.path.join(cropped_dir, f'{label}_cropped_{image_name}_{idx}.jpg')
                cv2.imwrite(cropped_image_path, cropped_image)

        print(f'Processed {image_name}: Cropped images for {target_labels} saved in {cropped_dir}')

def perform_ocr_on_cropped_images():
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=True)

    # Directory containing cropped images
    cropped_dir = 'cropped_images'

    # Check if the directory exists
    if not os.path.exists(cropped_dir):
        print(f"Error: {cropped_dir} does not exist.")
        return

    # Iterate through all cropped images in the folder
    for cropped_image_name in os.listdir(cropped_dir):
        cropped_image_path = os.path.join(cropped_dir, cropped_image_name)

        # Load the cropped image
        image = cv2.imread(cropped_image_path)

        if image is None:
            print(f"Error: Could not read {cropped_image_name}")
            continue

        # Perform OCR on the image
        results = reader.readtext(cropped_image_path)

        # Display the results
        print(f'OCR results for {cropped_image_name}:')
        for (bbox, text, confidence) in results:
            print(f'Text: {text}, Confidence: {confidence:.2f}')

            # Draw bounding boxes on the image
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Show the image with detected text
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    # Folder containing the test images
    test_folder = 'test_these'

    # Call the function to process images
    process_images(test_folder)

    # Perform OCR on cropped images
    perform_ocr_on_cropped_images()
