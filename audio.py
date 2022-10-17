import subprocess
from subprocess import Popen
import time
import whisper

AUDIO_FILE= "data/audio.wav"

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
    model = whisper.load_model("small") # base is faster
    result = model.transcribe(file)
    print(result["text"])

if __name__ == "__main__":
    while True:
        record_audio(10)
        transcribe(AUDIO_FILE)
    # play_audio()
