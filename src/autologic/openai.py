import openai
from dotenv import load_dotenv
import os



def invoke(prompt: str, api_key: str = None, temp: float = 0.8, max_context: int = 2000, model_name: str = None):
    
    if not api_key:
        load_dotenv()
        api_key = os.environ.get("AUTOLOGIC_OPENAI_API_KEY")

    # Set default model name if caller did not specify
    if not model_name:
        model_name = "gpt-3.5-turbo-0125"

    client = openai.OpenAI(api_key=api_key) 
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI chatbot who pays very close attention to instructions from the user - especially any instructions on how to format your response."
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=temp,
        max_tokens=max_context,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content