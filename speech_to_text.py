import streamlit as st
import speech_recognition as sr

def speechTotext():
    text=" "
    st.title("Speech to Text Converter")

    st.write("Click the 'Start' button and speak into your microphone.")

    if st.button("Start"):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Speak something...")
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            st.write("You said:", text)
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand your speech.")
        except sr.RequestError as e:
            st.write("Error occurred during speech recognition:", e)

    return text


text=speech_to_text()
