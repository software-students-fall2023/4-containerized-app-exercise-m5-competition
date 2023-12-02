"""
simple audio recognition and analysis client
"""

import speech_recognition as sr
from textblob import TextBlob
from collections import namedtuple

SentimentResult = namedtuple("SentimentResult", ["polarity", "subjectivity"])


def transcribe_audio(file_path):
    """
    Transcribe the given audio file
    """
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            # Handle the case where the recognizer does not understand the audio
            return "N/A"


def analyze_sentiment(text):
    """
    Sentiment analysis
    """
    if text == "N/A":
        # Handle the case where the recognizer does not understand the audio
        return SentimentResult(polarity=-2.0, subjectivity=None)
    analysis = TextBlob(text)
    return analysis.sentiment
