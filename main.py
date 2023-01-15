import tkinter as tk
from tkinter import filedialog
import pyttsx3
from PyPDF2 import PdfReader
import docx
import os
import threading

def select_file():
    """Opens filedialog and uploads selected file"""
    global selected_file, name_without_filetype
    filetypes = (("Text files", ".txt"), ("PDF files", ".pdf"), ("Word files", ".docx"), ("all files", "*.*"))
    selected_file = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
    # Gets name of the selected file
    name_with_filetype = os.path.basename(selected_file)
    name_without_filetype = os.path.splitext(name_with_filetype)[0]
    # Shows name of the selected file on screen
    file_label.configure(text=f"File selected: {name_with_filetype}")

def convert_to_mp3():
    """Converts selected file to mp3 and saves it to the current directory"""
    # Get string from file
    if selected_file.endswith(".txt"):
        with open(selected_file, "r") as f:
            file_string = f.read()
    elif selected_file.endswith(".pdf"):
        pdf_string = ""
        reader = PdfReader(selected_file)
        number_of_pages = len(reader.pages)
        for number in range(number_of_pages):
            page = reader.pages[number]
            pdf_string += page.extract_text()
        file_string = pdf_string
    elif selected_file.endswith(".docx"):
        doc = docx.Document(selected_file)
        file_string = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    else:
        file_string = ""
    # Convert string to mp3
    engine = pyttsx3.init()
    engine.save_to_file(file_string, f"{name_without_filetype}.mp3")
    engine.runAndWait()
    file_label.configure(text=f"File converted: {name_without_filetype}.mp3")

# Set up Tkinter GUI window
root = tk.Tk()
root.title("File Converter")
root.geometry("400x200")

# Label
file_label = tk.Label(root, text="File selected: None", font=("Arial", 18))
file_label.pack()

# Buttons
upload_button = tk.Button(root, text="Upload File", command=select_file)
upload_button.pack()
convert_button = tk.Button(root, text="Convert to MP3", command=convert_to_mp3)
convert_button.pack()

root.mainloop()
