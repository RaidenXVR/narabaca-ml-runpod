FROM python:3.10-slim

# Avoid interactive prompts during pip installs
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies early for caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app source code
COPY . .

# Expose port if testing locally (not needed for RunPod)
EXPOSE 8000

# Start the RunPod serverless function
CMD ["python", "rp_handler.py"]
