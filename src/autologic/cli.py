import argparse
from . import reasoningEngine
import sys 

def interactiveMode(discoverLLMConfig: reasoningEngine.LLMConfig, solveLLMConfig: reasoningEngine.LLMConfig,verbose: bool = False, retries: int = 5):
    print(f"\nEntering Interactive Mode: CTRL + C to send multi-line input. CTRL + D to exit the program.")
    while True:
        try:
            lines = []
            while True:
                line = input("> ")
                lines.append(line)
        except KeyboardInterrupt:
            if lines:
                prompt = "\n".join(lines)
                print(f"\nThinking...")
                answer = reasoningEngine.solve(
                    task=prompt,
                    discover_config=discoverLLMConfig,
                    solve_config=solveLLMConfig,
                    verbose=verbose,
                    retries=retries
                )
                print(f"\n\nANSWER: {answer}\n\n")
        except EOFError:
            print(f"Goodbye!")
            sys.exit(0)    

def mixed_inference(args):
    # Construct LLMConfig for the discover stage. 
    print(args)
    if args.discover_model_type == "gemini":
        discoverLLMConfig = reasoningEngine.LLMConfig(
            context_length=args.discover_context_length,
            api_key=args.discover_api_key,
            temp=args.discover_temp,
            model_type=reasoningEngine.ModelType.GEMINI,
        )
    elif args.discover_model_type == "openai":
        discoverLLMConfig = reasoningEngine.LLMConfig(
            context_length=args.discover_context_length,
            api_key=args.discover_api_key,
            temp=args.discover_temp,
            model_type=reasoningEngine.ModelType.OPENAI,
            model_name=args.discover_model_name
        )
    elif args.discover_model_type == "local":
        chat_template = None
        if args.discover_format == 'mixtral_instruct':
            chat_template = reasoningEngine.ChatTemplate.MIXTRAL_INSTRUCT
        elif args.discover_format == "zephyr":
            chat_template = reasoningEngine.ChatTemplate.ZEPHYR
        elif args.discover_format == "chatml":
            chat_template = reasoningEngine.ChatTemplate.CHATML
        else:
            ValueError("Invalid Chat Template Type!")
            
        discoverLLMConfig = reasoningEngine.LLMConfig(
            gguf_path = args.discover_gguf_path,
            context_length=args.discover_context_length,
            temp=args.discover_temp,
            model_type=reasoningEngine.ModelType.LOCAL,
            chat_template=chat_template,
            threads=args.discover_threads,
        )
    else:
        TypeError("Invalid Discover Model Type!")
    
    
    solveLLMConfig = None
    ## Construct LLMConfig for the solve stage. 
    if args.solve_model_type is None:
        solveLLMConfig = discoverLLMConfig
    elif args.solve_model_type == "gemini":
        solveLLMConfig = reasoningEngine.LLMConfig(
            context_length=args.solve_context_length,
            api_key=args.solve_api_key,
            temp=args.solve_temp,
            model_type=reasoningEngine.ModelType.GEMINI,
        )
    elif args.solve_model_type == "openai":
        solveLLMConfig = reasoningEngine.LLMConfig(
            context_length=args.solve_context_length,
            api_key=args.solve_api_key,
            temp=args.solve_temp,
            model_type=reasoningEngine.ModelType.OPENAI,
            model_name=args.solve_model_name
        )
    elif args.solve_model_type == "local":
        chat_template = None
        if args.solve_format == 'mixtral_instruct':
            chat_template = reasoningEngine.ChatTemplate.MIXTRAL_INSTRUCT
        elif args.solve_format == "zephyr":
            chat_template = reasoningEngine.ChatTemplate.ZEPHYR
        elif args.solve_format == "chatml":
            chat_template = reasoningEngine.ChatTemplate.CHATML
        else:
            ValueError("Invalid Chat Template Type!")
            
        solveLLMConfig = reasoningEngine.LLMConfig(
            gguf_path = args.solve_gguf_path,
            context_length=args.solve_context_length,
            temp=args.solve_temp,
            model_type=reasoningEngine.ModelType.LOCAL,
            chat_template=chat_template,
            threads=args.solve_threads,
        )
    else:
        TypeError("Invalid Solve Model Type!")
        
    
    if args.prompt:
        print("Thinking...")
        answer = reasoningEngine.solve(
            task=args.prompt,
            discover_config=discoverLLMConfig,
            solve_config=solveLLMConfig,
            verbose = args.verbose,
            retries=args.retries
        )
        print(f"\n\nANSWER: {answer}\n\n")
    else:
        interactiveMode(discoverLLMConfig=discoverLLMConfig,solveLLMConfig=solveLLMConfig,verbose=args.verbose,retries=args.retries)


