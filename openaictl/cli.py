import openai
from dotenv import load_dotenv
import os

# Load configurations from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL", "gpt-3.5-turbo")  # Default to gpt-3.5-turbo
max_tokens = int(os.getenv("MAX_TOKENS", 150))  # Default to 150 tokens

if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file.")
    exit(1)

# Initialize the OpenAI client
client = openai.Client(api_key=api_key)


def main():
    print("Interactive Chatbot with openaictl")
    print("Type 'exit' to quit.\n")

    # Initialize conversation history
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        # Prompt user for input
        user_input = input("You: ")

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        # Add user's input to the conversation history
        conversation.append({"role": "user", "content": user_input})

        try:
            # Call OpenAI ChatCompletion API using the client
            response = client.chat.completions.create(
                model=model,
                messages=conversation,
                max_tokens=max_tokens
            )

            # Extract the assistant's reply
            assistant_reply = response.choices[0].message.content
            print(f"AI: {assistant_reply}\n")

            # Add the assistant's reply to the conversation history
            conversation.append({"role": "assistant", "content": assistant_reply})

        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
