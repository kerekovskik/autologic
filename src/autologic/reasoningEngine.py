from . import config
from enum import Enum
from dataclasses import dataclass, field
from . import utils
from . import gemini 
from dotenv import load_dotenv
import os
from . import localLLM
from .utils import log_print
import json

__all__ = ['ModelType','LLMConfig','select','adapt','implement','solve','self_discover','ChatTemplate']


class ModelType(Enum):
    GEMINI = "gemini"
    LOCAL = "local"
    #GPT = "gpt" #TODO Add support for openai gpt4 and gpt3.5

class ChatTemplate(Enum):
    MIXTRAL_INSTRUCT = "mixtral_instruct"
    ZEPHYR = "zephyr"
    CHATML = "chatml"
    
    

@dataclass
class LLMConfig:
    gguf_path: str = field(default=None,metadata={"description": "Only for local ModelType. Path to GGUF file."})
    context_length: int = field(default=2000,metadata={"description": "Context Limit in terms of Tokens."})
    threads: int = field(default=12,metadata={"description": "Only for local ModelType. Number of threads to use."})
    api_key: str = field(default=None,metadata={"description": "Not used by GPT/Gemini ModelTypes. API key used for model."})
    temp: float = field(default=0.8,metadata={"description": "LLM Temperature setting."})
    chat_template: ChatTemplate = field(default=ChatTemplate.MIXTRAL_INSTRUCT,metadata={"description": "Only for local ModelType. Chat Template Type"})
    model_type: ModelType = field(default=ModelType.GEMINI,metadata={"description": "Model Type."})
    
    
def formatPrompt(prompt: str,llmConfig: LLMConfig) ->tuple:
    stop = []
    if llmConfig.chat_template == ChatTemplate.MIXTRAL_INSTRUCT:
        prompt = f"[INST] {prompt} [/INST]"
        stop = ["[/INST]"]
    elif llmConfig.chat_template == ChatTemplate.ZEPHYR:
        prompt = f"<|system|>\nYou are a friendly AI assistant who follows directions.</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"
        stop = ["</s>"]
    elif llmConfig.chat_template == ChatTemplate.CHATML:
        prompt = f"<|im_start|>system \nYou are a friendly AI assistant who follows directions.<|im_end|><|im_start|>user\n {prompt}<|im_end|>\n<|im_start|>assistant \n"
        stop = ['<|im_end|>']
        
    else:
        raise ValueError("Invalid ChatTemplate Enum!")
    
    return (prompt,stop)


def select(task: str, llmConfig: LLMConfig = LLMConfig()) -> dict:
    
    selection = None
    if llmConfig.model_type == ModelType.GEMINI:
        selection = __select_gemini(llmConfig=llmConfig,task=task)
    elif llmConfig.model_type == ModelType.LOCAL:
        selection = __select_local(llmConfig=llmConfig,task=task)
    else:
        raise ValueError("Unsupported model Type!")
    
    return selection

def adapt(task: str, reasoning_modules: dict, llmConfig: LLMConfig = LLMConfig()) -> str:
    
    adapted_modules = None
    if llmConfig.model_type == ModelType.GEMINI:
        adapted_modules = __adapt_gemini(llmConfig=llmConfig,task=task,reasoning_modules=reasoning_modules)
    elif llmConfig.model_type == ModelType.LOCAL:
        adapted_modules = __adapt_local(llmConfig=llmConfig,task=task,reasoning_modules=reasoning_modules)
    else: 
        raise ValueError("Unsupported model Type!")
    
    return adapted_modules

def implement(task: str, adapted_modules: str, llmConfig: LLMConfig = LLMConfig()) -> dict:
    
    reasoning_structure = None
    if llmConfig.model_type == ModelType.GEMINI:
        reasoning_structure = __implement_gemini(llmConfig=llmConfig,task=task,adapted_modules=adapted_modules)
    elif llmConfig.model_type == ModelType.LOCAL:
        reasoning_structure = __implement_local(llmConfig=llmConfig,task=task,adapted_modules=adapted_modules)
    else: 
        raise ValueError("Unsupported model Type!")
    
    return reasoning_structure
    
