<div align="center">

# 📄 AI Resume Analyzer

### Professional Resume Analysis Tool with Transparent Scoring

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Contributing](#contributing) • [License](#license)

</div>

---

## Overview

**AI Resume Analyzer** is an intelligent, open-source tool that provides honest and actionable feedback on resumes. Built with transparency in mind, it uses advanced NLP and rule-based algorithms to analyze resumes across multiple dimensions, helping job seekers optimize their applications for both human recruiters and Applicant Tracking Systems (ATS).

### Why AI Resume Analyzer?

- **Transparent Scoring** - No black-box algorithms, clear methodology for all scores
- **Multi-Dimensional Analysis** - Content, keywords, ATS compatibility, structure, and completeness
- **Real-Time Feedback** - Instant analysis with detailed recommendations
- **No Inflated Scores** - Honest, realistic assessment to drive genuine improvements
- **100% Open Source** - Community-driven development with complete transparency

---

## Features

### Comprehensive Analysis Engine

| Feature | Description |
|---------|-------------|
| **Content Quality** | Evaluates word count, action verbs, and quantified achievements (0-100 score) |
| **Keyword Optimization** | Identifies technical and soft skills to maximize ATS compatibility (0-100 score) |
| **ATS Compatibility** | Checks formatting for Applicant Tracking Systems (0-100 score) |
| **Structure Score** | Reviews organization and essential sections (0-100 score) |
| **Completeness** | Verifies all required information is present (0-100 score) |

### User Interface

- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Dark/Light Mode** - Comfortable viewing in any environment
- **Interactive Visualizations** - Charts and graphs powered by Plotly
- **Download Reports** - Export analysis results in multiple formats
- **Real-Time Processing** - Instant feedback as you upload

### Advanced Capabilities

- Support for PDF and TXT resume formats (up to 5MB)
- Technical skills detection (Python, Java, React, AWS, etc.)
- Soft skills identification (Leadership, Communication, Teamwork)
- Action verbs and quantified achievements extraction
- Education and experience section analysis
- Optional job description matching for targeted optimization
- Personalized improvement recommendations

---

## Demo

> **Live Demo**: [Coming Soon]

### Sample Analysis

```
Overall Score: 78/100

├─ Content Quality:      82/100  ✓ Good
├─ Keyword Optimization: 75/100  ⚠ Needs Work  
├─ ATS Compatibility:    88/100  ✓ Excellent
├─ Structure:            90/100  ✓ Excellent
└─ Completeness:         65/100  ⚠ Needs Work

Top Recommendations:
1. Add 3-5 more technical skills relevant to your field
2. Include quantified achievements in your experience section
3. Add your LinkedIn profile URL to contact information
```

---

## Tech Stack

<div align="center">

### Languages & Frameworks

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

### Frameworks & Libraries

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

### Deployment & Tools

![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

| Category | Technologies |
|----------|-------------|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) |
| **Backend** | Python 3.8+, FastAPI, Streamlit |
| **NLP & Analysis** | NLTK, spaCy, Custom Algorithms |
| **PDF Processing** | PyPDF2, python-docx |
| **Visualization** | Plotly, Matplotlib |
| **Deployment** | Vercel, Docker-ready |

</div>

---

## Project Structure

```
AI-Resume-Analyzer/
├── api/                      # FastAPI backend
│   ├── index.py                 # Main API application
│   └── analyze.py               # Analysis endpoints
├── backend/                  # Core analysis engine
│   ├── resume_analyzer.py       # Main analyzer logic
│   ├── keyword_matcher.py       # Keyword detection
│   └── pdf_extractor.py         # PDF text extraction
├── assets/                   # Static resources
│   ├── css/
│   │   └── main.css            # Application styles
│   └── js/
│       └── main.js             # Client-side logic
├── docs/                     # Documentation
│   ├── API.md                  # API documentation
│   ├── CONTRIBUTING.md         # Contribution guidelines
│   └── DEPLOYMENT.md           # Deployment guide
├── tests/                    # Test suite
│   ├── test_app.py
│   ├── test_resume_analyzer.py
│   └── test_smoke.py
├── scripts/                  # Setup scripts
│   ├── setup.sh                # Unix/Linux/macOS
│   └── setup.ps1               # Windows PowerShell
├── app.py                       # Streamlit application
├── requirements.txt             # Python dependencies
├── vercel.json                 # Vercel configuration
├── LICENSE                     # MIT License
└── README.md                   # This file
```

---

## Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.8 or higher ([Download](https://www.python.org/downloads/))
- **pip** package manager (comes with Python)
- **Git** ([Download](https://git-scm.com/downloads))

### Quick Start

#### Step 1: Clone the Repository

```bash
git clone https://github.com/Crewjah/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

#### Step 2: Set Up Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Download NLP Models (Required for first run)

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
python -m spacy download en_core_web_sm
```

---

## Usage

### Running the Application

#### Option 1: Streamlit (Recommended)

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

#### Option 2: FastAPI with Vercel Dev

```bash
# Install Vercel CLI (first time only)
npm install -g vercel

# Run development server
vercel dev
```

Then open your browser to `http://localhost:3000`

#### Option 3: FastAPI with Uvicorn

```bash
uvicorn api.index:app --reload --port 8000
```

Then open your browser to `http://localhost:8000`

### Using the Analyzer

1. **Upload Resume** - Drag & drop or select your resume (PDF/TXT)
2. **Add Job Description** (Optional) - Paste the job description for targeted analysis
3. **Analyze** - Click the analyze button
4. **Review Results** - View your scores, detected skills, and recommendations
5. **Download Report** - Export your analysis for future reference

### API Usage

```python
import requests

# Analyze resume via API
with open('resume.pdf', 'rb') as file:
    response = requests.post(
        'http://localhost:8000/api/analyze',
        files={'file': file}
    )
    
analysis = response.json()
print(f"Overall Score: {analysis['overall_score']}/100")
```

For complete API documentation, see [docs/API.md](docs/API.md)

---

## Deployment

### Deploy to Vercel (Recommended)

1. **Fork this repository** to your GitHub account

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your forked repository
   - Deploy with default settings

3. **Or use Vercel CLI**
   ```bash
   npm install -g vercel
   vercel login
   vercel --prod
   ```

### Deploy with Docker

```bash
# Build image
docker build -t ai-resume-analyzer .

# Run container
docker run -p 8501:8501 ai-resume-analyzer
```

### Deploy to Other Platforms

- **Heroku**: See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md#heroku)
- **AWS**: See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md#aws)
- **Google Cloud**: See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md#gcp)

---

## How It Works

### Analysis Methodology

Our transparent scoring system evaluates resumes across 5 key dimensions:

#### 1. Content Quality (0-100)
- **Word Count**: Optimal range 300-700 words
- **Action Verbs**: Bonus +2 points each (max 30)
- **Quantified Achievements**: +5 points each (max 30)
- **Base Score**: 40 points for appropriate length

#### 2. Keyword Optimization (0-100)
| Skills Detected | Score |
|-----------------|-------|
| 15+ skills      | 100   |
| 10-14 skills    | 85    |
| 7-9 skills      | 70    |
| 5-6 skills      | 55    |
| 3-4 skills      | 40    |

#### 3. ATS Compatibility (0-100)
- Starts at 100, deductions for:
  - Missing essential sections: -25 points each
  - Missing email: -15 points
  - Missing phone: -10 points
  - Missing dates: -10 points

#### 4. Structure Score (0-100)
| Sections | Score |
|----------|-------|
| 5+       | 100   |
| 4        | 85    |
| 3        | 70    |
| <3       | Proportional |

#### 5. Completeness (0-100)
- Starts at 100, deductions for:
  - Missing contact info: -15 points each
  - Missing key sections: -12 points each

### Overall Score Calculation

```
Overall = (25% × Content) + (20% × Keywords) + (25% × ATS) + (15% × Structure) + (15% × Completeness)
```

---

## API Reference

### Endpoints

#### `POST /api/analyze`

Analyze a resume file and get comprehensive feedback.

**Request:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@resume.pdf" \
  -F "job_description=Looking for Python developer..."
```

**Parameters:**
- `file` (required): Resume file (PDF or TXT, max 5MB)
- `job_description` (optional): Target job description for matching

**Response:**
```json
{
  "ok": true,
  "data": {
    "scores": {
      "overall_score": 78,
      "content_quality": 82,
      "keyword_optimization": 75,
      "ats_compatibility": 88,
      "structure_score": 90,
      "completeness": 65
    },
    "technical_skills": ["Python", "JavaScript", "React", "AWS"],
    "soft_skills": ["Leadership", "Communication", "Problem-solving"],
    "action_verbs": ["developed", "led", "implemented", "optimized"],
    "action_verbs_count": 15,
    "word_count": 520,
    "recommendations": [
      "Add 3-5 more technical skills",
      "Include LinkedIn profile URL",
      "Quantify achievements with metrics"
    ]
  }
}
```

#### `GET /health`

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-02T10:30:00Z"
}
```

#### `GET /status`

Check API readiness and version.

**Response:**
```json
{
  "ready": true,
  "message": "API is operational",
  "version": "2.0.0"
}
```

📖 **Full API documentation**: [docs/API.md](docs/API.md)

---

## Contributing

We welcome contributions from the community! Whether it's bug fixes, new features, documentation improvements, or feedback, all contributions are appreciated.

### How to Contribute

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub, then:
   git clone https://github.com/YOUR_USERNAME/AI-Resume-Analyzer.git
   cd AI-Resume-Analyzer
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests if applicable

4. **Test your changes**
   ```bash
   pytest tests/
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Describe your changes clearly

### Contribution Guidelines

- **Code Quality**: Write clean, readable, well-documented code
- **Testing**: Add tests for new features
- **Documentation**: Update docs for any changes
- **Focus**: One feature/fix per pull request
- **Communication**: Discuss major changes in issues first

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/ -v

# Format code
black .

# Lint code
flake8 --max-line-length=100
```

### Areas for Contribution

- **Bug Fixes**: Check [Issues](https://github.com/Crewjah/AI-Resume-Analyzer/issues)
- **New Features**: AI improvements, new analysis metrics
- **Documentation**: Tutorials, examples, translations
- **UI/UX**: Design improvements, accessibility
- **Testing**: Increase test coverage
- **Internationalization**: Multi-language support

### Code of Conduct

Be respectful, inclusive, and constructive. We're building this together!

**Full contributing guide**: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_resume_analyzer.py -v
```

### Test Structure

```
tests/
├── test_app.py                 # Streamlit app tests
├── test_resume_analyzer.py     # Core analyzer tests
└── test_smoke.py              # Integration tests
```

---

## Best Practices & Tips

### For Users

**Do:**
- Include all standard resume sections
- Use clear section headings
- Add contact information (email, phone, LinkedIn)
- Quantify achievements with numbers/percentages
- List relevant technical and soft skills
- Start bullet points with action verbs

**Avoid:**
- Excessive formatting or graphics
- Missing essential sections
- Vague descriptions without achievements
- Typos and grammatical errors
- Inconsistent date formats

### For Developers

- Follow PEP 8 style guide for Python
- Write docstrings for all functions
- Add type hints where applicable
- Keep functions focused and small
- Write tests for new features

---

## Privacy & Security

We take your privacy seriously:

- **No Data Storage** - Resumes are processed in real-time and immediately discarded
- **No Tracking** - We don't track or store personal information
- **Secure Processing** - All data stays within your session
- **No Third Parties** - Your resume never leaves our servers
- **Open Source** - Fully transparent codebase for audit

---

## Roadmap

### Current Version: 2.0.0

### Planned Features

- **AI-Powered Recommendations** - GPT integration for personalized suggestions
- **Resume Templates** - Downloadable ATS-friendly templates
- **Cover Letter Analysis** - Extend analysis to cover letters
- **LinkedIn Profile Optimizer** - Analyze LinkedIn profiles
- **Multi-Language Support** - Internationalization (i18n)
- **Browser Extension** - Quick analysis from LinkedIn/Indeed
- **Mobile App** - iOS and Android applications
- **Premium Features** - Advanced analytics and insights

### Version History

#### v2.0.0 (Current) - February 2026
- Complete UI redesign with Streamlit
- Transparent scoring algorithms
- Dark/light mode support
- Interactive visualizations with Plotly
- Download report functionality
- Mobile-responsive design

#### v1.0.0 - Initial Release
- Basic resume analysis
- PDF/TXT support
- Keyword detection
- FastAPI backend

---

## FAQ

<details>
<summary><b>Is this really free?</b></summary>
Yes! AI Resume Analyzer is completely free and open source under the MIT License.
</details>

<details>
<summary><b>Do you store my resume?</b></summary>
No. Your resume is processed in real-time and immediately discarded. We don't store any personal data.
</details>

<details>
<summary><b>What file formats are supported?</b></summary>
Currently PDF and TXT files up to 5MB. DOCX support is coming soon.
</details>

<details>
<summary><b>How accurate is the analysis?</b></summary>
Our scoring is based on industry best practices and ATS requirements. While helpful, always tailor your resume to specific job requirements.
</details>

<details>
<summary><b>Can I use this for commercial purposes?</b></summary>
Yes! The MIT License allows commercial use. Just provide attribution.
</details>

<details>
<summary><b>How can I improve my score?</b></summary>
Follow the personalized recommendations provided after analysis. Generally: add relevant skills, quantify achievements, and ensure all essential sections are present.
</details>

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Crewjah

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

### What this means:
- Commercial use
- Modification
- Distribution
- Private use
- Attribution required
- No warranty provided

---

## Acknowledgments

Built with these amazing technologies:

- [Python](https://www.python.org/) - Core programming language
- [Streamlit](https://streamlit.io/) - Interactive web framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern API framework
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF processing
- [NLTK](https://www.nltk.org/) - Natural language processing
- [spaCy](https://spacy.io/) - Advanced NLP
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Vercel](https://vercel.com/) - Deployment platform

Special thanks to all [contributors](https://github.com/Crewjah/AI-Resume-Analyzer/graphs/contributors) who have helped improve this project!

---

## Support & Contact

### Get Help

- **Documentation**: Check our [docs](docs/) folder
- **Bug Reports**: [Open an issue](https://github.com/Crewjah/AI-Resume-Analyzer/issues/new?template=bug_report.md)
- **Feature Requests**: [Request a feature](https://github.com/Crewjah/AI-Resume-Analyzer/issues/new?template=feature_request.md)
- **Discussions**: [GitHub Discussions](https://github.com/Crewjah/AI-Resume-Analyzer/discussions)

### Community

- **Star this repo** if you find it helpful!
- **Share** with friends looking for resume help
- **Contribute** to make it even better

---

<div align="center">

## Project Stats

![GitHub stars](https://img.shields.io/github/stars/Crewjah/AI-Resume-Analyzer?style=for-the-badge)](https://github.com/Crewjah/AI-Resume-Analyzer/stargazers)
![GitHub forks](https://img.shields.io/github/forks/Crewjah/AI-Resume-Analyzer?style=for-the-badge)](https://github.com/Crewjah/AI-Resume-Analyzer/network/members)
![GitHub issues](https://img.shields.io/github/issues/Crewjah/AI-Resume-Analyzer?style=for-the-badge)](https://github.com/Crewjah/AI-Resume-Analyzer/issues)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Crewjah/AI-Resume-Analyzer?style=for-the-badge)](https://github.com/Crewjah/AI-Resume-Analyzer/pulls)
![GitHub last commit](https://img.shields.io/github/last-commit/Crewjah/AI-Resume-Analyzer?style=for-the-badge)](https://github.com/Crewjah/AI-Resume-Analyzer/commits/main)
![GitHub contributors](https://img.shields.io/github/contributors/Crewjah/AI-Resume-Analyzer?style=for-the-badge)](https://github.com/Crewjah/AI-Resume-Analyzer/graphs/contributors)

---

### If this project helped you, please give it a star!

**Made with ❤️ by [Crewjah](https://github.com/Crewjah)**

*Helping job seekers succeed, one resume at a time.*

[Report Bug](https://github.com/Crewjah/AI-Resume-Analyzer/issues) · [Request Feature](https://github.com/Crewjah/AI-Resume-Analyzer/issues) · [Contribute](docs/CONTRIBUTING.md)

</div>

