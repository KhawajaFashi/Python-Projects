from pytubefix import YouTube
import os
import re
import imageio_ffmpeg
import subprocess

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

url = "https://www.youtube.com/watch?v=4Jmeg6nK0Y8"
output_path = "d:\\Fashi Work\\Python\\Python-Projects"

print(f"Processing: {url}")
yt = YouTube(url)
print(f"Title: {yt.title}")

# Simulate the app's logic
res = "1440p"
video_stream = yt.streams.filter(res=res, adaptive=True).first()
if not video_stream:
    print("1440p not found, trying 1080p")
    video_stream = yt.streams.filter(res="1080p", adaptive=True).first()

if video_stream:
    print(f"Found video stream: {video_stream}")
    print(f"Default filename: {video_stream.default_filename}")
    
    safe_title = sanitize_filename(video_stream.default_filename)
    print(f"Safe title: {safe_title}")
    
    video_filename = f"temp_video_{safe_title}"
    audio_filename = f"temp_audio_{safe_title}"
    final_filename = os.path.splitext(safe_title)[0] + ".mp4"
    
    video_path = os.path.join(output_path, video_filename)
    audio_path = os.path.join(output_path, audio_filename)
    final_path = os.path.join(output_path, final_filename)
    
    print("Downloading video...")
    video_stream.download(output_path=output_path, filename=video_filename)
    
    print("Downloading audio...")
    audio_stream = yt.streams.get_audio_only()
    audio_stream.download(output_path=output_path, filename=audio_filename)
    
    print("Merging...")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe, '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        final_path
    ]
    
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Merge successful!")
    except subprocess.CalledProcessError as e:
        print("Merge failed!")
        print("STDERR:", e.stderr)
else:
    print("No video stream found")
