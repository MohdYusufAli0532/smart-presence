import cv2
import face_recognition
import os
import numpy as np



def register_face(name, save_path='dataset'):
    cam = cv2.VideoCapture(0)
    print(f"[INFO] Capturing face for: {name}. Press 'q' to take photo.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("[ERROR] Failed to access webcam.")
            break

        cv2.imshow("Register Face", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            face_locations = face_recognition.face_locations(frame)
            if face_locations:
                encoding = face_recognition.face_encodings(frame, face_locations)[0]

                os.makedirs(save_path, exist_ok=True)
                np.save(f"{save_path}/{name}.npy", encoding)

                print(f"[SUCCESS] Face saved for: {name}")
                break
            else:
                print("[INFO] No face found. Try again...")

    cam.release()
    cv2.destroyAllWindows()

# Usage
if __name__ == "__main__":
    user_name = input("Enter name of student/employee: ").strip().replace(" ", "_")
    register_face(user_name)
