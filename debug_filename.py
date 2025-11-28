from pytubefix import YouTube

url = "https://youtu.be/zm6xa3ggt5A"
yt = YouTube(url)
print(f"Title: {yt.title}")
stream = yt.streams.filter(progressive=False).first()
print(f"Default Filename: {stream.default_filename}")

import os
# Check if default_filename is valid on Windows
invalid_chars = '<>:"/\|?*'
is_valid = not any(char in stream.default_filename for char in invalid_chars)
print(f"Is valid Windows filename: {is_valid}")
