import os
import numpy as np
import face_recognition

def load_registered_faces(path='dataset'):
    known_encodings = []
    known_names = []

    for file in os.listdir(path):
        if file.endswith('.npy'):
            encoding = np.load(os.path.join(path, file))
            known_encodings.append(encoding)
            known_names.append(file.replace('.npy', ''))

    return known_encodings, known_names


import cv2
from collections import defaultdict
import time

def capture_and_track_attendance(interval=120, total_images=30):
    known_encodings, known_names = load_registered_faces()
    attendance_counter = defaultdict(int)
    
    cam = cv2.VideoCapture(0)
    print("[INFO] Starting image capture...")

    for i in range(total_images):
        ret, frame = cam.read()
        if not ret:
            print("[ERROR] Failed to capture frame.")
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            if True in matches:
                matched_idx = matches.index(True)
                name = known_names[matched_idx]
                attendance_counter[name] += 1
                print(f"[MATCH] {name} detected ({attendance_counter[name]} times)")

        time.sleep(interval)  # wait between captures

    cam.release()
    return attendance_counter, total_images

import csv
from datetime import datetime

def calculate_final_attendance(attendance_counter, total_images, threshold_percent=60, period_name="Period_1"):
    threshold_count = (threshold_percent / 100) * total_images
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"attendance_{date_str}.csv"

    # Write headers if file doesn't exist
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Period", "Name", "Status", "Match_Count", "Total_Frames"])

        for name, count in attendance_counter.items():
            status = "Present" if count >= threshold_count else "Absent"
            writer.writerow([date_str, period_name, name, status, count, total_images])

    print(f"\n[SAVED] Attendance written to {filename}")



if __name__ == "__main__":
    counter, total = capture_and_track_attendance(interval=5, total_images=10)
    calculate_final_attendance(counter, total, period_name="Morning_Session")

