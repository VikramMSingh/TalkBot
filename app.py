# app.py

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import speech_recognition as sr
from gtts import gTTS
import os
import io
import base64
import google.generativeai as genai
from dotenv import load_dotenv
from pydub import AudioSegment

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, useful for development

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print("Gemini API configured successfully.")
else:
    print("Warning: GEMINI_API_KEY not found in .env file. AI interaction might not work.")

# Initialize the speech recognizer
r = sr.Recognizer()

# --- Utility Functions ---

def get_ai_response(user_message):
    """
    Sends user message to Gemini LLM and gets a response.
    The prompt is designed to act as a social anxiety and English speaking coach.
    """
    if not GEMINI_API_KEY:
        return "AI service is not configured. Please provide an API key."

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        # Combined prompt for social anxiety and spoken English feedback
        prompt = f"""You are an AI assistant specialized in helping individuals with social anxiety and improving their spoken English.
        Your goal is to provide constructive, empathetic, and actionable feedback on the user's conversational inputs.
        For social anxiety, focus on identifying areas for improvement in social interactions, suggesting coping mechanisms, and building confidence.
        For spoken English, provide feedback on grammar, vocabulary, pronunciation (if implied by context or common errors), and fluency.
        Always maintain a supportive, encouraging, and non-judgmental tone.
        Keep your responses concise and helpful.

        Here's the user's message: "{user_message}"
        """
        response = model.generate_content(prompt)

        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            return "I'm sorry, I couldn't generate a response. Please try again."
    except Exception as e:
        print(f"Error communicating with AI: {e}")
        return f"An error occurred while getting AI response: {e}"

def text_to_speech(text):
    """Converts text to speech and returns audio data as base64 string."""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        # Encode audio data to base64 for sending over HTTP
        return base64.b64encode(audio_buffer.read()).decode('utf-8')
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return None

def speech_to_text(audio_data):
    """Transcribes audio data (BytesIO object) to text."""
    try:
        # Use the audio data directly from BytesIO
        text = r.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred during speech-to-text: {e}")
        return ""

# --- Flask Routes ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/chat_text', methods=['POST'])
def chat_text():
    """Handles text-based chat messages."""
    data = request.get_json()
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    ai_response_text = get_ai_response(user_message)
    ai_response_audio_base64 = text_to_speech(ai_response_text)

    return jsonify({
        "text": ai_response_text,
        "audio": ai_response_audio_base64
    })

@app.route('/chat_audio', methods=['POST'])
def chat_audio():
    """Handles audio-based chat messages."""
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    audio_data = io.BytesIO(audio_file.read())

    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data.getvalue()))
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)
    except Exception as e:
        return jsonify({"error": f"Audio conversion failed: {e}"}), 400

    #Read audio data
    try:
        with sr.AudioFile(wav_io) as source:
            audio = r.record(source)
            user_message = speech_to_text(audio)
    except Exception as e:
        return jsonify({"error": f"Speech recognition failed: {e}"}), 400       

    if not user_message:
        return jsonify({
            "text": "I couldn't understand your audio. Could you please repeat or type?",
            "audio": text_to_speech("I couldn't understand your audio. Could you please repeat or type?")
        })

    # Get AI response based on transcribed text
    ai_response_text = get_ai_response(user_message)
    ai_response_audio_base64 = text_to_speech(ai_response_text)

    return jsonify({
        "user_text": user_message, # Return transcribed user text for display
        "text": ai_response_text,
        "audio": ai_response_audio_base64
    })

if __name__ == '__main__':
    # Create 'templates' directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    # Run the Flask app
    app.run(debug=True) # debug=True for development, turn off for production
