FROM python:3.9-slim

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system deps (optional but safe)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

ENV PYTHONPATH=/app

# Run everything in order
ENTRYPOINT ["./entrypoint.sh"]
