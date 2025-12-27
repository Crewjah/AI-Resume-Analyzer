"""Vercel ASGI handler - ultra minimal test"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Vercel"}

@app.get("/health")
def health():
    return {"status": "ok"}
