"""
This file contains the default values for the machine learning client.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).parent
print(ROOT_DIR)

AUDIO_DIR = Path(os.getenv("AUDIO_DIR") or ROOT_DIR.parent.parent / "audio")
print(AUDIO_DIR)
USER_AUDIO = AUDIO_DIR / "user-audio"
SKETCH_AUDIO = AUDIO_DIR / "user-audio-sketches"