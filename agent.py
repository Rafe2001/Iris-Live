from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from tool.webcam import analyze_image_with_query
from prompts import system_prompt
import os

load_dotenv()

# system_prompt = """
# You are **Iris**, a witty, clever, and helpful assistant. Always aim for accuracy and transparency.

# Instructions:
# 1. **Decide Tool Usage**  
#    - For any user query, first determine if the “webcam” tool or other tools is truly needed or not if required then use it otherwise don't use.  
#    - If the question explicitly involves capturing or processing a live camera image, invoke the webcam tool and don't ask for permission to look through the webcam, call it straight away.  
#    - Otherwise, answer directly using your internal knowledge — do not call any tool.

# 2. **No Hallucinations**  
#    - If you do not know an answer, respond: “Sorry, I don’t know the answer.”  
#    - Never guess or invent facts.

# 3. **UX Tone**  
#    - Keep your responses concise, friendly, and engaging.  
#    - Inject light humor where appropriate, but remain professional.

# 4. **Error Handling**  
#    - If the webcam tool fails or returns an error, explain what went wrong in simple terms and suggest next steps.

# Always adhere strictly to these rules.
# """

#client = Groq(api_key = os.getenv("GROQ_API_KEY"))

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model= "deepseek-r1-distill-llama-70b",
    temperature=0.2
)


def ask_agent(user_query: str)->str:
    agent = create_react_agent(
        model = llm,
        tools = [analyze_image_with_query],
        prompt = system_prompt
    )
    
    input_messages = {
        "messages": [
            {
                "role": "user",
                "content": user_query
            }
        ]
    }
    response = agent.invoke(input_messages)
    return response["messages"][-1].content

    
# print(ask_agent(user_query="Do I've beard?"))