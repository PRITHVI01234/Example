from pydub import AudioSegment
import sounddevice as sd

def play_audio(audio_file):
    sound = AudioSegment.from_mp3(audio_file)
    audio_data = sound.raw_data
    sd.play(audio_data, blocking=True)
