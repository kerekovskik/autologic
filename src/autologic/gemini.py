import google.generativeai as genai
from dotenv import load_dotenv
import os

def invoke(prompt: str, api_key: str = None, temp: float = 0.8, max_context: int = 2000):
    
    if not api_key:
        load_dotenv()
        api_key = os.environ.get("GEMINI_PRO_API_KEY")
    genai.configure(api_key=api_key)

    # Set up the model
    generation_config = {
        "temperature": temp,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": max_context,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
    ]

    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    convo = model.start_chat(history=[])

    convo.send_message(prompt)
    return convo.last.text
