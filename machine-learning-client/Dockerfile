FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

RUN pip install --no-cache-dir -r requirements.txt

# Install FLAC
RUN apt-get update && apt-get install -y flac

# Make Directory for audio storage
RUN mkdir -p /audio_files

COPY . .

EXPOSE 5000

CMD ["python", "./app.py"]