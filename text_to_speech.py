from elevenlabs.client import ElevenLabs
import elevenlabs
import subprocess
from gtts import gTTS
import platform
import os
from pydub import AudioSegment  # NEW

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def convert_mp3_to_wav(mp3_path, wav_path):
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

def play_audio(filepath):
    os_name = platform.system()
    
    # Convert mp3 to wav for Windows SoundPlayer
    if os_name == "Windows" and filepath.endswith(".mp3"):
        wav_path = filepath.replace(".mp3", ".wav")
        convert_mp3_to_wav(filepath, wav_path)
        filepath = wav_path

    try:
        if os_name == "Darwin":
            subprocess.run(["afplay", filepath])
        elif os_name == "Windows":
            subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{filepath}').PlaySync();"])
        elif os_name == "Linux":
            subprocess.run(["aplay", filepath])
        else:
            print(f"Unsupported OS: {os_name}")
    except Exception as e:
        print(f"Failed to play audio: {e}")

def text_to_speech(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    elevenlabs.save(audio, output_filepath)
    play_audio(output_filepath)

def text_to_speech_gtts(input_text, output_filepath):
    language = 'en'
    audio = gTTS(text=input_text, lang=language, slow=False)
    audio.save(output_filepath)
    play_audio(output_filepath)

# Run it
# text = "Welcome to Rafe's Assistant!"
# output_file = "output.mp3"
# text_to_speech(text, output_file)
# text_to_speech_gtts(text, output_file)
