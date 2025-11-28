import customtkinter as ctk
from pytubefix import YouTube
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os

# Set theme and color palette
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("YouTube Video Downloader")
        self.geometry("800x600")
        self.resizable(False, False)

        # Variables
        self.url_var = tk.StringVar()
        self.save_dir_var = tk.StringVar()
        self.resolution_var = tk.StringVar()
        self.yt_object = None
        self.resolutions = []

        # Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=0) # URL Input
        self.grid_rowconfigure(2, weight=0) # Video Info
        self.grid_rowconfigure(3, weight=0) # Options
        self.grid_rowconfigure(4, weight=0) # Progress
        self.grid_rowconfigure(5, weight=1) # Spacer

        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="YouTube Video Downloader", 
            font=("Roboto", 28, "bold"),
            text_color="#3B8ED0"
        )
        self.title_label.grid(row=0, column=0, pady=(30, 20), sticky="ew")

        # URL Input Frame
        self.url_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.url_frame.grid(row=1, column=0, padx=40, pady=10, sticky="ew")
        self.url_frame.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(
            self.url_frame, 
            textvariable=self.url_var,
            placeholder_text="Paste YouTube URL here...",
            height=40,
            font=("Roboto", 14)
        )
        self.url_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.fetch_btn = ctk.CTkButton(
            self.url_frame, 
            text="Get Video", 
            command=self.start_fetch_thread,
            height=40,
            font=("Roboto", 14, "bold")
        )
        self.fetch_btn.grid(row=0, column=1, padx=0)

        # Video Info Section (Initially Hidden or Empty)
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.grid(row=2, column=0, padx=40, pady=20, sticky="ew")
        self.info_frame.grid_columnconfigure(0, weight=1)

        self.video_title_label = ctk.CTkLabel(
            self.info_frame, 
            text="", 
            font=("Roboto", 16, "bold"),
            wraplength=700
        )
        self.video_title_label.grid(row=0, column=0, pady=5)

        # Options Frame
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=3, column=0, padx=40, pady=10, sticky="ew")
        self.options_frame.grid_columnconfigure((0, 1), weight=1)

        # Resolution Dropdown
        self.res_label = ctk.CTkLabel(self.options_frame, text="Resolution:", font=("Roboto", 12))
        self.res_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")
        
        self.res_option_menu = ctk.CTkOptionMenu(
            self.options_frame,
            variable=self.resolution_var,
            values=["Fetch Video First"],
            state="disabled"
        )
        self.res_option_menu.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="ew")

        # Save Location
        self.loc_label = ctk.CTkLabel(self.options_frame, text="Save Location:", font=("Roboto", 12))
        self.loc_label.grid(row=0, column=1, padx=20, pady=(15, 0), sticky="w")

        self.loc_btn = ctk.CTkButton(
            self.options_frame,
            text="Select Folder",
            command=self.select_folder,
            fg_color="#555555",
            hover_color="#444444"
        )
        self.loc_btn.grid(row=1, column=1, padx=20, pady=(5, 20), sticky="ew")
        
        self.loc_display = ctk.CTkLabel(self.options_frame, textvariable=self.save_dir_var, text_color="gray", font=("Roboto", 10))
        self.loc_display.grid(row=2, column=1, padx=20, pady=(0, 10), sticky="w")

        # Download Button
        self.download_btn = ctk.CTkButton(
            self, 
            text="Download Video", 
            command=self.start_download_thread,
            height=50,
            font=("Roboto", 18, "bold"),
            fg_color="#2CC985",
            hover_color="#25A970",
            state="disabled"
        )
        self.download_btn.grid(row=4, column=0, padx=40, pady=30, sticky="ew")

        # Progress Section
        self.progress_bar = ctk.CTkProgressBar(self, height=15)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=5, column=0, padx=40, pady=(0, 10), sticky="ew")
        self.progress_bar.grid_remove() # Hide initially

        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_label.grid(row=6, column=0, pady=(0, 20))

    def start_fetch_thread(self):
        url = self.url_var.get()
        if not url:
            self.status_label.configure(text="Please enter a URL", text_color="#FF5555")
            return
        
        self.fetch_btn.configure(state="disabled", text="Fetching...")
        self.status_label.configure(text="Fetching video info...", text_color="white")
        
        threading.Thread(target=self.fetch_video_info, args=(url,), daemon=True).start()

    def fetch_video_info(self, url):
        try:
            self.yt_object = YouTube(url, on_progress_callback=self.on_progress)
            self.yt_object.check_availability()
            
            # Get streams
            streams = self.yt_object.streams.filter(progressive=False, file_extension="mp4")
            self.resolutions = sorted(list(set([stream.resolution for stream in streams if stream.resolution])), key=lambda x: int(x[:-1]) if x[:-1].isdigit() else 0, reverse=True)
            
            if not self.resolutions:
                 raise Exception("No suitable streams found")

            # Update UI in main thread
            self.after(0, self.update_ui_after_fetch, True)
            
        except Exception as e:
            print(f"Error: {e}")
            self.after(0, self.update_ui_after_fetch, False, str(e))

    def update_ui_after_fetch(self, success, error_msg=""):
        self.fetch_btn.configure(state="normal", text="Get Video")
        
        if success:
            self.video_title_label.configure(text=self.yt_object.title)
            self.res_option_menu.configure(values=self.resolutions, state="normal")
            self.res_option_menu.set(self.resolutions[0])
            self.download_btn.configure(state="normal")
            self.status_label.configure(text="Video found! Select resolution and download.", text_color="#2CC985")
        else:
            self.video_title_label.configure(text="")
            self.res_option_menu.configure(values=["Error"], state="disabled")
            self.download_btn.configure(state="disabled")
            self.status_label.configure(text=f"Error: {error_msg}", text_color="#FF5555")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_dir_var.set(folder)

    def start_download_thread(self):
        if not self.save_dir_var.get():
            self.status_label.configure(text="Please select a save location", text_color="#FF5555")
            return

        self.download_btn.configure(state="disabled", text="Downloading...")
        self.progress_bar.grid() # Show progress bar
        self.progress_bar.set(0)
        
        threading.Thread(target=self.download_video, daemon=True).start()

    def download_video(self):
        try:
            res = self.resolution_var.get()
            stream = self.yt_object.streams.filter(res=res, file_extension='mp4').first()
            
            if not stream:
                 # Fallback if exact match fails (rare with filter)
                 stream = self.yt_object.streams.get_highest_resolution()

            stream.download(output_path=self.save_dir_var.get())
            
            self.after(0, self.download_complete, True)
        except Exception as e:
            self.after(0, self.download_complete, False, str(e))

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = bytes_downloaded / total_size
        self.after(0, self.update_progress, percentage, bytes_downloaded, total_size)

    def update_progress(self, val, downloaded, total):
        self.progress_bar.set(val)
        
        # Convert to MB
        downloaded_mb = downloaded / (1024 * 1024)
        total_mb = total / (1024 * 1024)
        remaining_mb = total_mb - downloaded_mb
        
        progress_text = f"Downloading... {int(val*100)}% | {downloaded_mb:.1f}MB / {total_mb:.1f}MB | Remaining: {remaining_mb:.1f}MB"
        self.status_label.configure(text=progress_text, text_color="white")

    def download_complete(self, success, error_msg=""):
        self.download_btn.configure(state="normal", text="Download Video")
        
        if success:
            self.status_label.configure(text="Download Complete! ✅", text_color="#2CC985")
            self.progress_bar.set(1)
            messagebox.showinfo("Success", "Video Downloaded Successfully!")
        else:
            self.status_label.configure(text=f"Download Failed: {error_msg}", text_color="#FF5555")
            self.progress_bar.grid_remove()

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
