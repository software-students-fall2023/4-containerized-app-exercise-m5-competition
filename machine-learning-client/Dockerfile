FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y && \
    apt-get install -y libgl1-mesa-glx

RUN pip install torch

RUN pip install easyocr

# Install FLAC
RUN apt-get update && apt-get install -y flac

COPY . .

EXPOSE 5000

CMD ["python", "./app.py"]