#!/bin/bash

# Install system dependencies
apt-get update
apt-get install -y python3-pip

# Install Python dependencies
pip install -r requirements.txt

# Download SpaCy model
python -m spacy download en_core_web_sm
