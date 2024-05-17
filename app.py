import os
import queue
import re
import sys
import time
import streamlit as st
from google.oauth2 import service_account
from google.cloud import speech
from audio_recorder_streamlit import audio_recorder

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'woven-alpha-364513-06bd95639b48.json'
client = speech.SpeechClient()
STREAMING_LIMIT = 240000  # 4 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

def get_current_time() -> int:
    return int(round(time.time() * 1000))

def listen_print_loop(responses): 
    for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if not result.alternatives:
            continue
        transcript = result.alternatives[0].transcript
        if result.is_final:
            st.write(transcript)
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                st.write("Exiting...")
                break

def process_audio(audio_bytes):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code="en-US",
        max_alternatives=1,
    )
    response = client.recognize(config=config, audio=audio)
    return response

def main():
    st.title("Real-time Speech-to-Text")
    st.write('Click "Start Recording" to record your speech.')

    audio_bytes = audio_recorder()
    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        st.write("Processing audio...")
        responses = process_audio(audio_bytes)
        listen_print_loop(responses)

if __name__ == "__main__":
    main()
