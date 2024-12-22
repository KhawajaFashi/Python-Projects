from pytubefix import YouTube
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter import font

# Global colors
background_color = "gray"
button_background_color = "dim gray"
foreground_color = "white"
URL_save = None


def get_video(url, root):

    yt = YouTube(url)
    return yt


def extract_resolution(url, root):
    try:
        yt = get_video(url, root)
        streams = yt.streams.filter(progressive=False, file_extension="mp4")
        resolutions = [stream.resolution for stream in streams if stream.resolution]
        resolutions = list(set(resolutions))
        resolutions.sort(key=lambda x: (len(x), x))
        print("\nVideo was successfully found!\n")
        return resolutions
    except Exception as e:
        print(f"Error: {e}")
        return ["Invalid URL or No Resolutions Found"]


def getUrl(root):
    custom_font = font.Font(
        family="Arial",
        size=16,
        weight="bold",
    )
    Label(
        root,
        text="Enter your YouTube URL: ",
        padx=20,
        bg=background_color,
        fg=foreground_color,
        font=custom_font,
    ).grid(row=1, columnspan=1)
    url_var = tk.StringVar()
    urlEntry = tk.Entry(root, textvariable=url_var, width=40, font=custom_font)
    urlEntry.grid(row=1, column=1)
    return url_var


def Downloading_Interface(root, save_dir, resolution):

    progress_label = tk.Label(
        root, text="Progress will appear here.", font=("Arial", 14, "bold")
    )
    progress_label.grid(row=9, column=1)

    progress_bar = ttk.Progressbar(
        root, orient="horizontal", length=300, mode="determinate"
    )
    progress_bar.grid(row=10, column=1, pady=25)

    def progress_function(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        total_size_mb = total_size / (1024 * 1024)
        bytes_downloaded_mb = bytes_downloaded / (1024 * 1024)
        percentage = (bytes_downloaded_mb / total_size_mb) * 100

        if total_size_mb > 1000:
            progress_text = f"Downloaded: {(bytes_downloaded_mb / 1024):.2f} / {(total_size_mb / 1024):.2f} GB ({percentage:.2f}%)"
        else:
            progress_text = f"Downloaded: {bytes_downloaded_mb:.2f} / {total_size_mb:.2f} MB ({percentage:.2f}%)"

        progress_label.config(text=progress_text)
        progress_bar["value"] = percentage
        root.update_idletasks()

    download_btn = tk.Button(
        root,
        text="Start Download",
        fg=foreground_color,
        bg=background_color,
        font=("Arial", 16, "bold"),
    )
    download_btn.grid(row=8, column=1, columnspan=1, pady=25)

    def Download_video(event=None):
        try:
            yt = YouTube(URL_save, on_progress_callback=progress_function)
            print(f"Video Title: {yt.title}")
            streams = yt.streams.filter(progressive=False, file_extension="mp4")
            if streams:
                highest_res_stream = streams.filter(
                    "", resolution
                ).get_highest_resolution(False)
                if highest_res_stream:
                    highest_res_stream.download(output_path=save_dir)
                    print("\nVideo Downloaded Successfully")
                else:
                    print("\nNo suitable stream found")
            else:
                print("\nNo streams found")
        except Exception as error:
            print(f"\nError: {error}")

    try:
        download_btn.bind("<Button-1>", Download_video)
    except Exception as e:
        print(e)


def main_Interface(root):
    custom_font = font.Font(
        family="Arial",
        size=16,
        weight="bold",
    )

    def open_file_dialog(event=None):
        folder = filedialog.askdirectory()
        if folder:
            save_dir_var.set(folder)
            print(f"Selected Folder: {folder}")
        return folder

    def selectResolution(event=None):
        resolution = combobox_var.get()
        if resolution:
            print(f"Selected Resolutio: {resolution}")
            return resolution

    def update_combobox():
        url = url_var.get()
        global URL_save
        URL_save = url
        if url:
            resolutions = extract_resolution(url, root)
            combobox_var.set("")
            combobox["values"] = resolutions
        else:
            combobox_var.set("")
            combobox["values"] = ["Enter a valid URL first"]

    def use_selected_value(event=None):
        resolution = combobox_var.get()
        folder = save_dir_var.get()
        try:
            yt = get_video(URL_save, root)
            Label(
                root,
                text=yt.title,
                fg=foreground_color,
                bg=background_color,
                font=("Arial", 12, "bold"),
                wraplength=250,
            ).grid(row=7, column=0)
        except Exception as e:
            print(f"Error: {e}")
        Label(
            root,
            text=folder,
            fg=foreground_color,
            bg=background_color,
            wraplength=250,
            font=("Arial", 12, "bold"),
        ).grid(row=7, column=1)
        Label(
            root,
            text=resolution,
            fg=foreground_color,
            bg=background_color,
            font=("Arial", 12, "bold"),
        ).grid(row=7, column=2)
        Downloading_Interface(root, folder, resolution)

    combobox_var = tk.StringVar()
    save_dir_var = tk.StringVar(value="")
    Label(
        root,
        text="Welcome to YouTube Video Downloader!",
        padx=200,
        pady=50,
        font=("Arial", 26, "bold"),
        fg=foreground_color,
        bg=background_color,
    ).grid(row=0, columnspan=15)

    url_var = getUrl(root)
    tk.Button(
        root,
        text="Get Video",
        command=update_combobox,
        bg=button_background_color,
        font=("Arial", 11, "bold"),
    ).grid(row=1, column=2, padx=18, columnspan=1)

    Label(
        root,
        text="Select the resolution: ",
        # padx=342,
        fg=foreground_color,
        bg=background_color,
        font=custom_font,
    ).grid(row=3, column=0, columnspan=1)

    combobox = ttk.Combobox(
        root,
        textvariable=combobox_var,
        values=["Enter the URL first"],
        width=30,
        font=custom_font,
    )
    combobox.grid(row=3, column=1, pady=35, padx=23)

    use_button = tk.Button(
        root,
        text="Get Resolution and Folder",
        bg=button_background_color,
        font=("Arial", 11, "bold"),
    )
    use_button.grid(row=6, column=1, columnspan=1, pady=20)

    use_button.bind("<Button-1>", use_selected_value)

    select_resolution_button = tk.Button(
        root,
        text="Select Resolution",
        bg=button_background_color,
        font=("Arial", 11, "bold"),
    )
    select_resolution_button.grid(row=3, column=2, columnspan=1)

    select_resolution_button.bind("<Button-1>", selectResolution)

    select_folder_button = tk.Button(
        root,
        text="Select Folder",
        bg=button_background_color,
        font=("Arial", 11, "bold"),
    )
    select_folder_button.grid(row=5, column=1, pady=2)

    select_folder_button.bind("<Button-1>", open_file_dialog)


def main():
    print("Welcome to YouTube Video Downloader")
    root = tk.Tk()
    root.geometry("1000x630")
    root.title("YouTube Video Download")
    root.config(bg=background_color)
    main_Interface(root)
    root.mainloop()

main()