def __implement_gemini(llmConfig: LLMConfig, task: str, adapted_modules: str):
    prompt = config.IMPLEMENT_PHASE_PROMPT_TEMPLATE.format(task=task,modules=adapted_modules)
    response = gemini.invoke(prompt,api_key=llmConfig.api_key,temp=llmConfig.temp,max_context=llmConfig.context_length)
    reasoning_structure = utils.extractJSONToDict(response=response)
    return reasoning_structure

def __implement_local(llmConfig: LLMConfig, task: str, adapted_modules: str):
    prompt = config.IMPLEMENT_PHASE_PROMPT_TEMPLATE.format(task=task,modules=adapted_modules)
    
    prompt,stop = formatPrompt(prompt,llmConfig)
    
    response = localLLM.invoke(
        prompt = prompt,
        gguf_path=llmConfig.gguf_path,
        temp=llmConfig.temp,
        max_context=llmConfig.context_length,
        threads=llmConfig.threads,
        stop=stop
        
    )
    
    reasoning_structure = utils.extractJSONToDict(response=response)
    return reasoning_structure


def self_discover(task: str, llmConfig: LLMConfig = LLMConfig(),verbose=False,retries = 3) -> dict:
    
    # SELECT
    selection = None 
    numAttempts = 0
    log_print("Starting SELECT Phase")
    while selection is None and numAttempts < retries:
        try:
            selection = select(task= task,llmConfig=llmConfig)
        except Exception as e:
            numAttempts += 1
            log_print(f"Failed to select Reasoning Modules due to {e}...")
    if selection is None: raise Exception("Unable to Reasoning Module selection from LLM response.")
    log_print("SELECT Phase Complete")
    if verbose: 
        
        module_list = ""
        for module in selection["reasoning_modules"]:
            module_list += f"- {module}. {utils.id_to_rm(module)}\n"
        log_print(f"Reasoning Modules Picked:\n{module_list}")
            
    # ADAPT
    adapted_modules = None
    numAttempts = 0
    log_print("Starting ADAPT Phase")
    while adapted_modules is None and numAttempts < retries:
        try:
            adapted_modules = adapt(task=task,reasoning_modules=selection,llmConfig=llmConfig)
        except Exception as e:
            numAttempts += 1
            log_print(f"Failed to rephrase Reasoning Modules due to {e}...")
    if adapted_modules is None: raise Exception("Unable to extract adapted_modules from LLM response.")
    log_print("ADAPT Phase Complete")
    if verbose: 
        log_print(f"Task-specific Reasoning Module verbiage:\n{adapted_modules}")
    
    # IMPLEMENT
    reasoning_structure = None
    numAttempts = 0
    log_print("Starting IMPLEMENT Phase")
    while reasoning_structure is None and numAttempts < retries:
        try:
            reasoning_structure = implement(task=task,adapted_modules=adapted_modules,llmConfig=llmConfig)
        except:
            numAttempts += 1
            if verbose: log_print(f"Failed to construct Reasoning Structure in JSON. Starting attempt {numAttempts+1}/{retries} ...")
    if reasoning_structure is None: raise Exception("Unable to extract reasoning structure from LLM response.")
    log_print("IMPLEMENT Phase Complete")
    if verbose: 
        log_print(f"Reasoning Structure:\n{json.dumps(reasoning_structure, indent=2)}")
        
    return reasoning_structure
    
def solve(task: str, llmConfig: LLMConfig = LLMConfig(),verbose=False,retries=3) -> str:
    
    reasoning_structure = self_discover(task=task,llmConfig=llmConfig,verbose=verbose,retries=retries)
    log_print
    if llmConfig.model_type == ModelType.GEMINI:
        answer = __solve_gemini(task=task,llmConfig=llmConfig,reasoning_structure=reasoning_structure,verbose=verbose,retries=retries)
    elif llmConfig.model_type == ModelType.LOCAL:
        answer = __solve_local(task=task,llmConfig=llmConfig,reasoning_structure=reasoning_structure,verbose=verbose,retries=retries)
    log_print("Solution has been found.")
    return answer
    
