import os
import re
import streamlit as st
from google.oauth2 import service_account
from google.cloud import speech
from audio_recorder_streamlit import audio_recorder

# Set up Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'woven-alpha-364513-06bd95639b48.json'
client = speech.SpeechClient()

SAMPLE_RATE = 16000

def process_audio(audio_bytes):
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    return response

def display_transcription(response):
    for result in response.results:
        if result.alternatives:
            transcript = result.alternatives[0].transcript
            st.write(transcript)
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                st.write("Detected exit command. Exiting...")
                break

def main():
    st.title("Speech-to-Text with Google Cloud")
    st.write('Click "Start Recording" to record your speech.')

    # Use the audio_recorder component to capture audio from the user
    audio_bytes = audio_recorder()

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        st.write("Processing audio...")
        response = process_audio(audio_bytes)
        display_transcription(response)

if __name__ == "__main__":
    main()
