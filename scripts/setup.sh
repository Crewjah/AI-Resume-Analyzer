#!/bin/bash

echo "Setting up AI Resume Analyzer..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

echo "Setup complete! Run 'streamlit run app.py' to start the application."
