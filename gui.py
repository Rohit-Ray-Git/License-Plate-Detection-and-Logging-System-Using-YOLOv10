import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import os
from ultralytics import YOLOv10
from datetime import datetime
import numpy as np
import math
import re
from paddleocr import PaddleOCR
import mysql.connector

# Initialize the Paddle OCR
ocr = PaddleOCR(use_angle_cls=True, use_gpu=False)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# YOLOv10 model
model = YOLOv10("yolov10/best.pt")

# License plate class name
className = ["License"]

class LicensePlateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("License Plate Detection and Logging System")
        self.video_path = None
        self.running = False
        self.cap = None

        # GUI Layout
        self.setup_gui()

    def setup_gui(self):
        # Upload Video Button
        upload_btn = tk.Button(self.root, text="Upload Video", command=self.upload_video, width=20, bg="lightblue")
        upload_btn.pack(pady=10)

        # Process Video Button (Initially Disabled)
        self.process_btn = tk.Button(self.root, text="Start Processing", command=self.process_video, width=20, bg="lightgreen", state=tk.DISABLED)
        self.process_btn.pack(pady=10)

        # Canvas to display video
        self.canvas = tk.Canvas(self.root, width=800, height=450, bg="black")
        self.canvas.pack(pady=10)

        # Real-time Table Section
        table_label = tk.Label(self.root, text="Real-Time License Plate Data", font=("Arial", 14))
        table_label.pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("start_time", "end_time", "license_plate"), show="headings")
        self.tree.heading("start_time", text="Start Time")
        self.tree.heading("end_time", text="End Time")
        self.tree.heading("license_plate", text="License Plate")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Logging Section
        log_label = tk.Label(self.root, text="Log Messages", font=("Arial", 14))
        log_label.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(self.root, width=80, height=8)
        self.log_text.pack(pady=10)

    def log_message(self, message):
        """Log a message in the text area."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def update_table(self, start_time, end_time, license_plate):
        """Add a new row to the table."""
        self.tree.insert("", tk.END, values=(start_time, end_time, license_plate))

    def upload_video(self):
        """Handle video file upload."""
        self.video_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mkv")]
        )
        if self.video_path:
            self.log_message(f"Video uploaded: {self.video_path}")
            self.process_btn.config(state=tk.NORMAL)  # Enable the Process button
        else:
            self.log_message("No video selected.")
            self.process_btn.config(state=tk.DISABLED)  # Keep the Process button disabled

    def process_video(self):
        """Process the video for license plate detection."""
        if not self.video_path:
            messagebox.showerror("Error", "Please upload a video before starting the process.")
            return

        self.log_message("Starting processing...")
        self.cap = cv2.VideoCapture(self.video_path)
        self.running = True
        self.start_time = datetime.now()
        self.license_plates = set()
        self.update_frame()

    def update_frame(self):
        """Update the video frame on the canvas."""
        if not self.running:
            return

        ret, frame = self.cap.read()
        if ret:
            # Perform YOLO detection
            results = model.predict(frame, conf=0.45)
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    label = self.paddle_ocr(frame, x1, y1, x2, y2)
                    if label:
                        self.license_plates.add(label)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Convert frame to PIL image and display on canvas
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.imgtk = imgtk

            # Log to database every 20 seconds
            current_time = datetime.now()
            if (current_time - self.start_time).seconds >= 20:
                self.save_to_database(self.license_plates, self.start_time, current_time)
                self.start_time = current_time
                self.license_plates.clear()

            # Schedule the next frame update
            self.root.after(10, self.update_frame)
        else:
            self.log_message("Processing completed.")
            self.cap.release()
            self.running = False

    def paddle_ocr(self, frame, x1, y1, x2, y2):
        """Perform OCR on a detected license plate."""
        frame = frame[y1:y2, x1:x2]
        result = ocr.ocr(frame, det=False, rec=True, cls=False)
        text = ""
        for r in result:
            scores = r[0][1]
            if np.isnan(scores):
                scores = 0
            else:
                scores = int(scores * 100)
            if scores > 60:
                text = r[0][0]
        pattern = re.compile('[\W]')
        text = pattern.sub('', text)
        text = text.replace("???", "").replace("O", "0").replace("粤", "")
        return str(text)

    def save_to_database(self, license_plates, start_time, end_time):
        """Save license plates to the SQL database and update the GUI table."""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="licensePlatedb"
            )
            cursor = conn.cursor()
            for plate in license_plates:
                cursor.execute(
                    '''
                    INSERT INTO LicensePlates (start_time, end_time, license_plate)
                    VALUES (%s, %s, %s)
                    ''', (start_time.isoformat(), end_time.isoformat(), plate)
                )
                # Update the GUI table
                self.update_table(start_time.isoformat(), end_time.isoformat(), plate)
            conn.commit()
            conn.close()
            self.log_message(f"Data saved: {license_plates}")
        except mysql.connector.Error as e:
            self.log_message(f"Database Error: {e}")

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = LicensePlateApp(root)
    root.mainloop()
