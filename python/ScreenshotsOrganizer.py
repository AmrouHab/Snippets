import os
import shutil
import re
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import tkinter as tk
from tkinter import filedialog, messagebox

def get_exif_date_taken(filepath):
    """Extract date taken from image EXIF data if available."""
    try:
        image = Image.open(filepath)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == "DateTimeOriginal":
                    dt = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    return dt.strftime("%Y"), dt.strftime("%m")
    except Exception:
        pass
    return None, None

def get_date_from_filename_or_metadata(filename, source_folder):
    """Extract date information from filename or file metadata."""
    windows_pattern = re.compile(r"Screenshot (\d{4})-(\d{2})-(\d{2})")
    sharex_pattern = re.compile(r"(\d{4})-(\d{2})")
    
    windows_match = windows_pattern.search(filename)
    if windows_match:
        return windows_match.group(1), windows_match.group(2)  # YYYY, MM
    
    sharex_match = sharex_pattern.search(filename)
    if sharex_match:
        return sharex_match.group(1), sharex_match.group(2)  # YYYY, MM
    
    file_path = os.path.join(source_folder, filename)
    year, month = get_exif_date_taken(file_path)
    if year and month:
        return year, month
    
    try:
        modified_time = os.path.getmtime(file_path)
        dt = datetime.fromtimestamp(modified_time)
        return dt.strftime("%Y"), dt.strftime("%m")
    except Exception:
        return None, None

def organize_screenshots(source_folder, destination_folder):
    """Organize screenshots into Year/Month folders."""
    if not os.path.exists(source_folder) or not os.path.exists(destination_folder):
        messagebox.showerror("Error", "Invalid source or destination folder!")
        return
    
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            year, month = get_date_from_filename_or_metadata(filename, source_folder)
            if year and month:
                year_folder = os.path.join(destination_folder, year)
                month_folder = os.path.join(year_folder, month)
                os.makedirs(month_folder, exist_ok=True)
                shutil.move(os.path.join(source_folder, filename), os.path.join(month_folder, filename))
    
    messagebox.showinfo("Success", "Organization complete!")

def select_source_folder():
    folder = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, folder)

def select_destination_folder():
    folder = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, folder)

def start_organization():
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    organize_screenshots(source_folder, destination_folder)

# Create UI
root = tk.Tk()
root.title("Ampy - Screenshot Organizer")
root.geometry("400x200")

tk.Label(root, text="Source Folder:").pack()
source_entry = tk.Entry(root, width=50)
source_entry.pack()
tk.Button(root, text="Browse", command=select_source_folder).pack()

tk.Label(root, text="Destination Folder:").pack()
destination_entry = tk.Entry(root, width=50)
destination_entry.pack()
tk.Button(root, text="Browse", command=select_destination_folder).pack()

tk.Button(root, text="Start", command=start_organization).pack()

root.mainloop()
