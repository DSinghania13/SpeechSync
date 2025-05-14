# 🎙️ SpeechSync – Speak with Ease, Translate in a Breeze

**SpeechSync** is a real-time multilingual speech-to-speech translation system that bridges communication gaps across languages. Built using a modular pipeline of ASR (Automatic Speech Recognition), NMT (Neural Machine Translation), and TTS (Text-to-Speech), SpeechSync delivers low-latency, high-accuracy translations that are both context-aware and user-friendly.

---

## 🚀 Features

- 🎤 Real-time speech recognition with pause/resume control  
- 🌐 Multilingual translation using MarianMT  
- 🗣️ Natural-sounding speech synthesis via TTS  
- ⚡ Low-latency (<5 sec) performance with GPU acceleration  
- 🧠 Support for low-resource languages  
- 💬 WebSocket-based live status updates  
- 🎛️ Clean, responsive UI with audio waveform visualization  

---

## 🛠️ Tech Stack

| Component        | Technology Used             |
|------------------|-----------------------------|
| Frontend         | HTML5, CSS3, Vanilla JS     |
| Backend          | Node.js (Express), WebSocket |
| Translation      | MarianMT (via Python script) |
| Speech-to-Text   | ASR (Whisper or DeepSpeech) |
| Text-to-Speech   | Tacotron / WaveNet (TTS)    |
| GPU Support      | NVIDIA RTX 4070             |

---

## 📸 Interface Overview

- 🎙️ Start, Stop, Pause recording buttons  
- 🎧 Playback and translated audio controls  
- 🌍 Dropdown to select translation language  
- 📈 Real-time waveform visualization  
- ⏳ Spinner showing processing stages via WebSocket  

---

## 📁 Project Structure

```
SpeechSync/
├── index.html                # Frontend interface
├── server.js                 # Node.js backend server
├── process_audio.py          # Python script for ASR + NMT + TTS
├── package.json              # NPM dependencies
├── .gitignore                # Git ignore rules
├── assets/                   # Icons, spinner, audio, etc.
│   ├── microphone.png
│   ├── pause.png
│   ├── stop.png
│   ├── spinner.gif
└── uploads/                  # Runtime audio storage (ignored in Git)
```

---

## 🧑‍💻 Installation & Setup

### 📦 1. Clone the Repository

```bash
git clone https://github.com/DSinghania13/SpeechSync.git
cd speechsync
```

### 🧪 2. Install Node Dependencies

```bash
npm install
```

### 🧪 3. Install Python Requirements

- Make sure you have Python 3 and pip installed. Then run:

```bash
pip install -r requirements.txt
```

###  Run the App

- Start the backend server:

```bash
node server.js
```

- Access the frontend:

```
http://localhost:3000
```

## 🧪 Model Architecture

1.	**ASR** → Transcribes speech into text
2.	**NMT (MarianMT)** → Translates text into target language
3.	**TTS** → Converts translated text into speech

## 🎯 Use Cases

- **Education**: Multi-language classrooms and learning tools
- **Healthcare**: Real-time doctor-patient translation
- **Business**: Cross-lingual collaboration
- **Tourism**: Voice translator for travel
- **Emergency**: Humanitarian aid communication

## 📊 Performance

- **⏱️ Latency**: Under 5 seconds
- **✅ Accuracy**: 90%+ for common languages
- 🌍 Supports Hindi, Spanish, French, Bengali
- 🔁 Scalable with modular backend

## 👨‍💻 Contributors

- Vipransh Ojha
- Divit Singhania
- Gaurav Lodhi
- Abhijeet Dubey

> _“Speak with ease, translate in a breeze” – because the world should never be lost in translation._

---
