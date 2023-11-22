"""simple audio recognition and analysis client"""

import speech_recognition as sr
from textblob import TextBlob


def transcribe_audio(file_path):
    """transcribe the given audio file"""
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text


def analyze_sentiment(text):
    """sentiment analysis"""
    analysis = TextBlob(text)
    return analysis.sentiment
