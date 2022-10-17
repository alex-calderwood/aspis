import whisper
from flask import Flask, request, jsonify
app = Flask(__name__)

def do_transcribe(file):
    model = whisper.load_model("small") # base is faster
    result = model.transcribe(file)
    return result["text"]

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if request.method == 'POST':
        text = do_transcribe(request.files['file'])
        return jsonify({'text': text})