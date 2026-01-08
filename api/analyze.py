from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import io
import traceback
from pypdf import PdfReader
from mangum import Mangum

try:
    from backend.resume_analyzer import ResumeAnalyzer
except ImportError as e:
    print(f"Warning: Could not import ResumeAnalyzer: {e}")
    ResumeAnalyzer = None


app = FastAPI(title="AI Resume Analyzer API", version="1.0.0")

# Open CORS for local dev convenience; Vercel will serve same-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy initialization to avoid startup errors
_analyzer = None
_analyzer_error = None

def get_analyzer():
    global _analyzer, _analyzer_error
    if _analyzer is None and _analyzer_error is None:
        try:
            if ResumeAnalyzer is None:
                raise ImportError("ResumeAnalyzer not available")
            _analyzer = ResumeAnalyzer()
        except Exception as e:
            _analyzer_error = str(e)
            traceback.print_exc()
            raise
    if _analyzer_error:
        raise RuntimeError(f"Analyzer init failed: {_analyzer_error}")
    return _analyzer




def _extract_text_from_upload(upload: UploadFile) -> str:
    content = upload.file.read()
    # Reset file pointer for safety in case of reuse
    upload.file.seek(0)
    if (upload.content_type and "pdf" in upload.content_type) or upload.filename.lower().endswith(".pdf"):
        reader = PdfReader(io.BytesIO(content))
        pages = []
        for page in reader.pages:
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
        return "\n".join(pages)
    # Fallback: try decode as text
    try:
        return content.decode("utf-8", errors="ignore")
    except Exception:
        return ""


@app.post("/")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
):
    try:
        resume_text = _extract_text_from_upload(file)
        if not resume_text.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Could not read resume file. Please upload a valid PDF or text file."},
            )

        analyzer = get_analyzer()
        result = analyzer.analyze(resume_text)

        # Optionally echo job description back (not used in scoring yet)
        if job_description:
            result["job_description_length"] = len(job_description.strip())

        return {"ok": True, "data": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"ok": False, "error": str(e)})


@app.get("/health")
async def health():
    """Simple health check endpoint"""
    return {"ok": True, "status": "healthy"}


@app.get("/status")
async def status():
    """API status with analyzer initialization status"""
    try:
        analyzer = get_analyzer()
        return {"ok": True, "analyzer_ready": True}
    except Exception as e:
        return {"ok": False, "analyzer_ready": False, "error": str(e)}


# Expose AWS Lambda-style handler for Vercel serverless runtime
handler = Mangum(app)
