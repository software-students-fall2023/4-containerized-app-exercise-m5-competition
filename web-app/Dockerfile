FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

# Install PulseAudio related packages
RUN apt-get update && apt-get install -y \
    vorbis-tools \
    sox \
    alsa-utils \
    libasound2 \
    portaudio19-dev \
    libasound2-plugins \
    pulseaudio \
    pulseaudio-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*


# Install any needed packages specified in requirements.txt
RUN pipenv install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Start the PulseAudio server in the background
CMD pulseaudio --start && python app.py