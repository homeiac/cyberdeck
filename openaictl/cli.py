import shutil
import subprocess
import openai
from dotenv import load_dotenv
import os
import readline
import atexit

# Load configurations from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL", "gpt-3.5-turbo")  # Default to gpt-3.5-turbo
max_tokens = int(os.getenv("MAX_TOKENS", 150))  # Default to 150 tokens
history_file = os.getenv("HISTORY_FILE", "/history/.openaictl_history")  # Default history file path inside the container

if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file.")
    exit(1)

# Initialize the OpenAI client
client = openai.Client(api_key=api_key)

# Load history from file
if os.path.exists(history_file):
    readline.read_history_file(history_file)

# Save history to file on exit
atexit.register(readline.write_history_file, history_file)


def get_terminal_height():
    """Get the terminal height dynamically."""
    try:
        return shutil.get_terminal_size().lines
    except OSError:
        return 24  # Default terminal height if not detected


def display_with_pager(output):
    """Display output using 'less' with conditional auto-quit."""
    lines = output.splitlines()
    terminal_height = get_terminal_height()

    # Add -F (auto-quit) if the output fits on one screen
    less_flags = ['-R']
    if len(lines) <= terminal_height - 2:  # Reserve 2 lines for prompt space
        less_flags.append('-F')

    try:
        process = subprocess.Popen(['less'] + less_flags, stdin=subprocess.PIPE, text=True)
        process.communicate(input=output)
    except subprocess.SubprocessError as e:
        print(f"Error while using less: {e}")


def main():
    print("Interactive Chatbot with openaictl")
    print("Type 'exit' to quit.\n")

    # Initialize conversation history
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        try:
            # Prompt user for input
            user_input = input("You: ")

            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            # Add user's input to the conversation history
            conversation.append({"role": "user", "content": user_input})

            # Call OpenAI ChatCompletion API using the client
            response = client.chat.completions.create(
                model=model,
                messages=conversation,
                max_tokens=max_tokens
            )

            # Extract the assistant's reply
            assistant_reply = response.choices[0].message.content
            print(f"AI: {assistant_reply}\n")
            display_with_pager(assistant_reply)  # Paginate the output with 'less'

            # Add the assistant's reply to the conversation history
            conversation.append({"role": "assistant", "content": assistant_reply})

        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
