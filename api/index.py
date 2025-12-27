"""Vercel serverless entry point for FastAPI app"""
import sys
import os

# Ensure backend modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.analyze import app
from mangum import Mangum

# Export handler for Vercel
handler = Mangum(app, lifespan="off")
