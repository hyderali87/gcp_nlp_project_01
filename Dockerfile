FROM python:3.11-slim

WORKDIR /app

# System deps (often needed for tokenizers / torch runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY pipeline/ pipeline/

# This image is used by pipeline components; entrypoint not required.
CMD ["python", "-c", "print('NLP translation image ready')"]
