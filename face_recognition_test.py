import face_recognition
import cv2

# Load an image (make sure to replace this with an actual image path)
image = face_recognition.load_image_file(r"C:\Users\MOHD ASHHAD\smart_presence\WIN_20250423_20_52_26_Pro.jpg")



# Find all face locations in the image
face_locations = face_recognition.face_locations(image)

# Print how many faces were found
print(f"Found {len(face_locations)} face(s) in this photograph.")
