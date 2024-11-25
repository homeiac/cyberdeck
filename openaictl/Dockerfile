# Use a lightweight Python base image for ARM32v7 architecture
FROM python:3.13.0-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Command to run the interactive CLI
ENTRYPOINT ["python", "cli.py"]
