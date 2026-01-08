"""Vercel ASGI handler for AI Resume Analyzer API"""
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Version
API_VERSION = "2.0"

# Ensure backend modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import io
from PyPDF2 import PdfReader

# Create FastAPI app
app = FastAPI(title="AI Resume Analyzer API", version=API_VERSION)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
assets_path = os.path.join(os.path.dirname(__file__), "..", "assets")
if os.path.exists(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

# Lazy load analyzer with graceful fallback
_analyzer = None
_analyzer_error = None

def get_analyzer():
    """Lazy load ResumeAnalyzer with error handling"""
    global _analyzer, _analyzer_error
    if _analyzer is None and _analyzer_error is None:
        try:
            # Try to import analyzer - it may not work if dependencies are missing
            from backend.resume_analyzer import ResumeAnalyzer
            _analyzer = ResumeAnalyzer()
            logger.info("ResumeAnalyzer initialized successfully")
        except ImportError as e:
            _analyzer_error = f"Analyzer dependencies not available: {e}"
            logger.warning(_analyzer_error)
        except Exception as e:
            _analyzer_error = f"Failed to initialize analyzer: {e}"
            logger.error(_analyzer_error, exc_info=True)
    
    if _analyzer_error:
        raise RuntimeError(_analyzer_error)
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

@app.get("/favicon.ico")
def favicon():
    favicon_path = os.path.join(os.path.dirname(__file__), "..", "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/svg+xml")
    return JSONResponse(status_code=404, content={"error": "Favicon not found"})

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/status")
def status():
    """Check if the analyzer is ready. For Vercel, always return ready since we can do lazy loading."""
    return {"ready": True, "message": "API is operational", "version": API_VERSION}

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
