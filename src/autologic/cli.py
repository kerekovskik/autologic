import argparse
from . import reasoningEngine
import sys 


def inference_entry(args):

    if args.command == 'gemini':
        
        llmConfig = reasoningEngine.LLMConfig(
            context_length=args.context_length,
            api_key=args.api_key,
            temp=args.temp,
            model_type=reasoningEngine.ModelType.GEMINI,
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
            llmConfig=llmConfig,
            verbose = args.verbose,
            retries=args.retries
        )
        print(f"\n\nANSWER: {answer}\n\n")
    else:
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
                        llmConfig=llmConfig,
                        verbose=args.verbose,
                        retries=args.retries
                    )
                    print(f"\n\nANSWER: {answer}\n\n")
            except EOFError:
                print(f"Goodbye!")
                sys.exit(0)



def build_args():
    parser = argparse.ArgumentParser(description='Autologic CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available subcommands')
    
    # Parser for the "upload" subcommand
    gemini_parser = subparsers.add_parser('gemini', help='Use Gemini Pro Model.')
    gemini_parser.add_argument('-c','--context_length',type=int, default=8000, help='Maximum tokens per message.') #
    gemini_parser.add_argument('-v','--verbose',action='store_true', help='Enable verbose output') #
    gemini_parser.add_argument('-p','--prompt',type=str, default=None, help="Prompt for the LLM. If not specified, the program will enter multiline interactive mode.") #
    gemini_parser.add_argument('--temp',type=float, default=0.8, help="Temperature setting for LLM inference.") #
    gemini_parser.add_argument('-a','--api_key',type=str, default=None, help='Gemini Pro API Key. If not specified, it will be read from the GEMINI_PRO_API_KEY environment variable.')
    gemini_parser.add_argument('-r','--retries',type=int, default=5, help='How many times to retry inference on each phase of the self-discover process. Default is 5.')
    gemini_parser.set_defaults(func=inference_entry)

    # Parser for the "download" subcommand
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
    args = parser.parse_args()
    args.func(args)
    
def main():
    build_args()
    
    
if __name__ == "__main__":
    main()