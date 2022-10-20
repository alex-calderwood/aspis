import sys
import subprocess
from subprocess import Popen
import time
import requests
import os, io
import pyaudio as pa

import speech_recognition as sr
from pydub import AudioSegment

from dazzled import Dazzled

# Run mic_info.py for some of this
DEVICE_INDEX=1
CHUNK =8096
CHANNELS=1
RATE=44100
FORMATIN = pa.paInt32
FORMATOUT = pa.paFloat32

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
RECORD_FOR = 15

dazzled = Dazzled()
dazzled.set_color((255, 0, 0), 0)

def record_audio(t):
    print(f"Recording for {RECORD_FOR} seconds")
    timeout = t
    p = Popen(["rec", AUDIO_FILE])
    while (p.poll() is None and timeout > 0):
        print('check')
        time.sleep(1)
        timeout-=1

    if timeout <= 0:
        p.terminate()  #Timeout

def record_pyaudio():
    audio = pa.PyAudio()
    print("Recording", audio.get_device_info_by_index(DEVICE_INDEX)['defaultSampleRate'], RATE)
    stream_in = audio.open(format=FORMATIN, channels=CHANNELS, rate=RATE, input=True, input_device_index=DEVICE_INDEX, frames_per_buffer=CHUNK)
    stream_out = audio.open(format=FORMATOUT, channels=CHANNELS, rate=RATE, output=True, input_device_index=DEVICE_INDEX, frames_per_buffer=CHUNK)

    while(True):
        print("read")
        in_data = stream_in.read(CHUNK)
        print("write")
        stream_out.write(in_data)

def record_with_speech_recognition():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1, sample_rate=RATE, chunk_size=CHUNK) as source:
        print("Say something!")
        audio = r.listen(source)
        data = io.BytesIO(audio.get_wav_data())
        audio_clip = AudioSegment.from_file(data)
        audio_clip.export(AUDIO_FILE, format="wav")

def play_audio():
    p = Popen(["play", AUDIO_FILE])
    p.wait()

def transcribe(file):
    response = requests.post(URL, files={'file': open(file, 'rb')})
    text = response.json()['text']
    return text

def text_based_lights(text):
    text = text.lower()
    if "red" in text:
        dazzled.set_color((255, 0, 0), 0)
    if "green" in text:
        dazzled.set_color((0, 255, 0), 0)
    if "blue" in text:
        dazzled.set_color((0, 0, 255), 0)
    if "shine" in text:
        dazzled.wave(2, (100, 100, 100))

if __name__ == "__main__":
    while True:
        # record_audio(RECORD_FOR)
        record_with_speech_recognition()
        # record_pyaudio()
        print("transcribing")
        text = transcribe(AUDIO_FILE)
        text_based_lights(text)
        print(text)
