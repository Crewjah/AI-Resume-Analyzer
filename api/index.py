"""Vercel serverless entry point for FastAPI app"""
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure backend modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fastapi import FastAPI, UploadFile, File, Form
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
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
        """Lazy load ResumeAnalyzer to avoid startup failures"""
        global _analyzer
        if _analyzer is None:
            try:
                from backend.resume_analyzer import ResumeAnalyzer
                _analyzer = ResumeAnalyzer()
                logger.info("ResumeAnalyzer initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize ResumeAnalyzer: {e}", exc_info=True)
                raise
        return _analyzer
    
    def extract_text_from_upload(upload: UploadFile) -> str:
        """Extract text from uploaded file"""
        try:
            content = upload.file.read()
            upload.file.seek(0)
            
            if (upload.content_type and "pdf" in upload.content_type) or (upload.filename and upload.filename.lower().endswith(".pdf")):
                reader = PdfReader(io.BytesIO(content))
                pages = []
                for page in reader.pages:
                    try:
                        pages.append(page.extract_text() or "")
                    except Exception as e:
                        logger.warning(f"Error extracting page text: {e}")
                        pages.append("")
                return "\n".join(pages)
            
            # Fallback: try decode as text
            return content.decode("utf-8", errors="ignore")
        except Exception as e:
            logger.error(f"Error extracting text from upload: {e}")
            raise
    
    @app.get("/")
    async def root():
        """API root endpoint"""
        return {"message": "AI Resume Analyzer API", "version": "1.0.0"}
    
    @app.get("/health")
    async def health():
        """Health check endpoint"""
        return {"status": "ok", "healthy": True}
    
    @app.get("/status")
    async def status():
        """Check if analyzer is ready"""
        try:
            analyzer = get_analyzer()
            return {"ready": True, "analyzer": "initialized"}
        except Exception as e:
            logger.error(f"Status check failed: {e}")
            return {"ready": False, "error": str(e)}
    
    @app.post("/api/analyze")
    async def analyze_resume(
        file: UploadFile = File(...),
        job_description: Optional[str] = Form(None),
    ):
        """Analyze resume against optional job description"""
        try:
            resume_text = extract_text_from_upload(file)
            if not resume_text.strip():
                return JSONResponse(
                    status_code=400,
                    content={"error": "Could not read resume file"},
                )
    
            analyzer = get_analyzer()
            result = analyzer.analyze(resume_text)
    
            if job_description:
                result["job_description_length"] = len(job_description.strip())
    
            return {"ok": True, "data": result}
        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"ok": False, "error": str(e)},
            )

except Exception as e:
    logger.error(f"Failed to initialize app: {e}", exc_info=True)
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def error_root():
        return {"error": str(e)}

# Try different ASGI adapters
try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
    logger.info("Using Mangum handler")
except Exception as e:
    logger.warning(f"Mangum failed, using direct ASGI: {e}")
    # Fallback: direct ASGI
    async def handler(scope, receive, send):
        await app(scope, receive, send)



