# AI Resume Analyzer

> **AI-powered resume analysis tool that helps you optimize your resume for Applicant Tracking Systems (ATS) and improve your job application success.**

**Current Version:** v2.0.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![GitHub stars](https://img.shields.io/github/stars/Crewjah/AI-Resume-Analyzer?style=social)](https://github.com/Crewjah/AI-Resume-Analyzer/stargazers)

## Overview

AI Resume Analyzer is a comprehensive Streamlit-based web application that provides instant, actionable feedback on your resume. Built with modern NLP techniques and an intuitive multi-page interface, it helps job seekers understand their resume strengths and areas for improvement.

## Features

### 📱 **Multi-Page Application**
1. **Upload & Analyze** - Upload multiple resume files (PDF, TXT) with instant validation
2. **Results Dashboard** - View comprehensive analysis with interactive charts
3. **Job Matching** - Compare your resume against job descriptions
4. **Settings** - Customize analysis weights and preferences

### 🎯 **5-Metric Scoring System**
- **Content Quality** (0-100): Evaluates word count, action verbs, and achievements
- **Keyword Optimization** (0-100): Analyzes keyword usage and relevance
- **ATS Compatibility** (0-100): Checks formatting for tracking systems
- **Structure Score** (0-100): Reviews organization and section completeness
- **Completeness** (0-100): Identifies missing resume sections

### 📊 **Interactive Visualizations**
- **Radar Chart**: Multi-dimensional score breakdown
- **Bar Chart**: Comparative metric analysis
- **Donut Chart**: Score distribution visualization
- **Gauge Chart**: Job match percentage display

### 🛠️ **Smart Analysis Features**
- **Technical Skills Detection**: Identifies programming languages, frameworks, and tools
- **Soft Skills Recognition**: Detects communication, leadership, and teamwork skills
- **Action Verb Analysis**: Counts strong action words vs passive language
- **Word Frequency Analysis**: Top keywords visualization
- **Missing Keywords**: Identifies skills gap compared to job descriptions

### 🎨 **Modern UI/UX**
- **Responsive Design**: Professional gradient theme with Inter font
- **Multi-File Upload**: Analyze multiple resumes with file management
- **Real-Time Analysis**: Progress indicators and instant feedback
- **Export Options**: Download results as CSV and JSON
- **Session State**: Maintains analysis results across pages

## Technical Stack

### Application Architecture
- **Frontend**: Streamlit 1.52.2 multi-page web application
- **Visualization**: Plotly 5.18.0 for interactive charts (radar, bar, donut, gauge)
- **Data Processing**: Pandas 2.3.3 for data manipulation
- **Document Processing**: PyPDF2 for PDF text extraction
- **Backend Analysis**: Custom NLP engine with regex and pattern matching

### Core Components
```
app.py (1022 lines)           # Main Streamlit application
├── Page Configuration        # Wide layout, expanded sidebar
├── Custom CSS Styling        # Professional gradient theme
├── Session State Management  # Multi-file analysis tracking
└── 4 Pages
    ├── Upload & Analyze     # File upload and validation
    ├── Results Dashboard    # Scores, charts, skills analysis
    ├── Job Matching         # Job description comparison
    └── Settings             # Customizable weights and preferences

backend/
├── resume_analyzer.py       # Core analysis engine
├── pdf_extractor.py         # PDF text extraction
└── keyword_matcher.py       # Keyword and skill matching
```

### Key Dependencies
```python
streamlit==1.52.2           # Web framework
plotly==5.18.0              # Interactive visualizations
pandas==2.3.3               # Data manipulation
PyPDF2==3.0.1               # PDF processing
scikit-learn>=1.1.0         # Machine learning
sentence-transformers>=2.2.2 # Semantic similarity
```

## Installation & Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Crewjah/AI-Resume-Analyzer.git
   cd AI-Resume-Analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the app**
   - Open your browser to `http://localhost:8501`
   - The browser should open automatically

### Alternative: Virtual Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

## How to Use

### Step-by-Step Guide

1. **Upload Your Resume**
   - Support for PDF and TXT formats
   - Maximum file size: 5MB per file
   - Drag-and-drop or click to browse

2. **Add Target Job (Optional)**
   - Paste the job description for personalized insights
   - Get keyword match scores
   - Identify skill gaps specific to the role

3. **Analyze & Review**
   - Click "Analyze My Resume" for instant results
   - Review your 5-metric scoring breakdown
   - Get specific, actionable recommendations

4. **Implement Changes**
   - Follow priority-ranked suggestions
   - Re-analyze to track improvements
   - Download results for reference

## Deployment

### Streamlit Community Cloud (Recommended)

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Select `app.py` as the main file
5. Deploy with one click

### Docker

```bash
docker build -t resume-analyzer .
docker run -p 8501:8501 resume-analyzer
```

### Heroku

```bash
# Create Procfile with:
# web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0

heroku create your-app-name
git push heroku main
```

## 💡 Pro Tips for Best Results

### Resume Optimization
- **Use action verbs**: "Led", "Developed", "Achieved" vs "Responsible for"
- **Quantify achievements**: "Increased sales by 25%" vs "Improved sales"
- **Include relevant keywords**: Match 70% of job posting terms
- **Standard formatting**: Use conventional section headers
- **ATS-friendly fonts**: Stick to Arial, Calibri, or Times New Roman

### Job Matching Strategy
- **Analyze multiple roles**: Compare requirements across similar positions
- **Track keyword frequency**: Focus on terms appearing in 3+ job posts
- **Customize per application**: Adjust keywords for each specific role
- **Balance specificity**: Include both broad skills and niche technologies

## 🔧 API Usage

### Python Integration
```python
from backend.resume_analyzer import ResumeAnalyzer

analyzer = ResumeAnalyzer()
results = analyzer.analyze_resume('path/to/resume.pdf')
print(results)
```

## 📊 Performance Metrics

- **Analysis Speed**: < 3 seconds for typical resume
- **File Support**: PDF, TXT formats
- **Max File Size**: 5MB per file
- **Multi-File**: Analyze multiple resumes
- **Browser Support**: All modern browsers

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute
- 🐛 **Report bugs** via [GitHub Issues](https://github.com/Crewjah/AI-Resume-Analyzer/issues)
- 💡 **Suggest features** for future releases
- 🔧 **Submit pull requests** with improvements
- 📚 **Improve documentation** and add examples
- 🧪 **Add test cases** for better coverage

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/Crewjah/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

# Create development branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Submit your changes
git push origin feature/your-feature-name
```

### Code Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation as needed

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=backend tests/
```

### Code Style

```bash
pip install black pylint
black .
pylint backend/
```

## Known Limitations

- Best results with text-based PDFs (not scanned images)
- English language resumes only
- Requires internet connection for initial model download

## Future Enhancements

- Support for DOCX file formats
- Multi-language support
- Resume template suggestions
- Industry-specific analysis
- Resume comparison feature
- Export detailed reports as PDF

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** for rapid web app development
- **Open Source Community** for inspiration and support
- **Social Winter of Code 2026** for the opportunity
- **All Contributors** who helped improve this project

## 📞 Support & Contact

### Get Help
- 📚 [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/Crewjah/AI-Resume-Analyzer/issues)
- 💬 [Discussions](https://github.com/Crewjah/AI-Resume-Analyzer/discussions)

### Stay Updated
- ⭐ Star this repository for updates
- 👁️ Watch releases for new features

---

### 🎯 **Ready to transform your resume?**

```bash
git clone https://github.com/Crewjah/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
pip install -r requirements.txt
streamlit run app.py
```

**Visit `http://localhost:8501` and start optimizing your resume today!**

---

<div align="center">

**Built with ❤️ using Python and Streamlit**

**Project Maintainer**: [Crewjah](https://github.com/Crewjah)

</div>
