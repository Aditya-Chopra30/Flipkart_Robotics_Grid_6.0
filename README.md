# Flipkart_Robotics_Grid_6.0
<h1 align="center">
    <img src="https://readme-typing-svg.herokuapp.com/?font=Righteous&size=35&center=true&vCenter=true&width=800&height=70&duration=4000&lines=Autonomous+Warehouse+Project+🚀🏬;" />
</h1>

This project aims to create a comprehensive autonomous system for warehouse management, incorporating key technologies like AI, IoT, and automation. The project is divided into four main tasks:

1. **Fruit Freshness Detection**
2. **Product Detection**
3. **OCR Extraction of Brand Name and Product Name**
4. **OCR Extraction of Expiry Date, Label, Mfg, and Price**

---

## 1. Fruit Freshness Detection 🍎🍌

The first step involves identifying the freshness of fruits and vegetables. Follow the guide below to set up the model and integrate it with a microcontroller for real-time detection.

### Step 1: Download the Dataset

Download the dataset required for this task from the link below:
[Download Fruit Freshness Dataset](https://drive.google.com/file/d/1Ya6miJYHvw6G2hnfsGiKFA6FIKYpHJjH/view?usp=drive_link)

### Step 2: Train the Model

1. Open the following Jupyter Notebook to start training the model:
   [Fruit Freshness Image Classification Model](https://github.com/TechArcanist/Flipkart_Robotics_Grid_6.0/blob/main/Fruit%20Freshness/Image_Class_Model.ipynb)

   Set the dataset paths correctly in the notebook:
   ```python
   data_train_path = 'Fruits_Vegetables/train'
   data_test_path = 'Fruits_Vegetables/test'
   data_val_path = 'Fruits_Vegetables/test'
   ```

2. Run all the cells in the notebook. Once the training is complete, the model will be saved.

### Step 3: Microcontroller Setup

After the model training, proceed to set up the microcontroller for real-time fruit freshness checking.

1. Open the Arduino IDE.
2. Follow the connection diagram below to connect the ESP32 and DHT22 sensors.
3. ![Doc1_page-0001](https://github.com/user-attachments/assets/4b4af15f-4539-4e98-9243-8132bae3b156)

4. Compile and upload the following code to your ESP32 microcontroller:
   [ESP32 Arduino Code](https://github.com/TechArcanist/Flipkart_Robotics_Grid_6.0/blob/main/Fruit%20Freshness/sketch_oct20a.ino)

### Step 4: Running the Freshness Check

1. Use the following notebook to execute the freshness check:
   [Fruit Freshness Check Notebook](https://github.com/TechArcanist/Flipkart_Robotics_Grid_6.0/blob/main/Fruit%20Freshness/image%20class%20model%20check.ipynb)

2. Execute all cells in the notebook. You will be presented with two options:
   - **Capture pictures randomly**: Take new photos for checking.
   - **Select from folder**: Choose existing images for analysis.

3. Follow the instructions, and the model will analyze the fruit's freshness.

### Congratulations 🎉 
You have successfully set up and executed the fruit freshness detection system. Repeat these steps for testing different fruits and vegetables!

---

## 2. 🏷 Product Detection and IR Counting

To get started with product detection and IR counting, follow these steps:

### Step 1: Download the Dataset
First, download the dataset from the link below:
- [Product Detection Dataset](https://drive.google.com/file/d/12r8oJrfIxTyvC-fBMLoB9EbhCXBQUeV9/view?usp=sharing)

After downloading, extract the folder.

### Step 2: Prepare Dataset for Training
1. Open the extracted folder using Visual Studio Code.
2. Edit the yaml file to set the correct paths according to your directory structure:
   yaml
   train: your_path/train/images 
   val: your_path/valid/images
   test: your_path/test/images
   

### Step 3: Train the Model
Create a Python file and use the code from the link below to start training:
- [Training Code](https://github.com/TechArcanist/Flipkart_Robotics_Grid_6.0/blob/main/Image%20Recognition%20and%20IR%20Counting/yola.py)

After training completes, you can check the runs/detect/predict folder to verify the accuracy. You should see that the trained model is saved as best.pt. Copy this file and paste it into your current project folder.

### Step 4: Test the Trained Model on Live Camera
Use the following code to test the trained model on a live camera:
- [Live Camera Testing Code](https://github.com/TechArcanist/Flipkart_Robotics_Grid_6.0/blob/main/Image%20Recognition%20and%20IR%20Counting/camera.py)

Once executed, you will see results like the one shown below.

### Step 5: IR Counting Integration
1. Open the Arduino IDE.
2. Follow the circuit diagram below for connections.
3. Upload the code to your microcontroller:
   - [IR Counting Code](https://github.com/TechArcanist/Flipkart_Robotics_Grid_6.0/blob/main/Image%20Recognition%20and%20IR%20Counting/sketch_mar11a.ino)

You can build your own conveyor belt to automate the process.

### Step 6: Combining Product Detection and IR Counting
To integrate both product detection and IR counting, use the following code via VS Code:
- [Combined Product Detection and IR Counting Code](https://github.com/TechArcanist/Flipkart_Robotics_Grid_6.0/blob/main/Image%20Recognition%20and%20IR%20Counting/ir.py)

🎉 Congratulations! You have successfully set up product detection and IR counting for your warehouse automation.

Here's the updated README section for **OCR Extraction of Expiry Date, MFG, and Price** in your Autonomous Warehouse Project:


idhar kro

This guide follows a structured approach, ensuring clarity and easy follow-along steps. It includes the essential code links and instructions to help set up OCR extraction efficiently.
**Stay Tuned!**  
More guides on Product Detection, OCR Extraction of Brand/Product Names, and Expiry Date Labeling are coming soon.

Feel free to explore the code, suggest improvements, and reach out if you need any assistance.

---

<h1 align="center">
    <img src="https://readme-typing-svg.herokuapp.com/?font=Righteous&size=35&center=true&vCenter=true&width=500&height=70&duration=4000&lines=Thanks+for+Visiting!+👋;" />
</h1>
