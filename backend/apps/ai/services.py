from openai import OpenAI
from django.conf import settings
from django.core.files.base import ContentFile
import uuid

client = None
if settings.OPENAI_API_KEY:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)


def speech_to_text(audio_file):
    """Convert audio file to text using OpenAI Whisper"""
    if not client:
        return None

    try:
        # Rewind the file pointer to the beginning
        audio_file.seek(0)
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcription.text
    except Exception as e:
        print(f"Speech-to-text error: {e}")
        return None


def text_to_speech(text):
    """Convert text to audio using OpenAI TTS"""
    if not client:
        return None

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        # Generate a unique filename
        filename = f"tts_{uuid.uuid4().hex}.mp3"
        # Create a ContentFile from the binary audio data
        audio_content = ContentFile(response.read(), name=filename)
        return audio_content
    except Exception as e:
        print(f"Text-to-speech error: {e}")
        return None


def generate_ai_response(input_text, interaction_type):
    """Generate an AI response using OpenAI GPT, tailored to pharmacy needs"""
    if not client:
        return "Je ne peux pas répondre pour le moment, réessayez plus tard."

    # Create a system prompt based on interaction type
    system_prompt = """Tu es un assistant pharmacie professionnel et serviable, travaillant pour une pharmacie en Côte d'Ivoire.
Tu dois répondre aux questions des utilisateurs sur les médicaments, les symptômes, les pharmacies de garde, etc.
Réponds en français, en étant concis et précis.
Si la question est sur un médicament, donne des informations sur son usage, ses contre-indications (si tu as les infos), sinon indique que tu ne peux pas donner d'avis médical sans consultation.
Si la question est sur des symptômes, conseille de consulter un médecin ou un pharmacien."""

    # Add user input to the messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": input_text}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI response generation error: {e}")
        return "Désolé, je n'ai pas pu générer de réponse pour le moment."
