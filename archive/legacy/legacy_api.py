from flask import Flask, request, jsonify, render_template_string
import os
import sys
sys.path.append(os.path.dirname(__file__))

from src.analyzer import ResumeAnalyzer
from src.config import APP_CONFIG as Config
import tempfile

app = Flask(__name__)

# HTML template with the same cyberpunk styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 AI Resume Nexus - Ultra Analysis</title>
    <style>
        /* trimmed for brevity in legacy copy */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🚀 AI Resume Nexus</h1>
            <p style="color: #00f5ff; font-size: 1.2rem;">Ultra-Modern Neural Analysis Engine</p>
        </div>
        <div class="upload-section">
            <div class="upload-area">
                <h3 style="color: #bf00ff; margin-bottom: 20px;">📄 Upload Your Resume</h3>
                <form id="uploadForm" enctype="multipart/form-data">
                    <input type="file" id="resumeFile" name="file" accept=".txt,.pdf,.docx" required>
                    <br>
                    <button type="submit" class="analyze-btn">🔬 Analyze Resume</button>
                </form>
            </div>
        </div>
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="color: #00f5ff;">Neural networks processing your resume...</p>
        </div>
        <div class="results" id="results"></div>
    </div>
    <script>
        // minimal legacy JS
    </script>
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
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            file.save(tmp_file.name)
            
            # Analyze resume
            analyzer = ResumeAnalyzer()
            analysis = analyzer.analyze_resume(tmp_file.name)
            
            # Clean up temp file
            os.unlink(tmp_file.name)
            
            return jsonify(analysis)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True)
