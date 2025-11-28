import PyInstaller.__main__
import os

def build_exe():
    print("Building executable...")
    
    PyInstaller.__main__.run([
        'YouTubeVideoDownloader.py',
        '--onefile',
        '--noconsole',
        '--name=YouTube Downloader',
        '--clean',
        '--collect-all=customtkinter',  # Important for customtkinter to work in exe
    ])
    
    print("Build complete! Check the 'dist' folder.")

if __name__ == "__main__":
    build_exe()
