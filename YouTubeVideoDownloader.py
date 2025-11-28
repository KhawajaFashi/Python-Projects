import customtkinter as ctk
from pytubefix import YouTube
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import subprocess
import imageio_ffmpeg
import re

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
        self.yt_object = None
        self.resolutions = []
        self.resolution_sizes = {} # Store sizes for each resolution

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
            command=self.update_size_label,
            state="disabled"
        )
        self.res_option_menu.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")
        
        self.size_label = ctk.CTkLabel(self.options_frame, text="", text_color="gray", font=("Roboto", 12))
        self.size_label.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="w")

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
            text_color="white",  # Explicitly set text color
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
            
            # Get streams - Remove file_extension filter to get 4K/WebM
            streams = self.yt_object.streams.filter(progressive=False)
            self.resolutions = sorted(list(set([stream.resolution for stream in streams if stream.resolution])), key=lambda x: int(x[:-1]) if x[:-1].isdigit() else 0, reverse=True)
            
            if not self.resolutions:
                 raise Exception("No suitable streams found")

            # Calculate sizes for each resolution
            self.resolution_sizes = {}
            audio_stream = self.yt_object.streams.get_audio_only()
            audio_size = audio_stream.filesize if audio_stream else 0
            
            for res in self.resolutions:
                # Try to find adaptive video stream first
                video_stream = self.yt_object.streams.filter(res=res, adaptive=True).first()
                if video_stream:
                    self.resolution_sizes[res] = video_stream.filesize + audio_size
                else:
                    # Fallback to progressive
                    prog_stream = self.yt_object.streams.filter(res=res, progressive=True).first()
                    if prog_stream:
                        self.resolution_sizes[res] = prog_stream.filesize
                    else:
                        self.resolution_sizes[res] = 0 # Unknown

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
            self.update_size_label(self.resolutions[0])
            self.download_btn.configure(state="normal")
            self.status_label.configure(text="Video found! Select resolution and download.", text_color="#2CC985")
        else:
            self.video_title_label.configure(text="")
            self.res_option_menu.configure(values=["Error"], state="disabled")
            self.download_btn.configure(state="disabled")
            self.status_label.configure(text=f"Error: {error_msg}", text_color="#FF5555")

    def update_size_label(self, choice):
        size_bytes = self.resolution_sizes.get(choice, 0)
        if size_bytes > 0:
            size_mb = size_bytes / (1024 * 1024)
            self.size_label.configure(text=f"Est. Size: {size_mb:.1f} MB")
        else:
            self.size_label.configure(text="Size: Unknown")

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

    def sanitize_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

    def download_video(self):
        try:
            res = self.resolution_var.get()
            output_path = self.save_dir_var.get()
            
            # Get the video stream
            video_stream = self.yt_object.streams.filter(res=res, adaptive=True).first()
            if not video_stream:
                # Fallback to progressive if adaptive not found (usually for lower res)
                video_stream = self.yt_object.streams.filter(res=res, progressive=True).first()
            
            if not video_stream:
                 # Fallback if exact match fails
                 video_stream = self.yt_object.streams.filter(res=res).first()

            if not video_stream:
                raise Exception("Stream not found")

            # Check if the stream is adaptive (video only)
            if video_stream.is_adaptive:
                self.status_label.configure(text="Downloading Video Stream...", text_color="white")
                
                # Sanitize filenames
                safe_title = self.sanitize_filename(video_stream.default_filename)
                video_filename = f"temp_video_{safe_title}"
                audio_filename = f"temp_audio_{safe_title}"
                
                # Force output to be .mp4 to support both VP9 (from WebM) and AAC (from audio)
                # WebM container does not support AAC audio.
                final_filename = os.path.splitext(safe_title)[0] + ".mp4"
                
                # Download with explicit filenames
                video_stream.download(output_path=output_path, filename=video_filename)
                
                self.status_label.configure(text="Downloading Audio Stream...", text_color="white")
                audio_stream = self.yt_object.streams.get_audio_only()
                audio_stream.download(output_path=output_path, filename=audio_filename)
                
                self.status_label.configure(text="Merging Video and Audio...", text_color="white")
                
                # Normalize paths to handle mixed slashes and ensure compatibility
                video_path = os.path.normpath(os.path.join(output_path, video_filename))
                audio_path = os.path.normpath(os.path.join(output_path, audio_filename))
                final_path = os.path.normpath(os.path.join(output_path, final_filename))
                
                # Use imageio-ffmpeg to get the ffmpeg executable path
                ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                
                # Merge using ffmpeg
                cmd = [
                    ffmpeg_exe, '-y',
                    '-i', video_path,
                    '-i', audio_path,
                    '-c:v', 'copy',
                    '-c:a', 'aac',
                    final_path
                ]
                
                # Run ffmpeg and capture output
                try:
                    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                except subprocess.CalledProcessError as e:
                    # If ffmpeg fails, raise an exception with the stderr output
                    raise Exception(f"FFmpeg failed: {e.stderr}")
                
                # Cleanup temp files
                if os.path.exists(video_path):
                    os.remove(video_path)
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                
            else:
                # Progressive stream (has audio and video)
                video_stream.download(output_path=output_path)

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
