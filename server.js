const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');
const WebSocket = require('ws');

const app = express();
const PORT = 3000;
const uploadDirectory = '/output';

// WebSocket server setup
const wss = new WebSocket.Server({ port: 8080 });
wss.on('connection', (ws) => {
    console.log('WebSocket client connected');
});

// Serve the frontend HTML
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Middleware to parse JSON body
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Multer setup
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        if (!fs.existsSync(uploadDirectory)) {
            fs.mkdirSync(uploadDirectory, { recursive: true });
        }
        cb(null, uploadDirectory);
    },
    filename: (req, file, cb) => {
        cb(null, 'recording.wav');
    },
});
const upload = multer({ storage });

// Upload endpoint
app.post('/upload', upload.single('audio'), (req, res) => {
    const inputFilePath = path.join(uploadDirectory, 'recording.wav');
    const outputFilePath = path.join(uploadDirectory, 'output_audio.wav');
    const language = req.body.language;  // Get the selected language

    if (!language) {
        return res.status(400).json({ message: 'Language not selected' });
    }

    // Notify WebSocket clients about the stages
    function sendWebSocketMessage(stage) {
        wss.clients.forEach((client) => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify({ stage }));
            }
        });
    }

    // Simulate stages of processing
    sendWebSocketMessage('Uploading audio...');
    setTimeout(() => sendWebSocketMessage('Transcribing audio...'), 1000);
    setTimeout(() => sendWebSocketMessage('Translating...'), 3000);
    setTimeout(() => sendWebSocketMessage('Generating audio...'), 5000);

    // Command to run the Python script with language argument
    const command = `python3 process_audio.py ${inputFilePath} ${outputFilePath} ${language}`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error('Error:', stderr);
            res.status(500).json({ message: 'Processing error!', error: stderr });
            sendWebSocketMessage('Error occurred during processing.');
        } else {
            console.log('Python script output:', stdout);
            sendWebSocketMessage('Processing complete.');
            res.json({
                message: 'Processing completed!',
                translatedAudioUrl: `/uploads/output_audio.wav`,
            });
        }
    });
});

// Serve static files
app.use('/uploads', express.static(uploadDirectory));
app.use(express.static(path.join(__dirname)));

// Start server
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
