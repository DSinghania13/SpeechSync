# 🎙️ SpeechSync – Speak with Ease, Translate in a Breeze

**SpeechSync** is a real-time multilingual speech-to-speech translation system that bridges communication gaps across languages. Built using a modular pipeline of ASR (Automatic Speech Recognition), NMT (Neural Machine Translation), and TTS (Text-to-Speech), SpeechSync delivers low-latency, high-accuracy translations that are both context-aware and user-friendly.

## 🔗 Live Demo

Access the live project here: [View Deployed App](https://speech-sync.vercel.app)

> ⚠️ **For the best experience, open this app in Google Chrome. Safari may have limited audio playback support.**

---

### 🖼️ User Interface Preview

Below is a preview of the web-based interface designed for seamless interaction. Users can speak live and receive real-time translations in an intuitive, responsive interface.

![image](https://github.com/user-attachments/assets/2097ac60-c2c9-46c2-9a93-fb77bbd15de2)

---

## 🚀 Features

- 🎤 Real-time speech recognition with pause/resume control  
- 🌐 Multilingual translation using MarianMT  
- 🗣️ Natural-sounding speech synthesis via gTTS  
- ⚡ Fast performance with Whisper Tiny model  
- 🧠 Support for low-resource languages (Hindi, Bengali, etc.)  
- 🔄 Manual and automatic transcription + translation options  
- 🎛️ Clean, responsive UI with real-time audio waveform visualization  
- 💻 Best experienced in Google Chrome (Safari playback may be limited)

---

## 🛠️ Tech Stack

| Component        | Technology Used               |
|------------------|-------------------------------|
| Frontend         | HTML5, CSS3, JavaScript       |
| Backend          | Flask (Python)                |
| Translation      | MarianMT (transformers)       |
| Speech-to-Text   | OpenAI Whisper (tiny)         |
| Text-to-Speech   | gTTS + pydub                  |
| Audio Encoding   | MediaRecorder API             |

---

## 📸 Interface Overview

- 🎙️ Start, Pause, and Stop recording buttons  
- 🎧 Playback for both input and translated audio  
- 🌍 Clickable buttons to select translation language  
- 📈 Real-time audio waveform visualizer  
- 🔄 Status updates showing transcription and translation stages

---

## 📁 Project Structure

📂 Here's how the core directory looks:

```
SpeechSync/
├── app.py                  # Flask backend server
├── index.html              # Main frontend UI
├── process_audio.py        # ASR, NMT, and TTS logic
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
├── uploads/                # Stores recorded audio files
├── output/                 # Stores generated audio response
```

---

## 🧑‍💻 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/DSinghania13/SpeechSync.git
cd SpeechSync
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python3.12 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python3 app.py
```

- Open your browser (preferably **Google Chrome**) and go to:

```
http://localhost:5050
```

---

## 🧪 Model Architecture

1.	**ASR (Whisper)** → Transcribes speech into text
2.	**NMT (MarianMT)** → Translates text into target language
3.	**TTS (gTTS)** → Converts translated text into speech

---

## ⚙️ How It Works

1. **Transcribe**: Converts input speech to text using Whisper.
2. **Translate**: Translates English text to the selected language using MarianMT.
3. **Synthesize**: Generates translated speech using gTTS and plays it back.

---

## 🌍 Supported Languages

- Hindi (`hi-IN`)
- Bengali (`bn-IN`)
- Spanish (`es-SP`)
- French (`fr-FR`)

> Note: More languages can be added by extending the MarianMT and gTTS logic in `process_audio.py`.

---

## 🎯 Use Cases

- **Education**: Multi-language classrooms and learning tools
- **Healthcare**: Real-time doctor-patient translation
- **Business**: Cross-lingual collaboration
- **Tourism**: Voice translator for travel
- **Emergency**: Humanitarian aid communication

---

## 📊 Performance

- **⏱️ Latency**: Under 5 seconds
- **✅ Accuracy**: 90%+ for common languages
- 🌍 Supports Hindi, Spanish, French, Bengali
- 🔁 Scalable with modular backend

---

## 👨‍💻 Contributors

- [Vipransh Ojha](https://www.linkedin.com/in/vipransh-ojha/)
- [Divit Singhania](https://www.linkedin.com/in/divit-singhania-13401628a/)
- Gaurav Lodhi
- [Abhijeet Dubey](https://www.linkedin.com/in/aiabhijeet/)

> _“Speak with ease, translate in a breeze” – because the world should never be lost in translation._

---
