import streamlit as st
import os
import pygame
import threading
from mail import SendEmail  # Assuming you have a module named 'mail' for sending emails

# Global variable to control audio playback
stop_audio = False

def play_mp3_file(file_path):
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Get the directory where pygame examples are installed
    pygame_dir = os.path.dirname(pygame.__file__)
    
    # Construct the path to the MP3 file
    mp3_file_path = os.path.join(pygame_dir, "examples", "data", file_path)
    
    # Load the MP3 file
    pygame.mixer.music.load(mp3_file_path)
    
    # Play the MP3 file in an endless loop
    pygame.mixer.music.play(loops=-1)

def email_and_play_audio(emails, file_path):
    # Start the email process
    email_process = threading.Thread(target=emailer, args=(emails,))
    email_process.start()
    
    # Play the audio file
    play_mp3_file(file_path)

def emailer(emails):
    for email in emails:
        user = SendEmail(email)
        user.criticalImpact('9:00', (15.15, 18.8), 'Log')

def printSending():
    st.write('Sending mail...')

# Main function
def main():
    # Set page title
    st.title("Combined App")
    
    # List of emails
    emails = ['suryaprabhakarangm@gmail.com', 'jofraarcher04@gmail.com', 'krithickguru13@gmail.com', 'valantamildasan@gmail.com', 'officialrudhresh@gmail.com']
    
    # Create button for sending email and playing audio
    send_mail_and_play_audio = st.button("Send Mail and Play Audio")
    
    # Check if the "Send Mail and Play Audio" button is clicked
    if send_mail_and_play_audio:
        email_and_play_audio(emails, "house_lo.mp3")
    
    # Create a "Stop" button to stop audio playback
    stop_button = st.button("Stop Audio")
    
    # Check if the "Stop" button is clicked
    if stop_button:
        # Stop the playback of the audio file
        pygame.mixer.music.stop()

# Call the main function
if __name__ == "__main__":
    main()
