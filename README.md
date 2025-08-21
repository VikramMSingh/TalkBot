# LLMSpeechReview

LLMSpeechReview is a web application designed to help users improve their social anxiety and spoken English skills using AI-powered feedback. The app allows users to interact via text or voice, receive constructive and empathetic feedback, and listen to AI-generated responses.

![Built with Gemini](https://img.shields.io/badge/Built%20with-Gemini-blueviolet)
![Powered by Flask](https://img.shields.io/badge/Powered%20by-Flask-lightgrey)
![Uses Google Speech Recognition](https://img.shields.io/badge/Speech%20Recognition-Google-yellowgreen)
![Text-to-Speech-gTTS-orange)

## Features

- **Text and Voice Input:** Communicate with the AI using either text or audio messages.
- **AI-Powered Feedback:** Get actionable advice for social anxiety and spoken English improvement.
- **Speech Recognition:** Transcribes user audio using Google Speech Recognition.
- **Text-to-Speech:** Converts AI responses to audio for playback.
- **Modern UI:** Simple web interface built with Flask.

## How It Works

1. **Text Chat:** Type your message and receive instant feedback.
2. **Voice Chat:** Record and send your voice; the app transcribes and analyzes your speech.
3. **AI Response:** The Gemini LLM provides supportive, concise feedback tailored to your needs.
4. **Listen:** Hear the AI’s response via synthesized speech.

## Setup Instructions

### Prerequisites

- Python 3.8+
- [ffmpeg](https://evermeet.cx/ffmpeg/) installed and available in your system PATH (required for audio conversion)
- Google Gemini API key (store in `gemini.env` as `GEMINI_API_KEY=your_key_here`)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/VikramMSingh/TalkBot.git
    cd TalkBot
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Install ffmpeg (if not already installed):**
    - Download from [evermeet.cx/ffmpeg](https://evermeet.cx/ffmpeg/)
    - Move `ffmpeg` and `ffprobe` binaries to `/usr/local/bin/`:
      ```sh
      sudo mv ~/Downloads/ffmpeg /usr/local/bin/
      sudo mv ~/Downloads/ffprobe /usr/local/bin/
      sudo chmod +x /usr/local/bin/ffmpeg
      sudo chmod +x /usr/local/bin/ffprobe
      ```

4. **Add your Gemini API key:**
    - Create a file named `gemini.env` in the project root:
      ```
      GEMINI_API_KEY=your_api_key_here
      ```

### Running the App

```sh
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

## Usage

- Type a message or upload/record an audio file.
- Receive feedback and listen to the AI’s response.

## Troubleshooting

- **ffmpeg not found:** Ensure `ffmpeg` and `ffprobe` are installed and in your PATH.
- **API key issues:** Make sure your `gemini.env` file is present and contains a valid key.
- **Speech recognition errors:** Check your audio format; most common formats (mp3, wav, m4a) are supported.

## License

MIT License

## Author

[VikramMSingh](https://github.com/VikramMSingh)

---

*Empower your conversations. Overcome social anxiety. Improve your English—one message