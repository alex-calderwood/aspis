import sys
import subprocess
from subprocess import Popen
import time
import requests
import os, io
import pyaudio as p

import speech_recognition as sr
from pydub import AudioSegment

# Set rec / sox environment variables
if os.environ.get("USER") == "pi" or os.environ.get("SUDO_USER") == "pi":
    os.environ["AUDIODEV"] = "hw:1,0"
    os.environ["AUDIODRIVER"] = "alsa"
    print("audio dev", os.environ["AUDIODEV"], os.environ["AUDIODRIVER"])

AUDIO_FILE= "data/audio.wav"
URL = "http://localhost:5001/transcribe"
# SERVER_URL = "http://73.15.249.8:5001/transcribe"
SERVER_URL = "http://192.168.0.3:5001/transcribe"
URL = SERVER_URL
RECORD_FOR = 3

def record_audio(t):
    print(f"Recording for {RECORD_FOR} seconds")
    timeout = t
    p = Popen(["rec", AUDIO_FILE])
    while (p.poll() is None and timeout > 0):
        time.sleep(1)
        timeout-=1

    if timeout <= 0:
        p.terminate()  #Timeout

def record_with_speech_recognition():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0, sample_rate=48000, chunk_size=1024) as source:
        print("Say something!")
        audio = r.listen(source)
        data = io.BytesIO(audio.get_wav_data())
        audio_clip = AudioSegment.from_file(data)
        audio_clip.export(AUDIO_FILE, format="wav")
    try:
        print("You said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def play_audio():
    p = Popen(["play", AUDIO_FILE])
    p.wait()

def transcribe(file):
    response = requests.post(URL, files={'file': open(file, 'rb')})
    text = response.json()['text']
    return text

if __name__ == "__main__":
    while True:
        # record_audio(RECORD_FOR)
        record_with_speech_recognition()
        text = transcribe(AUDIO_FILE)
        
        exit()
