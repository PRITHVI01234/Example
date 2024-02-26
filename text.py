import os
import pygame
import streamlit as st

class AudioPlayer:
    def __init__(self):
        # Get the directory where pygame examples are installed
        self.pygame_dir = os.path.dirname(pygame.__file__)

    def play_mp3_file(self, file_path):
        # Initialize pygame mixer
        pygame.mixer.init()

        # Construct the path to the MP3 file
        mp3_file_path = os.path.join(self.pygame_dir, "examples", "data", file_path)
        # Load the MP3 file
        pygame.mixer.music.load(mp3_file_path)
        # Play the MP3 file in an endless loop
        pygame.mixer.music.play(loops=-1)

    def stop_audio(self):
        # Stop the playback of the audio file
        pygame.mixer.music.stop()

def main():
    st.title("Audio Player")

    # Create an instance of AudioPlayer
    audio_player = AudioPlayer()

    # Start playing audio
    audio_player.play_mp3_file("house_lo.mp3")

    # Add a stop button
    stop_button = st.button("Stop Audio")

    if stop_button:
        # Stop the audio when the button is pressed
        audio_player.stop_audio()

if __name__ == "__main__":
    main()
