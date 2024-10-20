import torch
from ultralytics import YOLO
import cv2
import os
import easyocr
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Processor App")
        master.geometry("800x600")

        self.label = Label(master, text="Select a folder to process images")
        self.label.pack()

        self.process_button = Button(master, text="Select Folder", command=self.select_folder)
        self.process_button.pack()

        self.result_label = Label(master, text="")
        self.result_label.pack()

        self.image_label = Label(master)
        self.image_label.pack()

        self.current_image_index = 0
        self.cropped_images = []

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.label.config(text=f"Selected folder: {folder_path}")
            self.process_images(folder_path)

    def process_images(self, folder_path):
        # Load the trained YOLO model
        model = YOLO('Trained Model/best.pt')

        # Directory to save cropped images
        cropped_dir = 'cropped_images'
        if not os.path.exists(cropped_dir):
            os.makedirs(cropped_dir)

        # Clear previous images
        self.cropped_images.clear()

        # Define target labels for cropping
        target_labels = ['expiry', 'price']

        # Iterate through all images in the folder
        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)

            # Perform detection on the image
            results = model.predict(source=image_path, save=True, show=False)

            # Load the original image
            image = cv2.imread(image_path)

            if image is None:
                self.result_label.config(text=f"Error: Could not read {image_name}")
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

                    # Store the cropped image path for display
                    self.cropped_images.append(cropped_image_path)

        self.result_label.config(text=f"Processed images saved in {cropped_dir}")
        self.current_image_index = 0  # Reset index to the first image
        self.show_next_image()

    def perform_ocr_on_image(self, image_path):
        # Initialize the EasyOCR reader
        reader = easyocr.Reader(['en'], gpu=True)

        # Load the cropped image
        image = cv2.imread(image_path)

        if image is None:
            self.result_label.config(text=f"Error: Could not read {os.path.basename(image_path)}")
            return image, []

        # Perform OCR on the image
        results = reader.readtext(image_path)
        return image, results

    def show_next_image(self):
        if not self.cropped_images:
            self.result_label.config(text="No cropped images to display.")
            return

        # Get the current cropped image path
        image_path = self.cropped_images[self.current_image_index]
        self.current_image_index = (self.current_image_index + 1) % len(self.cropped_images)

        # Perform OCR on the image and get results
        image, ocr_results = self.perform_ocr_on_image(image_path)

        # Display OCR results
        ocr_text = f'OCR results for {os.path.basename(image_path)}:'
        for (bbox, text, confidence) in ocr_results:
            ocr_text += f'\nText: {text}, Confidence: {confidence:.2f}'

            # Draw bounding boxes on the image
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        self.result_label.config(text=ocr_text)

        # Convert image for Tkinter display
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        tk_image = ImageTk.PhotoImage(pil_image)

        # Display the image on the UI
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image  # Keep a reference

        # Schedule the next image to be shown after 3 seconds
        self.master.after(3000, self.show_next_image)

if __name__ == "__main__":
    root = Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
