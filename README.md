# 🚗 License Plate Detection and Logging System 🚓  

## 📢 Project Overview  
This project is a **License Plate Detection and Logging System**, designed to detect license plates from video streams, recognize the text on the plates, and log the details efficiently. It combines the power of **YOLOv10**, a state-of-the-art object detection model, and **PaddleOCR** for optical character recognition, along with seamless integration into a **SQL database** for robust data management.  

The system was developed in two phases:  
1. **Model Training**: A custom **YOLOv10 model** was trained using a specialized license plate dataset to ensure high accuracy. The trained model was saved and integrated into the system.  
2. **Project Integration**: The trained model was used to process video streams, detect license plates in real-time, recognize text using PaddleOCR, and store the results in both JSON files and a SQL database.  

---

## 💡 Key Features  

1. **Real-Time Detection**:  
   Utilizes the trained YOLOv10 model to detect license plates in live video streams.  

2. **Text Recognition**:  
   Extracts text from detected license plates using PaddleOCR with high accuracy, even in challenging scenarios.  

3. **SQL Database Integration**:  
   Logs detected license plate details, along with start and end timestamps, into a SQL database for organized storage and retrieval.  

4. **JSON Logging**:  
   - Generates interval-based JSON files every 20 seconds.  
   - Maintains a cumulative JSON file for tracking all detections.  

5. **Professional Visualization**:  
   Displays bounding boxes and recognized text directly on the video stream.  

---

## 🛠️ Tech Stack  

- **Python**: Programming language.  
- **YOLOv10**: Object detection model for real-time license plate detection.  
- **PaddleOCR**: Optical character recognition for reading license plate text.  
- **OpenCV**: Video processing and visualization.  
- **MySQL**: Database for logging license plate details.  
- **JSON**: For interval-based and cumulative logging.  

---

## 📌 How to Use  

### Prerequisites  

1. **Install Required Libraries**  
   Run the following command to install all dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up MySQL Database**
- Create a database named licensePlatedb.
- Create a table using the following SQL script:
  ```bash
  CREATE TABLE IF NOT EXISTS LicensePlates(
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_time TEXT,
    end_time TEXT,
    license_plate TEXT);
  ```

## **📽️ Output**
- Detected Video: Bounding boxes and recognized text are displayed in real-time.
- JSON Logs: Detected license plate details are saved in the json/ directory.
- SQL Database: Logs are stored in the LicensePlates table with start and end timestamps.

## ✨ **Example Outputs**
### JSON Log:
Interval-Based JSON:

```bash
{
    "Start Time": "2024-11-21T10:00:00",
    "End Time": "2024-11-21T10:00:20",
    "License Plate": ["ABC123", "XYZ789"]
}
```

## **Demo**
[Demo 1](https://drive.google.com/file/d/1MjsbiZYaWaiwoMx81VfzDvRHjjQL0K4C/view?usp=drive_link)

[Demo 2](https://drive.google.com/file/d/1MkJkQcfOrjxBAtgMVLSo3gkmFIURpZeR/view?usp=drive_link)

## 🤝 **Contribution**
Feel free to fork this repository and make improvements. Pull requests are welcome!
