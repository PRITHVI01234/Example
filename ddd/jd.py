import streamlit as st
import os
import pygame
import threading

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

# Main function
def main():
    # Set page title
    st.title("Audio Player")
    
    # Create buttons for user interaction
    button_play = st.button("Play Audio")
    button_stop = st.button("Stop Playback")
    
    # Check if the "Play Audio" button is clicked
    if button_play:
        # Call the function to play the MP3 file
        play_mp3_file("house_lo.mp3")
    
    # Check if the "Stop Playback" button is clicked
    if button_stop:
        # Stop the playback of the audio file
        pygame.mixer.music.stop()

# Call the main function
if __name__ == "__main__":
    main()
