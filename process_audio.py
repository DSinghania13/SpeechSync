import sys
import whisper
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import os

import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

def process_audio(input_path, output_path, target_language):
    # Model 1: Speech-to-Text using Whisper
    model = whisper.load_model("tiny")
    result = model.transcribe(input_path)
    text = result["text"]

    # Model 2: Translation (Dynamic model selection based on target_language)
    if target_language == 'hi':  # Hindi
        model_name = "Helsinki-NLP/opus-mt-en-hi"
    elif target_language == 'es':  # Spanish
        model_name = "Helsinki-NLP/opus-mt-en-es"
    elif target_language == 'fr':  # French
        model_name = "Helsinki-NLP/opus-mt-en-fr"
    elif target_language == 'bn':  # Bengali
        model_name = "shhossain/opus-mt-en-to-bn"
    else:
        raise ValueError(f"Unsupported target language: {target_language}")

    # Load translation model
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Model 3: Text-to-Speech using gTTS
    tts = gTTS(translation, lang=target_language)

    # Save the translated text as an audio file
    tts.save(output_path)


if __name__ == "__main__":
    input_file = sys.argv[1]  # Path to input audio file
    output_file = sys.argv[2]  # Path to output audio file
    target_language = sys.argv[3]  # Target language passed from backend
    process_audio(input_file, output_file, target_language)