def __solve_gemini(task: str, llmConfig: LLMConfig,reasoning_structure: dict,verbose=False,retries=3) -> str:
    
    reasoning_structure_str = json.dumps(reasoning_structure,indent=2)
    prompt = config.SOLVE_PROMPT_TEMPLATE.format(task=task,reasoning_structure=reasoning_structure_str)
    numAttempts = 0
    answer = None
    log_print("Starting to Solve Problem using Reasoning Structure")
    while answer is None and numAttempts < retries:
        try:
            response = gemini.invoke(prompt,api_key=llmConfig.api_key,temp=llmConfig.temp,max_context=llmConfig.context_length)
            reasoning = utils.extractJSONToDict(response)
            answer = reasoning["Reasoning Structure"]["FINAL_ANSWER"]
        except Exception as e:
            numAttempts += 1
            if verbose: log_print(f"Failed to Extract answer. Exception: {e} . Starting attempt {numAttempts+1}/{retries} ...")
    if verbose: log_print(f"Problem Solved\nCompleted Reasoning Structure:\n{json.dumps(reasoning,indent=2)}")
    return answer

def __solve_local(task: str, llmConfig: LLMConfig,reasoning_structure: dict,verbose=False,retries=3) -> str:
    reasoning_structure_str = json.dumps(reasoning_structure,indent=2)
    prompt = config.SOLVE_PROMPT_TEMPLATE.format(task=task,reasoning_structure=reasoning_structure_str)
    
    prompt,stop = formatPrompt(prompt,llmConfig)
    
    numAttempts = 0
    answer = None
    log_print("Starting to Solve Problem using Reasoning Structure")
    while answer is None and numAttempts < retries:
        try:
            response = localLLM.invoke(
                prompt = prompt,
                gguf_path=llmConfig.gguf_path,
                temp=llmConfig.temp,
                max_context=llmConfig.context_length,
                threads=llmConfig.threads,
                stop=stop
            )
            
            reasoning = utils.extractJSONToDict(response)
            answer = reasoning["Reasoning Structure"]["FINAL_ANSWER"]
        except Exception as e:
            numAttempts += 1
            
            if verbose: log_print(f"Failed to Extract answer. Exception: {e} . Starting attempt {numAttempts+1}/{retries} ...")
    if answer is None: raise Exception("Unable to extract answer markdown block from LLM response.")
    if verbose: log_print(f"Problem Solved\nCompleted Reasoning Structure:\n{json.dumps(reasoning,indent=2)}")
    return answer


def __select_gemini(llmConfig: LLMConfig, task: str) -> dict:
    
    prompt = config.SELECT_PHASE_PROMPT_TEMPLATE.format(task=task,modules=utils.rm_list())
    response = gemini.invoke(prompt,api_key=llmConfig.api_key,temp=llmConfig.temp,max_context=llmConfig.context_length)
    selection = utils.extractJSONToDict(response=response)
    return selection
    
def __adapt_gemini(llmConfig: LLMConfig, task: str, reasoning_modules: dict) -> str:
    
    module_list = ""
    for module in reasoning_modules["reasoning_modules"]:
        module_list += f"- {module}\n"
        
    prompt = config.ADAPT_PHASE_PROMPT_TEMPLATE.format(task=task,modules=module_list)
    response = gemini.invoke(prompt,api_key=llmConfig.api_key,temp=llmConfig.temp,max_context=llmConfig.context_length)
    adapted_modules = utils.extractMDBlock(response=response)
    return adapted_modules

def __adapt_local(llmConfig: LLMConfig, task: str, reasoning_modules: dict) -> str:
    module_list = ""
    for module in reasoning_modules["reasoning_modules"]:
        module_list += f"- {module}\n"
        
    prompt = config.ADAPT_PHASE_PROMPT_TEMPLATE.format(task=task,modules=module_list)
    
    prompt,stop = formatPrompt(prompt,llmConfig)
    
    response = localLLM.invoke(
        prompt = prompt,
        gguf_path=llmConfig.gguf_path,
        temp=llmConfig.temp,
        max_context=llmConfig.context_length,
        threads=llmConfig.threads,
        stop=stop
        
    )
    
    adapted_modules = utils.extractMDBlock(response=response)
    return adapted_modules

def __select_local(llmConfig: LLMConfig, task: str) -> dict:
    prompt = config.SELECT_PHASE_PROMPT_TEMPLATE.format(task=task,modules=utils.rm_list())
    
    prompt,stop = formatPrompt(prompt,llmConfig)
    
    response = localLLM.invoke(
        prompt = prompt,
        gguf_path=llmConfig.gguf_path,
        temp=llmConfig.temp,
        max_context=llmConfig.context_length,
        threads=llmConfig.threads,
        stop=stop
        
    )
    selection = utils.extractJSONToDict(response=response)
    return selection