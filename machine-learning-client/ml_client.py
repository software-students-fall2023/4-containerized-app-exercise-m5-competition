import speech_recognition as sr
from textblob import TextBlob
import os

def transcribe_audio(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment

# test if it is working
audio_text = transcribe_audio("./machine-learning-client/kids_are_talking.wav")
sentiment = analyze_sentiment(audio_text)
print("Transcribed Text:", audio_text)
print("Sentiment:", sentiment)
