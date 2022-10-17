import subprocess
from subprocess import Popen
import time
import requests

AUDIO_FILE= "data/audio.wav"
URL = "http://localhost:5001/transcribe"
RECORD_FOR = 3

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
    # play_audio()
