from flask import Flask, request, jsonify, render_template_string
import os
import sys
sys.path.append(os.path.dirname(__file__))

from analyzer import ResumeAnalyzer
from config import Config
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
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #0a0a0f 0%, #1a0520 50%, #0f0a1a 100%);
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            position: relative;
        }
        
        .title {
            font-size: 3rem;
            background: linear-gradient(45deg, #00f5ff, #bf00ff, #ff0080);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-shadow: 0 0 30px rgba(0, 245, 255, 0.3);
        }
        
        .upload-section {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            border: 1px solid rgba(0, 245, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 245, 255, 0.1);
        }
        
        .upload-area {
            border: 2px dashed #00f5ff;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            transition: all 0.3s ease;
            background: rgba(0, 245, 255, 0.05);
        }
        
        .upload-area:hover {
            border-color: #bf00ff;
            background: rgba(191, 0, 255, 0.05);
            transform: translateY(-2px);
        }
        
        input[type="file"] {
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid #00f5ff;
            border-radius: 10px;
            color: #ffffff;
            font-size: 16px;
        }
        
        .analyze-btn {
            background: linear-gradient(45deg, #00f5ff, #bf00ff);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 25px;
            font-size: 18px;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 20px rgba(0, 245, 255, 0.3);
        }
        
        .analyze-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(191, 0, 255, 0.4);
        }
        
        .results {
            display: none;
            margin-top: 40px;
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            border: 1px solid rgba(57, 255, 20, 0.3);
            box-shadow: 0 8px 32px rgba(57, 255, 20, 0.1);
        }
        
        .score {
            font-size: 2.5rem;
            font-weight: bold;
            color: #39ff14;
            text-shadow: 0 0 20px rgba(57, 255, 20, 0.5);
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(0, 245, 255, 0.1);
            border-top: 4px solid #00f5ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
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
        document.getElementById('uploadForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const fileInput = document.getElementById('resumeFile');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            if (!fileInput.files[0]) {
                alert('Please select a file');
                return;
            }
            
            loading.style.display = 'block';
            results.style.display = 'none';
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                loading.style.display = 'none';
                results.style.display = 'block';
                
                results.innerHTML = `
                    <div class="metric-card">
                        <h3 style="color: #00f5ff; margin-bottom: 15px;">🎯 ATS Compatibility Score</h3>
                        <div class="score">${data.ats_score}%</div>
                    </div>
                    
                    <div class="metric-card">
                        <h3 style="color: #bf00ff; margin-bottom: 15px;">💼 Skills Detected</h3>
                        <p style="color: #39ff14; font-size: 1.1rem;">${data.skills.join(', ') || 'No specific skills detected'}</p>
                    </div>
                    
                    <div class="metric-card">
                        <h3 style="color: #ff0080; margin-bottom: 15px;">📊 Analysis Summary</h3>
                        <p style="line-height: 1.6;">${data.summary}</p>
                    </div>
                    
                    <div class="metric-card">
                        <h3 style="color: #39ff14; margin-bottom: 15px;">🚀 Recommendations</h3>
                        <ul style="list-style: none; padding: 0;">
                            ${data.recommendations.map(rec => `<li style="margin: 10px 0; padding-left: 20px;">▶ ${rec}</li>`).join('')}
                        </ul>
                    </div>
                `;
                
            } catch (error) {
                loading.style.display = 'none';
                alert('Analysis failed. Please try again.');
                console.error('Error:', error);
            }
        });
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