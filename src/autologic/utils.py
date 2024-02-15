from . import config 
import json
import re
import datetime

def id_to_rm(id: int) -> str:
    try:
        return config.REASONING_MODULES_LIST[id]
    except:
        raise ValueError("Invalid ID")
    pass

def rm_list() -> str: 
    module_list_str = ""
    
    for id, module in enumerate(config.REASONING_MODULES_LIST):
        module_list_str += f"{id}. {module}\n"
        
    return module_list_str

def extractJSONToDict(response: str,language_identifer_optional = True):
    # Define the pattern
    if language_identifer_optional:
        pattern = r"```(?:json)?\s*(.*?)```"
    else: 
        pattern = r"```json\s*(.*?)```"
    matches = re.findall(pattern, response, flags=re.DOTALL)  

    json_str = None
    if matches:
        json_str = matches[0]
    else:
        print("No JSON found in the text.")
        print(json_str)
        raise Exception("No JSON Found")

    selection = None
    if json_str:
        try:
            selection = json.loads(json_str)
        except:
            raise Exception("Unable to instantiate JSON.")
        
    return selection

def extractMDBlock(response: str,language_identifer_optional = True):
    # Define the pattern
    if language_identifer_optional:
        pattern = r"```(?:md)?\s*(.*?)```"
    else: 
        pattern = r"```md\s*(.*?)```"
    matches = re.findall(pattern, response, flags=re.DOTALL)  

    md_str = None
    if matches:
        md_str = matches[0]
    else:
        print("No Markdown found in the text.")
        print(response)
        raise Exception("No markdown Found")

    return md_str

def log_print(msg):
    print(f"{datetime.datetime.now()} | {msg}")