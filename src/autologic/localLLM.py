from llama_cpp import Llama
from dotenv import load_dotenv
import os

def invoke(prompt: str, gguf_path: str = None, threads: int =12 ,temp: float = 0.8, max_context: int = 2000,stop: list[str] = ["[/INST]","<|im_end|>"]) -> str:

    
    llm = Llama(
        model_path=gguf_path,
        n_gpu_layers=-1, 
        n_ctx=max_context, 
        verbose=False,
        n_threads=threads,
        n_threads_batch=threads
    )

    output = llm(
        prompt, # Prompt
        max_tokens=None, # Generate up to 32 tokens, set to None to generate up to the end of the context window
        stop=stop,# Stop generating just before the model would generate a new question
        temperature=temp
    ) # Generate a completion, can also call create_completion
    response = output["choices"][0]["text"]
    return response
