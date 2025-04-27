import tkinter as tk
from tkinter import messagebox, filedialog
import os
import cv2
import face_recognition
import numpy as np
import csv
from datetime import datetime
import pandas as pd


def register_face(name, save_path='dataset'):
    cam = cv2.VideoCapture(0)
    messagebox.showinfo("Info", f"Capturing face for: {name}. Press 'q' to take photo.")

    while True:
        ret, frame = cam.read()
        if not ret:
            messagebox.showerror("Error", "Failed to access webcam.")
            break

        cv2.imshow("Register Face", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            face_locations = face_recognition.face_locations(frame)
            if face_locations:
                encoding = face_recognition.face_encodings(frame, face_locations)[0]

                os.makedirs(save_path, exist_ok=True)
                np.save(f"{save_path}/{name}.npy", encoding)

                messagebox.showinfo("Success", f"Face saved for: {name}")
                break
            else:
                messagebox.showinfo("Info", "No face found. Try again.")

    cam.release()
    cv2.destroyAllWindows()

def delete_face(name, dataset_path='dataset'):
    filepath = os.path.join(dataset_path, f"{name}.npy")
    if os.path.exists(filepath):
        os.remove(filepath)
        messagebox.showinfo("Deleted", f"{name}'s face data has been deleted.")
    else:
        messagebox.showerror("Not Found", f"{name}.npy not found in dataset.")

def open_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        top = tk.Toplevel()
        top.title(f"Attendance - {os.path.basename(file_path)}")
        top.configure(bg="#1e1e1e")

        text = tk.Text(top, wrap=tk.WORD, width=100, height=30, bg="#2e2e2e", fg="white", insertbackground="white")
        text.pack(padx=10, pady=10)

        text.insert(tk.END, df.to_string(index=False))




# Main GUI Window
root = tk.Tk()






# After splash screen, set up the main window
root.title("Smart Presence Admin Panel")
root.geometry("600x500")
root.configure(bg="#1e1e1e")
root.iconbitmap('C:\\Users\\MOHD ASHHAD\\smart_presence\\layout_icon_264862.ico')


# Style variables
label_style = {"bg": "#1e1e1e", "fg": "white", "font": ("Helvetica", 12)}
entry_style = {"bg": "#2e2e2e", "fg": "white", "insertbackground": "white", "font": ("Helvetica", 11)}
button_style = {"bg": "#333", "fg": "white", "font": ("Helvetica", 11, "bold"), "activebackground": "#444"}

# Widgets
title = tk.Label(root, text="Smart Presence Admin", font=("Helvetica", 18, "bold"), bg="#1e1e1e", fg="#00ffcc")
title.pack(pady=20)

entry_label = tk.Label(root, text="Student/Employee Name:", **label_style)
entry_label.pack()

name_entry = tk.Entry(root, **entry_style)
name_entry.pack(pady=10, ipadx=20, ipady=5)

def on_register():
    name = name_entry.get().strip().replace(" ", "_")
    if name:
        register_face(name)
    else:
        messagebox.showwarning("Input Error", "Please enter a valid name.")

def on_delete():
    name = name_entry.get().strip().replace(" ", "_")
    if name:
        delete_face(name)
    else:
        messagebox.showwarning("Input Error", "Please enter a valid name.")

def on_enter(event):
    event.widget.config(bg="#444")  # Change the button color when the mouse enters

def on_leave(event):
    event.widget.config(bg="#333")


register_button = tk.Button(root, text="Register Face", command=on_register, width=20, **button_style)
register_button.pack(pady=10)

delete_button = tk.Button(root, text="Delete Face", command=on_delete, width=20, **button_style)
delete_button.pack(pady=5)

csv_button = tk.Button(root, text="Open Attendance CSV", command=open_csv, width=20, **button_style)
csv_button.pack(pady=30)

register_button.bind("<Enter>", on_enter)
register_button.bind("<Leave>", on_leave)

delete_button.bind("<Enter>", on_enter)
delete_button.bind("<Leave>", on_leave)

csv_button.bind("<Enter>", on_enter)
csv_button.bind("<Leave>", on_leave)

root.mainloop()
