FROM python:3.11-slim

WORKDIR /app

# Install system deps for python-docx and other libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev libxslt1-dev zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

ENV PORT=8000

EXPOSE ${PORT}

# Use gunicorn to serve the Flask app
CMD ["gunicorn", "api.index:app", "--bind", "0.0.0.0:8000", "--workers", "2"]
