import whisper
from flask import Flask, request, jsonify
import pronouncing
app = Flask(__name__)
# https://github.com/saharmor/whisper-playground

data_file = "data/audio.wav"

def do_transcribe(file):
    model = whisper.load_model("small") # base is faster
    result = model.transcribe(file)
    return result["text"]

def do_nlp(text):
    words = text.split()
    rhymes = pronouncing.rhymes(text)
    return {"words": words, "rhymes": rhymes}

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if request.method == 'POST':
        file = request.files['file']
        file.save(data_file)
        text = do_transcribe(data_file)
        # if request.args.get('nlp'):
        features = do_nlp(text)
        return jsonify({'text': text, 'features': features})