def inference_entry(args):

    if args.command == 'gemini':
        
        llmConfig = reasoningEngine.LLMConfig(
            context_length=args.context_length,
            api_key=args.api_key,
            temp=args.temp,
            model_type=reasoningEngine.ModelType.GEMINI,
        )
    elif args.command == "openai":
        llmConfig = reasoningEngine.LLMConfig(
            context_length=args.context_length,
            api_key=args.api_key,
            temp=args.temp,
            model_type=reasoningEngine.ModelType.OPENAI,
            model_name=args.model_name
        )
    else: 
        chat_template = None
        if args.format == 'mixtral_instruct':
            chat_template = reasoningEngine.ChatTemplate.MIXTRAL_INSTRUCT
        elif args.format == "zephyr":
            chat_template = reasoningEngine.ChatTemplate.ZEPHYR
        elif args.format == "chatml":
            chat_template = reasoningEngine.ChatTemplate.CHATML
        else:
            ValueError("Invalid Chat Template Type!")
            
        llmConfig = reasoningEngine.LLMConfig(
            gguf_path = args.gguf_path,
            context_length=args.context_length,
            temp=args.temp,
            model_type=reasoningEngine.ModelType.LOCAL,
            chat_template=chat_template,
            threads=args.threads,
            
        )
    
    if args.prompt:
        print("Thinking...")
        answer = reasoningEngine.solve(
            task=args.prompt,
            discover_config=llmConfig,
            verbose = args.verbose,
            retries=args.retries
        )
        print(f"\n\nANSWER: {answer}\n\n")
    else:
        interactiveMode(discoverLLMConfig=llmConfig,solveLLMConfig=llmConfig,verbose=args.verbose,retries=args.retries)



