import os
import streamlit as st
import speech_recognition as sr

st.title("Speech-to-Text Transcription App")

# Function for speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak Anything...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.write("You said: {}".format(text))
    except sr.UnknownValueError:
        st.error("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        st.error("Could not request results from Google Speech Recognition service; {0}".format(e))

# Call the speech-to-text function
speech_to_text()

