FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    build-essential \
    libffi-dev \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create working directories
RUN mkdir -p /app/{config,timestamps,emails}
WORKDIR /app

# Copy application code
COPY . .

# Expose ports
EXPOSE 2525 8000

CMD ["python", "main.py"]