import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def main():

    function_responses = []
    loop_limit = 20
    count = 0

    if len(sys.argv) == 1:
        print("no prompt found")
        sys.exit(1)
    else:

        for arg in sys.argv:
            if not arg.startswith("--"):
                user_prompt = arg

        verbose = "--verbose" in sys.argv

        messages = [
                types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]

        while count <= loop_limit:

            function_call_present = False
            
            try:
                response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),)

 #               if available_functions not in response.candidates and (response.text != None or response != ""):
 #                   print("Final response:")
 #                   print(f"{response.text}")
 #                   break

                for candidate in response.candidates:
                    for part in candidate.content.parts:
                        if part.function_call != None:
                            function_call_present = True
                            break

                if (not function_call_present) and response.text:
                    print("Final response:")
                    print(response.text)
                    break

                for candidate in response.candidates:
                    messages.append(candidate.content)

                if response.function_calls is not None:
                    for function_call_part in response.function_calls:
                        function_call_result = call_function(function_call_part, verbose)
                        if (
                            not function_call_result.parts
                            or not function_call_result.parts[0].function_response
                        ):
                            raise Exception("empty function call result")
                        if verbose:
                            print(f"-> {function_call_result.parts[0].function_response}")
                        function_responses.append(function_call_result.parts[0])

                    if not function_responses:
                        raise Exception("no function responses generated, exiting.")
                    
                    messages.append(
                        types.Content(role="user", parts=function_responses)
                    )
                    
            except Exception as e:
                print(f"Error: {e}")
                
            count += 1


'''
        print(response.text)


        if is_verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
'''

if __name__ == "__main__":
    main()
