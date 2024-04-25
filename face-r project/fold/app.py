import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk

import cv2
import os
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-48233-default-rtdb.firebaseio.com/",
    'storageBucket': "face-48233.appspot.com"
})
ref = db.reference('Students')

# Create Images directory if it doesn't exist
images_dir = "old"
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Function to register student
def register_student():
    global images_dir  # Make images_dir a global variable
    # Get student details from entry fields
    student_id = student_id_entry.get()
    name = name_entry.get()
    branch = branch_entry.get()
    starting_year = starting_year_entry.get()
    total_attendance = total_attendance_entry.get()
    status = status_entry.get()
    year = year_entry.get()
    last_attendance_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if any field is empty
    if not (student_id and name and branch and starting_year and total_attendance and status and year):
        messagebox.showerror("Error", "Please fill in all fields")
        return

    # Save student data to Firebase
    student_data = {
        "name": name,
        "branch": branch,
        "starting_year": starting_year,
        "total_attendance": total_attendance,
        "status": status,
        "year": year,
        "last_attendance_time": last_attendance_time
    }
    ref.child(student_id).set(student_data)

    # Save student image if path is set
    if image_path:
        image = Image.open(image_path)
        image.save(os.path.join(images_dir, f"{student_id}.png"))

    # Show success message
    messagebox.showinfo("Success", "Student registered successfully")
    clear_inputs()  # Clear inputs after registering

# Function to clear input fields and reset image display
def clear_inputs():
    # Clear entry fields
    for entry_field in entry_fields:
        entry_field.delete(0, 'end')
    
    # Clear image label
    image_label.config(image=None)

# Function to browse image
def browse_image():
    global image_path
    student_id = student_id_entry.get()
    if not student_id:
        messagebox.showerror("Error", "Please enter a Student ID before capturing an image")
        return
    file_path = filedialog.askopenfilename()
    if file_path:
        image_path = file_path
        if image_path.lower().endswith(('.jpg', '.jpeg')):
            # Convert JPG image to PNG with resize (240, 240)
            image = Image.open(image_path)
            image = image.resize((240, 240))
            image_path = os.path.join(images_dir, f"{student_id_entry.get()}.png")
            image.save(image_path, format="PNG")
        else:
            # Open image directly
            image = Image.open(image_path)
            image = image.resize((240, 240))
        display_image(image)

# Function to capture image
def capture_image():
    global image_path
    student_id = student_id_entry.get()
    if not student_id:
        messagebox.showerror("Error", "Please enter a Student ID before capturing an image")
        return
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (240, 240))
        image = Image.fromarray(frame)
        image_path = f"{images_dir}/{student_id}.png"
        image.save(image_path)
        display_image(image)

# Function to display image on label
def display_image(image):
    image = image.resize((240, 240), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

# Create a Tkinter window
root = tk.Tk()
root.title("Student Registration")
root.geometry("500x600")  # Set window size

# Set background color
root.configure(bg="#F5F5DC")

# Create title label at top center
title_label = tk.Label(root, text="Student Registration", font=("Helvetica", 16), bg="#F5F5DC")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create labels and entry fields
labels = ["Student ID:", "Name:", "Branch:", "Starting Year:", "Total Attendance:", "Status:", "Year:"]
entry_fields = []

for i, label_text in enumerate(labels):
    label = tk.Label(root, text=label_text, bg="#F5F5DC")
    label.grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
    
    # For Status and Year fields, use OptionMenu
    if label_text == "Status:":
        status_var = tk.StringVar(root)
        status_var.set("Student")  # Default value
        status_menu = ttk.OptionMenu(root, status_var,"select", "Student", "Teacher")
        status_menu.grid(row=i+1, column=1, padx=10, pady=5, sticky="ew")
        entry_fields.append(status_var)
    elif label_text == "Year:":
        year_var = tk.StringVar(root)
        year_var.set("1st")  # Default value
        year_menu = ttk.OptionMenu(root, year_var, "select","1st", "2nd", "3rd", "4th")
        year_menu.grid(row=i+1, column=1, padx=10, pady=5, sticky="ew")
        entry_fields.append(year_var)
    else:
        entry_field = tk.Entry(root)
        entry_field.grid(row=i+1, column=1, padx=10, pady=5)
        entry_fields.append(entry_field)

# Retrieve individual entry fields
student_id_entry, name_entry, branch_entry, starting_year_entry, total_attendance_entry, status_entry, year_entry = entry_fields

# Add Last Attendance Time label
tk.Label(root, text="Last Attendance Time:", bg="#F5F5DC").grid(row=len(labels)+1, column=0, padx=10, pady=5, sticky="w")

# Add entry field for Last Attendance Time
last_attendance_time_entry = tk.Entry(root)
last_attendance_time_entry.grid(row=len(labels)+1, column=1, padx=10, pady=5)
last_attendance_time_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Create a button to register the student
register_button = tk.Button(root, text="Register", command=register_student)
register_button.grid(row=len(labels)+2, column=0, columnspan=2, padx=10, pady=10)

# Create buttons to browse and capture image
browse_button = tk.Button(root, text="Browse Image", command=browse_image)
browse_button.grid(row=len(labels)+3, column=0, padx=10, pady=5)

capture_button = tk.Button(root, text="Capture Image", command=capture_image)
capture_button.grid(row=len(labels)+3, column=1, padx=10, pady=5)

# Create button to clear inputs
clear_button = tk.Button(root, text="Restart", command=clear_inputs)
clear_button.grid(row=len(labels)+4, column=0, columnspan=2, padx=10, pady=10)

# Create label to display the image
image_label = tk.Label(root)
image_label.grid(row=len(labels)+5, column=0, columnspan=2, padx=10, pady=5)

# Run the Tkinter event loop
root.mainloop()
