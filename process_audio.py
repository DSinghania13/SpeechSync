import sys
import whisper
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
from pydub import AudioSegment
import os
import certifi
import json
import warnings

os.environ["SSL_CERT_FILE"] = certifi.where()

warnings.filterwarnings("ignore")

def transcribe_audio(input_path):
    model = whisper.load_model("tiny") 
    result = model.transcribe(input_path)
    return result["text"]  

def translate_text(text, target_language, output_path=None):
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

    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs)
    translated = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if output_path:
        tts = gTTS(translated, lang=target_language)
        temp_mp3 = "temp.mp3"
        tts.save(temp_mp3)
        sound = AudioSegment.from_mp3(temp_mp3)
        sound.export(output_path, format="wav")
        os.remove(temp_mp3)

    return translated 

def generate_audio(text, target_language, output_path):
    tts = gTTS(text, lang=target_language)  
    temp_mp3 = "temp.mp3"
    tts.save(temp_mp3)  
    sound = AudioSegment.from_mp3(temp_mp3)  
    sound.export(output_path, format="wav")  
    os.remove(temp_mp3) 

if __name__ == "__main__":
    args = sys.argv  
    print("Received args:", args, file=sys.stderr)  

    if len(args) < 3:
        print(json.dumps({"error": "Insufficient arguments"}))
        sys.exit(1)

    mode = args[1]  # Determine mode (transcribe, translate-text, synthesize-audio)

    if mode == "transcribe":
        input_file = args[2]
        try:
            transcript = transcribe_audio(input_file)
            print(json.dumps({"transcription": transcript}))  # Output JSON
        except Exception as e:
            print(json.dumps({"error": str(e)}))

    elif mode == "translate-text":
        try:
            text = args[2]
            target_language = args[3]
            translated = translate_text(text, target_language, None)
            print(json.dumps({"translation": translated}))  # Output JSON
        except Exception as e:
            print(json.dumps({"translation": "", "error": str(e)}))

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

    
    else:
        print(json.dumps({"error": "Unsupported mode"}))
