#!/usr/bin/env python3
"""
AI Resume Analyzer Backend
Flask-based API for resume analysis with ATS scoring, skills extraction, and job matching.

Usage:
    python backend/app.py              # Run locally on 127.0.0.1:5000
    FLASK_ENV=production python ...    # Production mode
    PORT=8000 python ...               # Custom port
"""

import os
import sys
import logging
import tempfile
from pathlib import Path
from typing import Tuple, Dict, Any

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, InternalServerError

# Try to import CORS support
try:
    from flask_cors import CORS
    HAS_CORS = True
except ImportError:
    HAS_CORS = False

# Setup path for imports
ROOT_DIR = Path(__file__).parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.analyzer import ResumeAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB max file size

# Setup CORS
if HAS_CORS:
    CORS(app, resources={
        r"/analyze": {"origins": "*"},
        r"/health": {"origins": "*"}
    })
else:
    @app.after_request
    def add_cors_headers(response):
        """Add CORS headers manually if flask-cors is not available."""
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept'
        return response


def extract_job_description(req) -> str:
    """
    Extract job description from request (form or JSON).
    
    Args:
        req: Flask request object
        
    Returns:
        Job description string or empty string
    """
    try:
        # Try form data first
        if req.form:
            job_desc = req.form.get('job_description', '')
            if job_desc:
                return job_desc.strip()
        
        # Try JSON data
        json_data = req.get_json(silent=True) or {}
        if isinstance(json_data, dict):
            return json_data.get('job_description', '').strip()
    except Exception as e:
        logger.warning(f"Error extracting job description: {e}")
    
    return ''


def validate_upload(file) -> Tuple[bool, str]:
    """
    Validate uploaded file.
    
    Args:
        file: FileStorage object from request
        
    Returns:
        (is_valid, error_message)
    """
    if not file:
        return False, 'No file provided'
    
    if not file.filename:
        return False, 'No file selected'
    
    # Check file extension
    allowed_extensions = {'pdf', 'docx', 'txt'}
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    
    if ext not in allowed_extensions:
        return False, f'Invalid file type. Allowed: {", ".join(allowed_extensions).upper()}'
    
    return True, ''


@app.route('/health', methods=['GET'])
def health() -> Tuple[Dict[str, Any], int]:
    """
    Health check endpoint.
    
    Returns:
        JSON response with service status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'AI Resume Analyzer',
        'version': '2.0.0',
        'environment': os.environ.get('FLASK_ENV', 'development')
    }), 200


@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze() -> Tuple[Dict[str, Any], int]:
    """
    Analyze a resume and return detailed insights.
    
    Expected multipart/form-data:
    - file: Resume file (PDF, DOCX, or TXT)
    - job_description: (optional) Job description for matching
    
    Returns:
        JSON with analysis results or error message
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return jsonify({}), 204
    
    try:
        # Validate file upload
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided. Please upload a resume.'}), 400
        
        file = request.files['file']
        is_valid, error_msg = validate_upload(file)
        
        if not is_valid:
            logger.warning(f"Invalid upload: {error_msg}")
            return jsonify({'error': error_msg}), 400
        
        logger.info(f"Processing file: {file.filename}")
        
        # Extract job description
        job_description = extract_job_description(request)
        
        # Create temporary file and process
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            file.save(tmp_path)
            
            try:
                # Analyze resume
                analyzer = ResumeAnalyzer()
                resume_text = analyzer.extract_text_from_file(tmp_path)
                
                # Validate extracted text
                if not resume_text or len(resume_text.strip()) < 20:
                    return jsonify({
                        'error': 'Could not extract text from file. Please ensure the file is a valid resume.'
                    }), 400
                
                # Perform analysis
                analysis_result = analyzer.analyze_resume(resume_text, job_description)
                
                logger.info(f"Analysis complete for {file.filename}")
                return jsonify(analysis_result), 200
            
            except Exception as e:
                logger.error(f"Analysis error: {str(e)}", exc_info=True)
                return jsonify({
                    'error': f'Analysis failed: {str(e)}'
                }), 500
            
            finally:
                # Cleanup temporary file
                try:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                except Exception as e:
                    logger.warning(f"Could not delete temp file {tmp_path}: {e}")
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(413)
def request_entity_too_large(e):
    """Handle file size limit exceeded."""
    return jsonify({'error': 'File size exceeds 10 MB limit'}), 413


@app.errorhandler(400)
def bad_request(e):
    """Handle bad request errors."""
    return jsonify({'error': 'Bad request'}), 400


@app.errorhandler(404)
def not_found(e):
    """Handle not found errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    logger.error(f"Internal server error: {str(e)}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Get configuration from environment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting AI Resume Analyzer on 0.0.0.0:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"CORS enabled: {HAS_CORS}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug
    )
