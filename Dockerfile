# 1. Start from an official RunPod base image with PyTorch and CUDA
FROM runpod/pytorch:2.3.0-py3.11-cuda12.1.1-ubuntu22.04

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your handler script
COPY rp_handler.py .

# 6. Set the command to run when the container starts
CMD ["python", "rp_handler.py"]