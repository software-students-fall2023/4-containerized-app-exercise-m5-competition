import subprocess

subprocess.run(["ffmpeg", "-i", "kids_are_talking.wav", "-c:a", "libvorbis", "kids_are_talking.webm"])