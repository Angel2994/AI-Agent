import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt 
from call_function import available_functions, call_function

def main():
    
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    #Parse user message
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    #Create client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    ## Create messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    
    #Create model response
    response = client.chat.completions.create(
        model="openrouter/free",
        messages= messages,
        tools = available_functions
    )
    
    prompt_tokens = response.usage.prompt_tokens
    completions_tokens = response.usage.completion_tokens
    if not completions_tokens:
        raise ValueError("Response failed try again")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {completions_tokens}")
        
    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)
            if not result_message.get("content"):
                raise RuntimeError(f"Empty result from {tool_call.function.name}")
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print(response.choices[0].message.content)


if __name__ == "__main__":
    main()