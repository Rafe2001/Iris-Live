# 👧🏼 Iris – Voice-First Personal AI Assistant with Vision

*A witty, clever, and helpful assistant—just like Gemini Live, but your own.*

## Overview

**Iris** is a real‑time, voice-driven AI assistant that listens, thinks, speaks, and even sees.

* Accepts **continuous voice input** using microphone and STT transcription.
* Responds through **LLM-powered chat**, following a strict prompt to avoid hallucinations.
* **Webcam-enabled**: responds to live camera queries instantly (invokes webcam tool when needed).
* Replies in natural speech via TTS.
* Built with modular components–easy to extend.

---

## ⚙️ Features

| Feature                     | Description                                                                                                   |
| --------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Continuous voice interface  | Just speak; Iris listens and responds automatically                          ([Medium][2], [Hugging Face][1]) |
| Intelligent chat responses  | LLM-based replies with personality, accuracy, and wit                                                         |
| Webcam-powered visual input | Automatically captures camera feed when a visual query is issued                                              |
|Speech to Text Input         | Used whisper model to take the input via audio that will get transcribe by the model                          |
| Text‑to‑speech output       | Responses are spoken aloud in natural voice using ElevenLabs or gTTs                                          |
| Gradio-based UI             | Clean, responsive interface built with `gr.Blocks`, `gr.Image`, and `gr.Chatbot` components ([Gradio][3])     |

---

## 🔧 Tech Stack

* **Python**
* **Gradio** for UI–Blocks, image streaming, chatbot UI (type="messages") ([Gradio][4])
* **OpenCV** for webcam capture
* **Speech-to-Text** and **Text-to-Speech** modules
* **Langchain and LangGraph** for text-based intelligence i.e. Agent

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install gradio opencv-python
# plus any speech‑to‑text/text‑to‑speech dependencies
```

Set your environment variable:

```bash
export GROQ_API_KEY="your_api_key"
```

### Running Iris

```bash
python main.py
```

* Open browser at: `http://localhost:7860`
* For external access (public link): ensure you’re online and use `share=True` in `demo.launch()`

---

## 🧠 System Prompt

```text
You are Iris, a witty, clever, and helpful assistant. Always aim for accuracy and transparency.
1. Decide Tool Usage…
2. No hallucinations…
3. UX tone: concise, friendly, engaging…
4. Error handling…
```

This ensures Iris decides when to invoke the webcam, never invents answers, and keeps the experience dynamic.

---

## 🗣️ How It Works

1. **Audio recording** from user → voice transcribed to text
2. **LLM** processes user query → replies based on `system_prompt` rules
3. **TTS** converts response to speech (agent\_response.mp3)
4. **Chat history** maintained in OpenAI-style message format, streamed live via `yield` to Gradio chatbot component ([Gradio][5], [Hugging Face][1], [Gradio][3], [Gradio][6], [dev.to][7], [Gradio][4])

---

## 📷 Webcam Tool Usage

* For image-based queries (e.g., “what do your camera see?”), Iris will directly capture and process a frame via OpenCV — no user prompt required for tool invocation.
* If any error occurs during webcam capture, Iris explains in plain language and suggests steps (restarting camera, checking devices).

---

## 🧪 Extending Iris

Things you could add:

* **Auto-play agent’s response audio** using a `gr.Audio` component
* **LAN-based access** by supplying `server_name=<local_ip>` instead of `0.0.0.0`
* Add **examples**, **session persistence**, or **support more tools** per system prompt logic

---

## 🙋 Contribution

Feel free to fork or raise an issue! Suggestions, bug reports, or witty jokes to add to Iris’s personality are all welcome.
