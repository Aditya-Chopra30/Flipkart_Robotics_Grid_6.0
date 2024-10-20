import cv2
from ultralytics import YOLO
import os
import easyocr
import pandas as pd
import re
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple OCR Interface")
        self.root.geometry("800x600")

        self.model = YOLO('best.pt')  # YOLO model
        self.camera = cv2.VideoCapture(1)  # Camera device index

        if not self.camera.isOpened():
            print("Error: Could not access the camera.")
            return

        self.cropped_dir = 'cropped_images'
        if not os.path.exists(self.cropped_dir):
            os.makedirs(self.cropped_dir)

        # Setup UI components
        self.setup_ui()

        # Start video feed
        self.update_camera_feed()

    def setup_ui(self):
        # Camera feed
        self.camera_label = tk.Label(self.root)
        self.camera_label.pack(padx=10, pady=10)

        # Button to capture image
        self.capture_button = ttk.Button(self.root, text="Capture", command=self.capture_image)
        self.capture_button.pack(pady=10)

        # Results display
        self.results_text = tk.Text(self.root, wrap='word', height=15, width=70)
        self.results_text.pack(padx=10, pady=10)

    def update_camera_feed(self):
        ret, frame = self.camera.read()
        if not ret:
            self.root.after(10, self.update_camera_feed)
            return

        # Convert to Tkinter format
        cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2_image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.camera_label.imgtk = imgtk
        self.camera_label.configure(image=imgtk)

        # Continue updating the camera feed
        self.root.after(10, self.update_camera_feed)

    def capture_image(self):
        ret, frame = self.camera.read()
        if not ret:
            self.results_text.insert(tk.END, "Error: Unable to capture a frame from the camera.\n")
            return

        # Predict using YOLO model
        results = self.model.predict(source=frame, device='cuda', save=True, show=True)
        self.process_detection_results(frame, results)

    def process_detection_results(self, frame, results):
        self.results_text.delete(1.0, tk.END)  # Clear previous results

        reader = easyocr.Reader(['en'], gpu=True)
        csv_file_path = 'product_data1.csv'
        if not os.path.isfile(csv_file_path):
            self.results_text.insert(tk.END, f"Error: The CSV file '{csv_file_path}' does not exist.\n")
            return
        df = pd.read_csv(csv_file_path)

        for idx, (box, cls) in enumerate(zip(results[0].boxes.xyxy, results[0].boxes.cls)):
            label = results[0].names[int(cls)]
            x1, y1, x2, y2 = map(int, box)
            cropped_image = frame[y1:y2, x1:x2]
            temp_cropped_image_path = os.path.join(self.cropped_dir, f'{label}_cropped_{idx}.jpg')
            cv2.imwrite(temp_cropped_image_path, cropped_image)

            # Perform OCR on the saved cropped image
            ocr_results = reader.readtext(cropped_image)
            extracted_texts = [
                re.sub(r'[^A-Za-z]', '', text) for (_, text, _) in ocr_results if text and len(text) > 3
            ]

            # Display the OCR results in a tabular format
            for extracted_text in extracted_texts:
                matching_results = df[df.iloc[:, 1].astype(str).str.contains(extracted_text, case=False, na=False)]
                
                if not matching_results.empty:
                    self.results_text.insert(tk.END, f"\nSearch Results for '{extracted_text}':\n")
                    self.results_text.insert(tk.END, f"{'Product':<30} {'Category':<20} {'Sub-category':<20} {'Brand':<15} {'Type':<25} {'Rating':<5}\n")
                    self.results_text.insert(tk.END, "-"*115 + "\n")
                    
                    for index, row in matching_results.iterrows():
                        self.results_text.insert(
                            tk.END, 
                            f"{row['product']:<30} {row['category']:<20} {row['sub_category']:<20} {row['brand']:<15} {row['type']:<25} {row['rating']:<5}\n"
                        )
                # else:
                #     self.results_text.insert(tk.END, f"No matching result for '{extracted_text}'\n")

    def close(self):
        self.camera.release()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
