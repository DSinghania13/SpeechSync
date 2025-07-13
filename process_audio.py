import sys
import whisper
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
from pydub import AudioSegment
import os
import certifi
import json
import warnings

# Ensure proper SSL certificates are used for downloading models
os.environ["SSL_CERT_FILE"] = certifi.where()

# Suppress any unnecessary warnings
warnings.filterwarnings("ignore")

# Function to transcribe audio using OpenAI's Whisper model
def transcribe_audio(input_path):
    model = whisper.load_model("tiny")  # Load the 'tiny' model for fast transcription
    result = model.transcribe(input_path)  # Run transcription
    return result["text"]  # Return only the transcribed text

# Function to translate English text into the specified target language
def translate_text(text, target_language, output_path=None):
    # Select appropriate translation model based on the target language
    if target_language == 'hi':
        model_name = "Helsinki-NLP/opus-mt-en-hi"
    elif target_language == 'es':
        model_name = "Helsinki-NLP/opus-mt-en-es"
    elif target_language == 'fr':
        model_name = "Helsinki-NLP/opus-mt-en-fr"
    elif target_language == 'bn':
        model_name = "shhossain/opus-mt-en-to-bn"
    else:
        raise ValueError(f"Unsupported target language: {target_language}")

    # Load the tokenizer and model
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # Prepare input and generate translation
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs)
    translated = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # If an output path is given, synthesize speech for the translated text
    if output_path:
        tts = gTTS(translated, lang=target_language)
        temp_mp3 = "temp.mp3"
        tts.save(temp_mp3)
        sound = AudioSegment.from_mp3(temp_mp3)
        sound.export(output_path, format="wav")
        os.remove(temp_mp3)

    return translated  # Return the translated text

# Function to generate speech audio for any given text
def generate_audio(text, target_language, output_path):
    tts = gTTS(text, lang=target_language)  # Generate TTS using gTTS
    temp_mp3 = "temp.mp3"
    tts.save(temp_mp3)  # Save as temporary MP3
    sound = AudioSegment.from_mp3(temp_mp3)  # Load MP3
    sound.export(output_path, format="wav")  # Export to WAV format
    os.remove(temp_mp3)  # Clean up temporary file

# Command-line interface entry point
if __name__ == "__main__":
    args = sys.argv  # Get command-line arguments
    print("Received args:", args, file=sys.stderr)  # Print arguments for debugging

    if len(args) < 3:
        # Not enough arguments provided
        print(json.dumps({"error": "Insufficient arguments"}))
        sys.exit(1)

    mode = args[1]  # Determine mode (transcribe, translate-text, synthesize-audio)

    # Handle transcription
    if mode == "transcribe":
        input_file = args[2]
        try:
            transcript = transcribe_audio(input_file)
            print(json.dumps({"transcription": transcript}))  # Output JSON
        except Exception as e:
            print(json.dumps({"error": str(e)}))

    # Handle translation
    elif mode == "translate-text":
        try:
            text = args[2]
            target_language = args[3]
            translated = translate_text(text, target_language, None)
            print(json.dumps({"translation": translated}))  # Output JSON
        except Exception as e:
            print(json.dumps({"translation": "", "error": str(e)}))

    # Handle audio synthesis
    elif mode == "synthesize-audio":
        try:
            text = args[2]
            output_path = args[3]
            target_language = args[4]

            tts = gTTS(text, lang=target_language)
            temp_mp3 = "temp.mp3"
            tts.save(temp_mp3)
            sound = AudioSegment.from_mp3(temp_mp3)
            sound.export(output_path, format="wav")
            os.remove(temp_mp3)

            print(json.dumps({"audioPath": output_path}))  # Output JSON
        except Exception as e:
            print(json.dumps({"error": str(e)}))

    # Handle unsupported mode
    else:
        print(json.dumps({"error": "Unsupported mode"}))