from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define folders for storing uploaded audio and output audio
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Serve the index.html file as homepage
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve uploaded audio files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Serve output audio files
@app.route('/output/<filename>')
def output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

# Main route to handle upload and processing stages
@app.route('/upload', methods=['POST'])
def upload():
    print("Upload route hit")

    language = request.form.get('language')
    audio = request.files.get('audio')
    stage = request.args.get('stage', 'full')

    print(f"Language: {language}")
    print(f"Audio received: {bool(audio)}")
    print(f"Stage: {stage}")

    if not language or not audio:
        return jsonify({'error': 'Missing language or audio'}), 400

    lang_short = language.split('-')[0]
    input_path = os.path.join(UPLOAD_FOLDER, 'recording.wav')
    output_path = os.path.join(OUTPUT_FOLDER, 'output_audio.wav')
    audio.save(input_path)

    transcription = None
    translation = None

    # Handle full or translation-only processing
    if stage in ['translate', 'full']:
        # Transcription step
        try:
            transcribe_cmd = ['python3', 'process_audio.py', 'transcribe', input_path]
            print(f"Running transcription command: {' '.join(transcribe_cmd)}")
            transcribe_output = subprocess.check_output(transcribe_cmd, stderr=subprocess.STDOUT)
            print("Raw transcription output:\n", transcribe_output.decode())

            json_start = transcribe_output.decode().rfind('{')
            if json_start == -1:
                raise ValueError("No JSON object found in transcription output")

            transcribe_json = json.loads(transcribe_output.decode()[json_start:])
            transcription = transcribe_json.get('transcription', '').strip()
        except subprocess.CalledProcessError as e:
            print("Transcription failed:", e.output.decode())
            return jsonify({'error': 'Transcription failed', 'details': e.output.decode()}), 500
        except Exception as e:
            print("Error parsing transcription JSON:", str(e))
            return jsonify({'error': 'Invalid JSON from transcription', 'details': str(e)}), 500

        # Translation step
        try:
            translate_cmd = ['python3', 'process_audio.py', 'translate-text', transcription, lang_short]
            print(f"Running translation command: {' '.join(translate_cmd)}")
            translate_output = subprocess.check_output(translate_cmd, stderr=subprocess.STDOUT)
            print("Raw translation output:\n", translate_output.decode())

            json_start = translate_output.decode().rfind('{')
            if json_start == -1:
                raise ValueError("No JSON object found in translation output")

            translate_json = json.loads(translate_output.decode()[json_start:])
            translation = translate_json.get('translation', '').strip()
        except subprocess.CalledProcessError as e:
            print("Translation failed:", e.output.decode())
            return jsonify({'error': 'Translation failed', 'details': e.output.decode()}), 500
        except Exception as e:
            print("Error parsing translation JSON:", str(e))
            return jsonify({'error': 'Invalid JSON from translation', 'details': str(e)}), 500

        # Audio synthesis step
        try:
            synth_cmd = ['python3', 'process_audio.py', 'synthesize-audio', translation, output_path, lang_short]
            print(f"Running synthesis command: {' '.join(synth_cmd)}")
            subprocess.check_call(synth_cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            print("Audio synthesis failed:", e.output.decode())
            return jsonify({'error': 'Audio synthesis failed', 'details': e.output.decode()}), 500

        # Final response for full pipeline
        return jsonify({
            'transcription': transcription,
            'translation': translation,
            'inputAudioUrl': '/uploads/recording.wav',
            'outputAudioUrl': '/output/output_audio.wav'
        })

    # Handle transcription-only stage
    elif stage == 'transcribe':
        try:
            transcribe_cmd = ['python3', 'process_audio.py', 'transcribe', input_path]
            print(f"Running transcription command: {' '.join(transcribe_cmd)}")
            transcribe_output = subprocess.check_output(transcribe_cmd, stderr=subprocess.STDOUT)
            print("Raw transcription output:\n", transcribe_output.decode())

            json_start = transcribe_output.decode().rfind('{')
            if json_start == -1:
                raise ValueError("No JSON object found in transcription output")

            transcribe_json = json.loads(transcribe_output.decode()[json_start:])
            transcription = transcribe_json.get('transcription', '').strip()

            return jsonify({
                'transcription': transcription,
                'inputAudioUrl': '/uploads/recording.wav'
            })
        except subprocess.CalledProcessError as e:
            return jsonify({'error': 'Transcription failed', 'details': e.output.decode()}), 500
        except Exception as e:
            return jsonify({'error': 'Invalid JSON from transcription', 'details': str(e)}), 500

    # Invalid stage provided
    else:
        return jsonify({'error': 'Invalid stage provided'}), 400

# Start Flask server on port 5050 with debug mode on
if __name__ == '__main__':
    app.run(port=5050, debug=True)