def build_args():
    parser = argparse.ArgumentParser(description='Autologic CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available subcommands')
    
    # Parser for the "gemini" subcommand
    gemini_parser = subparsers.add_parser('gemini', help='Use Gemini Pro Model.')
    gemini_parser.add_argument('-c','--context_length',type=int, default=8000, help='Maximum tokens per message.') #
    gemini_parser.add_argument('-v','--verbose',action='store_true', help='Enable verbose output') #
    gemini_parser.add_argument('-p','--prompt',type=str, default=None, help="Prompt for the LLM. If not specified, the program will enter multiline interactive mode.") #
    gemini_parser.add_argument('--temp',type=float, default=0.8, help="Temperature setting for LLM inference.") #
    gemini_parser.add_argument('-a','--api_key',type=str, default=None, help='Gemini Pro API Key. If not specified, it will be read from the GEMINI_PRO_API_KEY environment variable.')
    gemini_parser.add_argument('-r','--retries',type=int, default=5, help='How many times to retry inference on each phase of the self-discover process. Default is 5.')
    gemini_parser.set_defaults(func=inference_entry)

    # Parser for the "openai" subcommand
    openai_parser = subparsers.add_parser('openai', help='Use OpenAI Models.')
    openai_parser.add_argument('-c','--context_length',type=int, default=2000, help='Maximum tokens per message.') #
    openai_parser.add_argument('-v','--verbose',action='store_true', help='Enable verbose output') #
    openai_parser.add_argument('-p','--prompt',type=str, default=None, help="Prompt for the LLM. If not specified, the program will enter multiline interactive mode.") #
    openai_parser.add_argument('--temp',type=float, default=0.8, help="Temperature setting for LLM inference.") #
    openai_parser.add_argument('-a','--api_key',type=str, default=None, help='OpenAI API Key. If not specified, it will be read from the AUTOLOGIC_OPENAI_API_KEY environment variable.')
    openai_parser.add_argument('-r','--retries',type=int, default=5, help='How many times to retry inference on each phase of the self-discover process. Default is 5.')
    openai_parser.add_argument('-m','--model_name',type=str, default=None, help="OpenAI Model Name.") #
    openai_parser.set_defaults(func=inference_entry)

    # Parser for the "local" subcommand
    local_parser = subparsers.add_parser('local', help='Use a local model with llama-cpp-python.')
    local_parser.add_argument('-c','--context_length',type=int, default=8000, help='Maximum tokens per message.') #
    local_parser.add_argument('-v','--verbose',action='store_true', help='Enable verbose output') #
    local_parser.add_argument('-p','--prompt',type=str, default=None, help="Prompt for the LLM. If not specified, the program will enter multiline interactive mode.") #
    local_parser.add_argument('--temp',type=float, default=0.8, help="Temperature setting for LLM inference.") #
    local_parser.add_argument('-g','--gguf_path',type=str,required=True,help="Path to GGUF Model file.")
    local_parser.add_argument('-t','--threads',type=int,default=4,help="Number of Threads use with llama.cpp.")
    local_parser.add_argument('-l','--layers',type=int,default=-1,help="Number of layers to offload to GPU. -1 = as many as possible.")
    local_parser.add_argument('-f', '--format', choices=['mixtral_instruct','zephyr','chatml'], default='mixtral_instruct', help='Chat Template Format (default: mixtral_instruct)')
    local_parser.add_argument('-r','--retries',type=int, default=5, help='How many times to retry inference on each phase of the self-discover process. Default is 5.')
    local_parser.set_defaults(func=inference_entry)
    
    # Mixed Mode 
    mixed_parser = subparsers.add_parser('mixed', help='Use different models for discover and solve')
    mixed_parser.add_argument('-v','--verbose',action='store_true', help='Enable verbose output') #
    mixed_parser.add_argument('-p','--prompt',type=str, default=None, help="Prompt for the LLM. If not specified, the program will enter multiline interactive mode.") 
    mixed_parser.add_argument('-r','--retries',type=int, default=5, help='How many times to retry inference on each phase of the self-discover process. Default is 5.')
    
    mixed_parser_discover_group = mixed_parser.add_argument_group('Discovery Options') 
    mixed_parser_discover_group.add_argument('--discover-context_length',type=int, default=2000, help='Maximum tokens per message.')
    mixed_parser_discover_group.add_argument('--discover-temp',type=float, default=0.8, help="Temperature setting for LLM inference.") #
    mixed_parser_discover_group.add_argument('--discover-api_key',type=str, default=None, help='Gemini/OpenAI API Key. If not specified, it will be read from the environment.')
    mixed_parser_discover_group.add_argument('--discover-model_name',type=str, default=None, help="OpenAI/Gemini Model Name.") #
    mixed_parser_discover_group.add_argument('--discover-gguf_path',type=str,help="Path to GGUF Model file.")
    mixed_parser_discover_group.add_argument('--discover-threads',type=int,default=4,help="Number of Threads use with llama.cpp.")
    mixed_parser_discover_group.add_argument('--discover-layers',type=int,default=-1,help="Number of layers to offload to GPU. -1 = as many as possible.")
    mixed_parser_discover_group.add_argument('--discover-format', choices=['mixtral_instruct','zephyr','chatml'], default='mixtral_instruct', help='Chat Template Format (default: mixtral_instruct)')
    mixed_parser_discover_group.add_argument('--discover-model_type', choices=['openai','gemini','local'], default='gemini', help='Model type (default: gemini)')
    mixed_parser_discover_group.add_argument('--discover_threads',type=int,default=4,help="Number of Threads use with llama.cpp.")

    mixed_parser_solve_group = mixed_parser.add_argument_group('Solve Options')
    mixed_parser_solve_group.add_argument('--solve-context_length',type=int, default=2000, help='Maximum tokens per message.')
    mixed_parser_solve_group.add_argument('--solve-temp',type=float, default=0.8, help="Temperature setting for LLM inference.") #
    mixed_parser_solve_group.add_argument('--solve-api_key',type=str, default=None, help='Gemini/OpenAI API Key. If not specified, it will be read from the environment.')
    mixed_parser_solve_group.add_argument('--solve-model_name',type=str, default=None, help="OpenAI/Gemini Model Name.") #
    mixed_parser_solve_group.add_argument('--solve-gguf_path',type=str,help="Path to GGUF Model file.")
    mixed_parser_solve_group.add_argument('--solve-threads',type=int,default=4,help="Number of Threads use with llama.cpp.")
    mixed_parser_solve_group.add_argument('--solve-layers',type=int,default=-1,help="Number of layers to offload to GPU. -1 = as many as possible.")
    mixed_parser_solve_group.add_argument('--solve-format', choices=['mixtral_instruct','zephyr','chatml'], default='mixtral_instruct', help='Chat Template Format (default: mixtral_instruct)')
    mixed_parser_solve_group.add_argument('--solve-model_type', choices=['openai','gemini','local'], default=None, help='')
    mixed_parser_solve_group.add_argument('--solve_threads',type=int,default=4,help="Number of Threads use with llama.cpp.")
    mixed_parser.set_defaults(func=mixed_inference)
    args = parser.parse_args()
    args.func(args)
    
def main():
    build_args()
    
    
if __name__ == "__main__":
    main()