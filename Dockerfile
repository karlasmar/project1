FROM python:3.10-slim

WORKDIR /app

# Install required Python packages
RUN pip install --no-cache-dir torch diffusers transformers accelerate runpod

# Copy your Runpod handler script
COPY rp_handler.py .

# Command to run the API
CMD ["python", "-u", "rp_handler.py"]
