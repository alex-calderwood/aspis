import sys
import subprocess
from subprocess import Popen
import time
import requests
import os

# Set rec / sox environment variables
if os.environ["USER"].strip() == "pi" or os.environ["SUDO_USER"] == "pi":
    os.environ["AUDIODEV"] = "hw:1,0"
    os.environ["AUDIODRIVER"] = "alsa"
    print("audio dev", os.environ["AUDIODEV"], os.environ["AUDIODRIVER"])

AUDIO_FILE= "data/audio.wav"
URL = "http://localhost:5001/transcribe"
# SERVER_URL = "http://73.15.249.8:5001/transcribe"
SERVER_URL = "http://192.168.0.3:5001/transcribe"
URL = SERVER_URL
RECORD_FOR = 100 

def record_audio(t):
    timeout = t
    p = Popen(["rec", AUDIO_FILE])
    while (p.poll() is None and timeout > 0):
        time.sleep(1)
        timeout-=1

    if timeout <= 0:
        p.terminate()  #Timeout

def play_audio():
    p = Popen(["play", AUDIO_FILE])
    p.wait()

def transcribe(file):
    response = requests.post(URL, files={'file': open(file, 'rb')})
    text = response.json()['text']
    print(text)

if __name__ == "__main__":
    print(f"Recording for {RECORD_FOR} seconds")
    while True:
        record_audio(RECORD_FOR)
        transcribe(AUDIO_FILE)
        exit()
