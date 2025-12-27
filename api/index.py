"""Vercel serverless entry point for FastAPI app"""
import sys
import os

# Ensure backend modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from mangum import Mangum

# Create minimal app to test handler
app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "AI Resume Analyzer API"}

# Export handler for Vercel
handler = Mangum(app, lifespan="off")

