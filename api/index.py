from flask import Flask, request, jsonify, render_template_string
import os
import sys
import tempfile
from src.analyzer import ResumeAnalyzer

app = Flask(__name__)

# Clean, professional HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Resume Analyzer</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">AI Resume Analyzer</h1>
            <p style="color: #9fb0c8; font-size: 1rem; margin-top: 6px;">
                Clean, accurate resume parsing — PDF, DOCX, TXT
            </p>
        </div>
        
        <div class="upload-section">
            <div class="upload-area">
                <h3 style="color: #cfe6ff; margin-bottom: 12px; font-size: 1.1rem;">
                    Upload your resume
                </h3>
                <p style="color: #9fb0c8; margin-bottom: 12px; font-size: 0.95rem;">
                    Supported formats: <strong>PDF, DOCX, TXT</strong>. Files must contain resume content.
                </p>
                <p style="color: #9fb0c8; margin-top: 4px; font-size: 0.85rem;">Tip: upload a complete resume (recommended &gt;2 KB).</p>
                <form id="uploadForm" enctype="multipart/form-data">
                    <input type="file" id="resumeFile" name="file" accept=".txt,.pdf,.docx" required>
                    <br>
                    <button type="submit" class="analyze-btn">
                        Analyze
                    </button>
                </form>
                <div id="fileWarning" style="display:none; margin-top:10px; color: #ff6b6b; font-size:0.95rem;"></div>
            </div>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="color: #cfe6ff; font-size: 1.05rem;" class="pulse-text">
                Processing — a few seconds.
            </p>
        </div>
        
        <div class="results" id="results"></div>
    </div>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily and pass extracted text to analyzer
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            file.save(tmp_file.name)

            try:
                analyzer = ResumeAnalyzer()

                # Let the analyzer extract text from the saved file (analyzer supports path or file-like)
                resume_text = None
                try:
                    resume_text = analyzer.extract_text_from_file(tmp_file.name)
                except Exception:
                    # Fallback: read raw bytes and decode
                    try:
                        with open(tmp_file.name, 'rb') as f:
                            resume_text = f.read().decode('utf-8', errors='ignore')
                    except Exception:
                        resume_text = ''

                # Perform analysis on extracted text
                analysis = analyzer.analyze_resume(resume_text)

                # Clean up temp file
                try:
                    os.unlink(tmp_file.name)
                except Exception:
                    pass

                # If analyzer indicates invalid content, return 400 with message
                if isinstance(analysis, dict) and analysis.get('valid') is False:
                    return jsonify({'error': analysis.get('message', 'Invalid resume content')}), 400

                return jsonify(analysis)

            except Exception as analysis_error:
                # Clean up temp file even if analysis fails
                try:
                    os.unlink(tmp_file.name)
                except Exception:
                    pass

                # Return an explicit error
                return jsonify({'error': 'Analysis failed due to internal error.'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'AI Resume Nexus',
        'version': '2.0'
    })

# For Vercel serverless deployment
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

if __name__ == '__main__':
    app.run(debug=True)