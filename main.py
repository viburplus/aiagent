import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():

    if len(sys.argv) == 1:
        print("no prompt found")
        sys.exit(1)
    else:

        for arg in sys.argv:
            if not arg.startswith("--"):
                user_prompt = arg

        is_verbose = "--verbose" in sys.argv

        messages = [
                types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]

        response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt),)

        print(response.text)

        if is_verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
