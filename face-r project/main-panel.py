import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import os

def run_main():
    os.system("python main.py")

def run_registration():
    root.destroy()
    os.system("python fold/reg.py")

root = tk.Tk()
root.title("Face Recognition using Python")

window_width = 600
window_height = 400
root.geometry(f"{window_width}x{window_height}")
root.configure(bg="#F5F5DC")
root.minsize(window_width, window_height)

top_frame = tk.Frame(root, bg="#12CEEB", padx=10, pady=10)
top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

left_frame = tk.Frame(root, bg="#96CEEB", padx=10, pady=10)
left_frame.grid(row=1, column=0, sticky="nsew")

right_frame = tk.Frame(root, bg="#FFA97A", padx=10, pady=10)
right_frame.grid(row=1, column=1, sticky="nsew")

top_title_label = ttk.Label(top_frame, text="Face Recognition using Python", font=("Helvetica", 16), background="#12CEEB")
top_title_label.pack()

left_title_label = ttk.Label(left_frame, text="Face Recognition", font=("Helvetica", 14), background="#96CEEB")
left_title_label.grid(row=0, column=0, pady=10)

left_button = ttk.Button(left_frame, text="Open", command=run_main)
left_button.grid(row=1, column=0, pady=10)

img_left = Image.open('Resources/fr.jpeg')
img_left = img_left.resize((200, 200), Image.ANTIALIAS)
img_left = ImageTk.PhotoImage(img_left)
left_img_label = tk.Label(left_frame, image=img_left, bg="#96CEEB")
left_img_label.grid(row=2, column=0, pady=10)

right_title_label = ttk.Label(right_frame, text="Add New Member", font=("Helvetica", 14), background="#FFA97A")
right_title_label.grid(row=0, column=0, pady=10)

right_button = ttk.Button(right_frame, text="Open", command=run_registration)
right_button.grid(row=1, column=0, pady=10)

img_right = Image.open('Resources/adding.jpeg')
img_right = img_right.resize((200, 200), Image.ANTIALIAS)
img_right = ImageTk.PhotoImage(img_right)
right_img_label = tk.Label(right_frame, image=img_right, bg="#FFA97A")
right_img_label.grid(row=2, column=0, pady=10)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()
