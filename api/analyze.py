"""
Vercel Serverless API for Resume Analysis
Handles POST /api/analyze requests with multipart/form-data (file + job_description)
"""

import os
import sys
import json
import tempfile
from typing import Tuple, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyzer import ResumeAnalyzer

# Initialize analyzer once (cached across cold starts)
analyzer = ResumeAnalyzer()


def handler(request) -> Tuple[Dict[str, Any], int]:
    """
    Vercel serverless function handler.
    Expects: multipart/form-data with 'file' (resume) and optional 'job_description'
    Returns: JSON with analysis results or error
    """
    
    # Handle CORS
    if request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
        }, 200
    
    # Only POST allowed
    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Method not allowed. Use POST."}),
        }, 405
    
    try:
        # Get file from request
        if "file" not in request.files:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "No file provided. Please upload a resume."}),
            }, 400
        
        file = request.files["file"]
        
        if not file or file.filename == "":
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "No file selected."}),
            }, 400
        
        # Validate file extension
        allowed_extensions = {"pdf", "docx", "txt"}
        filename = file.filename.lower()
        if not any(filename.endswith(f".{ext}") for ext in allowed_extensions):
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": f"Invalid file type. Allowed: {', '.join(allowed_extensions).upper()}"}),
            }, 400
        
        # Get optional job description
        job_description = request.form.get("job_description", "").strip() if request.form else ""
        
        # Save file to temp location and analyze
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
            tmp_path = tmp_file.name
            file.save(tmp_path)
            
            try:
                # Extract text
                resume_text = analyzer.extract_text_from_file(tmp_path)
                
                # Analyze
                results = analyzer.analyze_resume(resume_text, job_description)
                
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps(results),
                }, 200
            
            except Exception as e:
                return {
                    "statusCode": 500,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": f"Analysis failed: {str(e)}"}),
                }, 500
            
            finally:
                # Clean up temp file
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
    
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"}),
        }, 500
