FROM python:3.10-slim

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application files (leveraging .dockerignore)
COPY . /code

# Create storage directories
RUN mkdir -p /code/uploads /code/models_assets

# Persistent storage volumes for databases and scans
VOLUME ["/code/uploads", "/code/database.db"]

# Expose server port (Hugging Face default 7860 / standard 8000)
EXPOSE 7860

# Container Health Probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/health')" || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
