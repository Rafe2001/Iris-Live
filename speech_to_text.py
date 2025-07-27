from groq import Groq
import os
from dotenv import load_dotenv
import logging
from io import BytesIO
from pydub import AudioSegment
import speech_recognition as sr

load_dotenv()


logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

def record_audio_user(file_path, timeout = 20, phrase_time_limit = None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting the ambient noise....")
            recognizer.adjust_for_ambient_noise(source, 
                                                duration=1
                                                )
            logging.info("Start speaking please.....")
            audio_data = recognizer.listen(
                source, 
                timeout=timeout, 
                phrase_time_limit = phrase_time_limit
            )
            logging.info("Recording finished.")
            
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            logging.info(f"Audio saved to {file_path}")
    except sr.WaitTimeoutError:
        logging.error("Recording timed out. Please try again.")
    except Exception as e:
        logging.error(f"An error occurred during recording: {e}")
        

def transcribe_audio(audio_filepath):
    stt_model = "whisper-large-v3"
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    audio_file = open(audio_filepath, "rb")
    transcribation = client.audio.transcriptions.create(
        model=stt_model, 
        file=audio_file, 
        language= "en"
    )
    return transcribation.text

# path = "user_audio.mp3"
# output = transcribe_audio(path)
# print(output)    
    
            