FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

# Install ffmpeg for format conversion
RUN apt-get update && apt-get install -y ffmpeg

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install FLAC
RUN apt-get update && apt-get install -y flac

COPY . .

EXPOSE 5000

CMD ["python", "./app.py"]