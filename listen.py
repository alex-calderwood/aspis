import whisper
from flask import Flask, request, jsonify
app = Flask(__name__)

data_file = "data/audio.wav"

def do_transcribe(file):
    model = whisper.load_model("small") # base is faster
    result = model.transcribe(file)
    return result["text"]

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if request.method == 'POST':
        # write the file
        file = request.files['file']
        file.save(data_file) # should this be with open?
        # with open(data_file, 'wb') as f:
        #     f.write(file.read())
        text = do_transcribe(data_file)
        return jsonify({'text': text})