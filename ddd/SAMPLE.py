import multiprocessing
from mail import SendEmail
import streamlit as st
from pydub import AudioSegment
from pydub.playback import play

# Initialize session state
if 'email_process_started' not in st.session_state:
    st.session_state.email_process_started = False

def emailer(emails):
    for email in emails:
        user = SendEmail(email)
        user.criticalImpact('9:00', (15.15, 18.8), 'Log')

def printSending():
    st.write('Sending mail...')

def play_audio():
    audio_file_path = 'ALARM_SOUND.mp3'  # Change this to the path of your audio file
    sound = AudioSegment.from_mp3(audio_file_path)
    play(sound)

emails = ['suryaprabhakarangm@gmail.com', 'jofraarcher04@gmail.com', 'krithickguru13@gmail.com', 'valantamildasan@gmail.com', 'officialrudhresh@gmail.com']

sendemail = st.button('Send Email')
log = st.button('Log Message')
play_audio_button = st.button('Play Audio')

def main():
    if sendemail and not st.session_state.email_process_started:
        st.session_state.email_process_started = True
        p = multiprocessing.Process(target=emailer, args=(emails,))
        p.start()
        p.join()  # Wait for the process to finish
        st.session_state.email_process_started = False

if log:
    printSending()

if sendemail or log:
    main()

if play_audio_button:
    play_audio()
