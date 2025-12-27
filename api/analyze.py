from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import io
from PyPDF2 import PdfReader
from mangum import Mangum

from backend.resume_analyzer import ResumeAnalyzer


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

def get_analyzer():
    global _analyzer
    if _analyzer is None:
        _analyzer = ResumeAnalyzer()
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
    return {"ok": True}


# Expose AWS Lambda-style handler for Vercel serverless runtime
handler = Mangum(app)
