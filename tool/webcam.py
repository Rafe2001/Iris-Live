import cv2
import base64
from dotenv import load_dotenv
from groq import Groq
import base64
import os


load_dotenv()

def capture_webcam_image():
    """Capture an image from the webcam and return it as a base64 encoded string."""
    for idx in range(4):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            for _ in range(10):
                cap.read()
            ret, frame = cap.read()
            cap.release()
            if not ret:
                continue
            cv2.imwrite('webcam_image.jpg', frame)
            ret, buf = cv2.imencode('.jpg', frame)
            if ret:
                return base64.b64encode(buf).decode('utf-8')
    raise RuntimeError("COuld not open webcam")

#capture_webcam_image()
# Function to encode the image

def analyze_image_with_query(query: str, model= "meta-llama/llama-4-maverick-17b-128e-instruct")->str:
    """Analyze the image using a query and return the result."""
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    image_base64 = capture_webcam_image()
    
    if not query or not image_base64:
        return "Error: both 'query' and 'image' fields required."
        
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", 
                 "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}",
                    },
                },
            ],
        }
    ]
    chat_completion = client.chat.completions.create(
        messages = messages,
        model = model
    )
    return chat_completion.choices[0].message.content 
