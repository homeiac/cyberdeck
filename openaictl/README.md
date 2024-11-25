
# openaictl: Interactive OpenAI Chatbot CLI

**openaictl** is an interactive command-line chatbot built with Python. It communicates with OpenAI's GPT model using the new client-based interface (`openai-python>=1.0.0`). The chatbot supports conversational context, enabling dynamic and intelligent interactions.

---

## Features

- **Interactive Chat**: Engage in real-time conversations with OpenAI's GPT model.
- **Context-Aware**: Maintains conversation history for context-based responses.
- **Customizable**: Configure model, token limits, and API key via the `.env` file.
- **Secure API Key Handling**: Loads OpenAI API key and other configurations from the `.env` file.
- **Dockerized**: Fully containerized for ease of use across different systems and architectures.

---

## Prerequisites

1. **Python**: Ensure Python 3.9 or newer is installed if not using Docker.
2. **Docker**: Install Docker for containerized execution.
3. **OpenAI API Key**: Obtain an API key from [OpenAI](https://platform.openai.com/signup/).

---

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### Python Setup (Optional)

If running locally (not with Docker):

1. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Configuration

1. **Create a `.env` File**:
   Add the following configuration to a `.env` file in the project directory:

   ```dotenv
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL=gpt-3.5-turbo
   MAX_TOKENS=150
   ```

   - `OPENAI_API_KEY`: Your OpenAI API key.
   - `MODEL`: The OpenAI model to use (e.g., `gpt-4`, `gpt-3.5-turbo`).
   - `MAX_TOKENS`: Maximum number of tokens per response.

---

## Usage

### Docker

1. **Build the Docker Image**:

   ```bash
   docker build -t openaictl .
   ```

2. **Run the Chatbot**:

   ```bash
   docker run --rm -it --env-file .env openaictl
   ```

### Local Python Execution

Run the chatbot interactively:

```bash
python cli.py
```

---

## Example Interaction

```plaintext
Interactive Chatbot with OpenAI (Client-Based API)
Type 'exit' to quit.

You: Hello
AI: Hi there! How can I assist you today?

You: What's the capital of France?
AI: The capital of France is Paris.

You: exit
Goodbye!
```

---

## Instructions for Building for Raspberry Pi 2 on a Mac

The Raspberry Pi 2 has an ARMv7 architecture, so you need to ensure the Docker image is compatible with that architecture. Here's how you can build and run openaictl for a Raspberry Pi 2 on a Mac (including Apple Silicon).

### Steps to Build and Run

1. **Enable Buildx on Docker**:
   - Ensure Docker's `buildx` feature is enabled for multi-platform builds. You can check with:

     ```bash
     docker buildx version
     ```

   - If not enabled, install it using Docker's official instructions: [Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/).

2. **Set Up QEMU for Cross-Platform Emulation**:
   - If you haven’t already, set up QEMU for multi-architecture emulation:

     ```bash
     docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
     ```

3. **Build the Docker Image for ARMv7**:
   - Use `buildx` to target the Raspberry Pi 2 architecture (`linux/arm/v7`):

     ```bash
     docker buildx build --platform linux/arm/v7 -t openaictl:rpi2 .
     ```

4. **Save the Image for Transfer (Optional)**:
   - If building the image on your Mac and transferring it to the Raspberry Pi 2, save the image as a tar file:

     ```bash
     docker save -o openaictl-rpi2.tar openaictl:rpi2
     ```

5. **Transfer the Image to Raspberry Pi 2**:
   - Copy the image file to the Raspberry Pi using `scp` or another file transfer method:

     ```bash
     scp openaictl-rpi2.tar pi@<RPI_IP>:/home/pi
     ```

6. **Load and Run the Image on Raspberry Pi 2**:
   - SSH into the Raspberry Pi:

     ```bash
     ssh pi@<RPI_IP>
     ```

   - Load the Docker image:

     ```bash
     docker load < openaictl-rpi2.tar
     ```

   - Run the chatbot:

     ```bash
     docker run --rm -it --env-file .env openaictl:rpi2
     ```

7. **Direct Deployment to Raspberry Pi (Alternative)**:
   - If the Raspberry Pi is network-accessible, you can build and push directly to it:

     ```bash
     docker buildx build --platform linux/arm/v7 -t openaictl:rpi2 --push .
     ```

---

## Key Files

- **`cli.py`**: Main script for the chatbot.
- **`Dockerfile`**: Configuration for building the Docker image.
- **`requirements.txt`**: Python dependencies.
- **`.env`**: Configuration file for the API key, model, and other parameters.

---

## Dependencies

- [openai](https://github.com/openai/openai-python) `>=1.0.0`
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## Troubleshooting

### Missing API Key

Ensure the `.env` file is properly configured with the `OPENAI_API_KEY`.

### Other Errors

Check your `.env` file for incorrect values or run the script with debug logging to identify the issue.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [OpenAI Python Library](https://github.com/openai/openai-python)
- [Docker](https://www.docker.com/)
