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
from fastapi.responses import JSONResponse, HTMLResponse
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
            # Import clean analyzer
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

# Static favicon is served by Vercel from /public; no API route needed.

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/status")
def status():
    """Check if the analyzer is ready. For Vercel, always return ready since we can do lazy loading."""
    return {"ready": True, "message": "API is operational", "version": API_VERSION}

@app.get("/analyze")
def analyze_page():
    """Serve upload interface for resume analysis"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload Resume - AI Resume Analyzer</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', -apple-system, sans-serif;
                background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                max-width: 600px;
                width: 100%;
                background: white;
                border-radius: 20px;
                padding: 48px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
            }
            h1 { color: #2563EB; margin-bottom: 12px; font-size: 2rem; }
            .subtitle { color: #6B7280; margin-bottom: 32px; }
            .upload-area {
                border: 3px dashed #2563EB;
                border-radius: 12px;
                padding: 48px 24px;
                text-align: center;
                background: #F0F9FF;
                cursor: pointer;
                transition: all 0.3s;
                margin-bottom: 24px;
            }
            .upload-area:hover { background: #DBEAFE; transform: scale(1.02); }
            .upload-icon { font-size: 3rem; margin-bottom: 16px; }
            input[type="file"] { display: none; }
            .btn {
                width: 100%;
                padding: 14px;
                background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4); }
            .btn:disabled { opacity: 0.5; cursor: not-allowed; }
            #fileName { margin: 16px 0; font-size: 0.9rem; color: #10B981; font-weight: 600; }
            .back-link { text-align: center; margin-top: 24px; }
            .back-link a { color: #2563EB; text-decoration: none; font-weight: 600; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 Upload Your Resume</h1>
            <p class="subtitle">Get instant analysis and actionable feedback</p>
            
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                    <div class="upload-icon">📤</div>
                    <p style="color: #2563EB; font-weight: 600;">Click to upload or drag & drop</p>
                    <p style="color: #6B7280; font-size: 0.875rem; margin-top: 8px;">PDF or TXT (max 5MB)</p>
                </div>
                <input type="file" id="fileInput" accept=".pdf,.txt" required>
                <div id="fileName"></div>
                <button type="submit" class="btn" id="analyzeBtn" disabled>Analyze Resume</button>
            </form>
            
            <div class="back-link">
                <a href="/">← Back to Home</a>
            </div>
        </div>
        
        <script>
            const fileInput = document.getElementById('fileInput');
            const fileName = document.getElementById('fileName');
            const analyzeBtn = document.getElementById('analyzeBtn');
            const uploadForm = document.getElementById('uploadForm');
            
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    fileName.textContent = `✓ ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
                    analyzeBtn.disabled = false;
                }
            });
            
            uploadForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const file = fileInput.files[0];
                if (!file) return;
                
                analyzeBtn.disabled = true;
                analyzeBtn.textContent = 'Analyzing...';
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const response = await fetch('/api/analyze', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.ok) {
                        displayResults(result.data);
                    } else {
                        alert('Error: ' + (result.error || 'Analysis failed'));
                        analyzeBtn.disabled = false;
                        analyzeBtn.textContent = 'Analyze Resume';
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                    analyzeBtn.disabled = false;
                    analyzeBtn.textContent = 'Analyze Resume';
                }
            });
            
            function displayResults(data) {
                const scores = data.scores || {};
                const html = `
                    <h2 style="color: #2563EB; margin: 32px 0 16px;">Analysis Results</h2>
                    <div style="background: #F0F9FF; padding: 24px; border-radius: 12px; margin-bottom: 16px;">
                        <h3 style="color: #1F2937; margin-bottom: 16px;">Scores</h3>
                        <p><strong>Overall:</strong> ${scores.overall_score || 0}%</p>
                        <p><strong>Content Quality:</strong> ${scores.content_quality || 0}%</p>
                        <p><strong>ATS Compatibility:</strong> ${scores.ats_compatibility || 0}%</p>
                        <p><strong>Keyword Optimization:</strong> ${scores.keyword_optimization || 0}%</p>
                    </div>
                    <button class="btn" onclick="location.reload()">Analyze Another</button>
                `;
                document.querySelector('.container').innerHTML = html;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)

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
