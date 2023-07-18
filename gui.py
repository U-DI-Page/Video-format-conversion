import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from threading import Thread

def convert_videos(input_path):
    output_folder = os.path.join(input_path, "outputs")
    os.makedirs(output_folder, exist_ok=True)

    info_label.config(text="Converting videos...\n")
    progress_bar["value"] = 0

    error_files = []
    video_files = [video_file for video_file in os.listdir(input_path) if video_file.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))]
    total_files = len(video_files)

    for i, video_file in enumerate(video_files, start=1):
        input_file_path = os.path.join(input_path, video_file)
        output_file_path = os.path.join(output_folder, f"{os.path.splitext(video_file)[0]}.mp4")
        command = f"ffmpeg -i \"{input_file_path}\" -c:v libx264 -preset medium -crf 23 \"{output_file_path}\""

        try:
            subprocess.run(command, check=True, shell=True)
            message = f"Converted {video_file} successfully\n"
        except subprocess.CalledProcessError as e:
            error_files.append(video_file)
            message = f"Failed to convert {video_file}: {e}\n"

        progress = int((i / total_files) * 100)
        progress_bar["value"] = progress
        root.update_idletasks()

        print(message)
        info_label.config(text=info_label.cget("text") + message)

    if error_files:
        error_message = "Errors occurred during conversion for the following files:\n"
        for error_file in error_files:
            error_message += f"- {error_file}\n"
        print(error_message)
        info_label.config(text=info_label.cget("text") + error_message)

    info_label.config(text=info_label.cget("text") + "Conversion completed. Check the 'outputs' folder.\n")
    progress_bar["value"] = 100

def open_directory():
    input_path = filedialog.askdirectory()
    if input_path:
        # Run the conversion in a separate thread
        conversion_thread = Thread(target=convert_videos, args=(input_path,))
        conversion_thread.start()

root = tk.Tk()
root.title("Video Format Converter")
root.geometry("400x250")

open_button = tk.Button(root, text="Open Directory", command=open_directory)
open_button.pack(pady=20)

progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
progress_bar.pack()

info_label = tk.Label(root, text="")
info_label.pack()

root.mainloop()
