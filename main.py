import gradio as gr
from speech_to_text import record_audio_user, transcribe_audio
from text_to_speech import text_to_speech
from agent import ask_agent
from prompts import system_prompt
import os
import logging
import cv2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
api_key = os.getenv("GROQ_API_KEY")
audio_path = "user_audio2.mp3"

# Global Variables
camera = None
is_running = False
last_frame = None

def process_audio_and_chat():
    """Continuously listen, transcribe, get response, and update chat."""
    chat_history = []
    while True:
        try:
            record_audio_user(file_path=audio_path)
            user_input = transcribe_audio(audio_filepath=audio_path)
            logging.info(f"User input: {user_input}")

            if "goodbye" in user_input.lower():
                logging.info("Exiting the chat.")
                break

            response = ask_agent(user_query=user_input)
            logging.info(f"Agent response: {response}")

            text_to_speech(input_text=response, output_filepath="agent_response.mp3")

            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": response})
            yield chat_history  # Yield updated chat
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            break

# Camera logic
def initialize_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            logging.info("Camera initialized successfully.")
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            camera.set(cv2.CAP_PROP_FPS, 30)
            camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return camera is not None and camera.isOpened()

def start_camera():
    global is_running, last_frame
    is_running = True
    if not initialize_camera():
        logging.error("Failed to initialize camera.")
        return None
    ret, frame = camera.read()
    if ret and frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        last_frame = frame
        return frame
    return last_frame

def stop_camera():
    global is_running, camera
    is_running = False
    if camera is not None:
        camera.release()
        camera = None
        logging.info("Camera stopped successfully.")
    return None

def get_webcam_frame():
    global camera, is_running, last_frame
    if not is_running or camera is None:
        logging.warning("Camera is not running.")
        return last_frame
    if camera.get(cv2.CAP_PROP_BUFFERSIZE) > 1:
        for _ in range(int(camera.get(cv2.CAP_PROP_BUFFERSIZE)) - 1):
            camera.read()
    ret, frame = camera.read()
    if ret and frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        last_frame = frame
        return frame
    return last_frame

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='color: orange; text-align: center; font-size: 4em;'> 👧🏼 Iris – Your Personal AI Assistant</h1>")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Webcam Feed")
            with gr.Row():
                start_btn = gr.Button("Start Camera", variant="primary")
                stop_btn = gr.Button("Stop Camera", variant="secondary")
            webcam_output = gr.Image(label="Live Feed", streaming=True, show_label=False, width=640, height=480)
            webcam_timer = gr.Timer(0.033)

        with gr.Column(scale=1):
            gr.Markdown("## Chat Interface")
            chatbot = gr.Chatbot(
                label="Conversation",
                height=400,
                show_label=False,
                type="messages"  # ✅ Updated to avoid warning
            )
            gr.Markdown("*🎤 Continuous listening mode is active - speak anytime!*")
            with gr.Row():
                clear_btn = gr.Button("Clear Chat", variant="secondary")

    # Button callbacks
    start_btn.click(fn=start_camera, outputs=webcam_output)
    stop_btn.click(fn=stop_camera, outputs=webcam_output)
    webcam_timer.tick(fn=get_webcam_frame, outputs=webcam_output, show_progress=False)
    clear_btn.click(fn=lambda: [], outputs=chatbot)

    # Auto-start audio chat
    demo.load(
        fn=process_audio_and_chat,
        outputs=chatbot
    )

# Launch app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,   # ✅ This creates a public link if online
        debug=True
    )
