import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt 
from call_function import available_functions, call_function

MAX_ITERATIONS = 20

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
    
    for _ in range(MAX_ITERATIONS):
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
        
        # 1. Record the assistant's turn first (it carries any tool calls).
        message = response.choices[0].message
        messages.append(message)

        # 2. No tool calls means the model is done: print the answer and stop.
        if not message.tool_calls:
            print("Final response:")
            print(message.content)
            return

        # 3. Run each requested tool and append one tool message per call.
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)
            if not result_message.get("content"):
                raise RuntimeError(f"Empty result from {tool_call.function.name}")
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)

    # Only reached if all iterations ran without a final response.
    print(f"Error: agent did not produce a final response within {MAX_ITERATIONS} iterations")
    sys.exit(1)


if __name__ == "__main__":
    main()