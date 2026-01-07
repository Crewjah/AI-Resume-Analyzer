"""Vercel ASGI handler for AI Resume Analyzer API"""
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure backend modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from typing import Optional
import io
from PyPDF2 import PdfReader

# Create FastAPI app
app = FastAPI(title="AI Resume Analyzer API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy load analyzer
_analyzer = None

def get_analyzer():
    """Lazy load ResumeAnalyzer"""
    global _analyzer
    if _analyzer is None:
        try:
            from backend.resume_analyzer import ResumeAnalyzer
            _analyzer = ResumeAnalyzer()
            logger.info("ResumeAnalyzer initialized")
        except Exception as e:
            logger.error(f"Failed to init analyzer: {e}", exc_info=True)
            raise
    return _analyzer

def extract_text_from_upload(upload: UploadFile) -> str:
    """Extract text from file"""
    content = upload.file.read()
    upload.file.seek(0)
    
    if (upload.content_type and "pdf" in upload.content_type) or (upload.filename and upload.filename.lower().endswith(".pdf")):
        reader = PdfReader(io.BytesIO(content))
        pages = []
        for page in reader.pages:
            try:
                pages.append(page.extract_text() or "")
            except:
                pages.append("")
        return "\n".join(pages)
    
    return content.decode("utf-8", errors="ignore")

@app.get("/")
def root():
    try:
        index_path = os.path.join(os.path.dirname(__file__), "..", "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()
        return HTMLResponse(content=html, status_code=200)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to load homepage: {e}"})

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/status")
def status():
    try:
        analyzer = get_analyzer()
        return {"ready": True}
    except Exception as e:
        return {"ready": False, "error": str(e)}

@app.post("/api/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
):
    try:
        resume_text = extract_text_from_upload(file)
        if not resume_text.strip():
            return JSONResponse(status_code=400, content={"error": "Could not read file"})

        analyzer = get_analyzer()
        result = analyzer.analyze(resume_text)

        if job_description:
            result["job_description_length"] = len(job_description.strip())

        return {"ok": True, "data": result}
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"ok": False, "error": str(e)})
