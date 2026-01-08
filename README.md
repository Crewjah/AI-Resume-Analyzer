# AI Resume Analyzer

> Professional resume analysis tool powered by advanced natural language processing

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

AI Resume Analyzer is a web-based application that provides honest, actionable feedback on your resume. Built with modern web technologies and transparent scoring algorithms, it helps job seekers understand their resume strengths and areas for improvement.

**No fake data. No inflated scores. Just genuine, helpful analysis.**

## Features

### Comprehensive Analysis

- **Content Quality (0-100)**: Evaluates word count, action verbs, and quantified achievements
- **Keyword Optimization (0-100)**: Identifies technical and soft skills in your resume
- **ATS Compatibility (0-100)**: Checks formatting for Applicant Tracking Systems
- **Structure Score (0-100)**: Reviews organization and essential sections
- **Completeness (0-100)**: Verifies required information is present

### Key Capabilities

- Upload resume files (PDF or TXT format, up to 5MB)
- Detect technical skills (programming languages, frameworks, tools)
- Identify soft skills (leadership, communication, teamwork)
- Extract action verbs and achievements
- Generate tailored recommendations for improvement
- Download analysis reports
- Optional job description matching

### User Interface

- Clean, professional design with responsive layout
- Multi-page navigation (Upload, Results, About)
- Real-time file validation
- Progress indicators during analysis
- Color-coded scores and visual feedback
- Mobile-friendly responsive design

## Technical Stack

### Frontend
- **HTML5**: Semantic, accessible markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **JavaScript (ES6+)**: Interactive functionality without frameworks

### Backend
- **FastAPI**: High-performance Python web framework
- **PyPDF2**: PDF text extraction
- **Python 3.8+**: Core analysis logic

### Deployment
- **Vercel**: Serverless deployment platform
- Optimized for edge functions and static assets

## Project Structure

```
AI-Resume-Analyzer/
├── api/
│   ├── index.py              # Main FastAPI application
│   └── analyze.py            # Analysis endpoint (legacy)
├── backend/
│   ├── resume_analyzer.py    # Core analysis engine
│   ├── keyword_matcher.py    # Keyword matching utilities
│   └── pdf_extractor.py      # PDF extraction utilities
├── assets/
│   ├── css/
│   │   └── main.css          # Application styles
│   └── js/
│       └── main.js           # Client-side logic
├── index.html                # Main application page
├── vercel.json               # Vercel configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Crewjah/AI-Resume-Analyzer.git
   cd AI-Resume-Analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally with Vercel CLI** (recommended)
   ```bash
   npm install -g vercel
   vercel dev
   ```

4. **Or run with uvicorn** (alternative)
   ```bash
   uvicorn api.index:app --reload
   ```

5. **Open in browser**
   ```
   http://localhost:3000 (Vercel)
   http://localhost:8000 (uvicorn)
   ```

## Deployment

### Deploy to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Production deployment**
   ```bash
   vercel --prod
   ```

### Environment Variables

No environment variables are required for basic operation.

## How It Works

### Analysis Process

1. **File Upload**: User uploads resume (PDF or TXT)
2. **Text Extraction**: System extracts text from the file
3. **Content Analysis**: Algorithm analyzes multiple dimensions:
   - Word count and content quality
   - Action verbs and quantified achievements
   - Technical and soft skills detection
   - Section structure and completeness
   - ATS compatibility factors
4. **Score Calculation**: Transparent algorithms calculate scores:
   - Overall = 25% Content + 20% Keywords + 25% ATS + 15% Structure + 15% Completeness
5. **Recommendations**: System generates specific, actionable improvements
6. **Results Display**: User sees detailed scores and insights

### Scoring Methodology

All scores are calculated using transparent, rule-based algorithms:

#### Content Quality (0-100)
- Optimal word count: 300-700 words
- Action verbs bonus: +2 points each (max 30)
- Quantified achievements: +5 points each (max 30)
- Base score: 40 points for appropriate length

#### Keyword Optimization (0-100)
- Based on number of relevant skills detected
- 15+ skills: 100 points
- 10-14 skills: 85 points
- 7-9 skills: 70 points
- 5-6 skills: 55 points
- 3-4 skills: 40 points

#### ATS Compatibility (0-100)
- Starts at 100, deductions for:
  - Missing essential sections: -25 points each
  - Missing contact info: -15 points (email), -10 points (phone)
  - Missing dates: -10 points

#### Structure Score (0-100)
- 5+ sections: 100 points
- 4 sections: 85 points
- 3 sections: 70 points
- Fewer sections: proportional scoring

#### Completeness (0-100)
- Starts at 100, deductions for:
  - Missing email: -15 points
  - Missing phone: -15 points
  - Missing experience/education/skills: -12 points each

## API Endpoints

### POST /api/analyze

Analyze a resume file.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body:
  - `file`: Resume file (PDF or TXT)
  - `job_description`: Optional job description text

**Response:**
```json
{
  "ok": true,
  "data": {
    "scores": {
      "overall_score": 75,
      "content_quality": 80,
      "keyword_optimization": 70,
      "ats_compatibility": 85,
      "structure_score": 75,
      "completeness": 65
    },
    "technical_skills": ["Python", "JavaScript", "React"],
    "soft_skills": ["Leadership", "Communication"],
    "action_verbs": ["developed", "led", "implemented"],
    "action_verbs_count": 12,
    "word_count": 450,
    "recommendations": ["Add more quantified achievements", "Include contact information"]
  }
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### GET /status

Check if analyzer is ready.

**Response:**
```json
{
  "ready": true,
  "message": "API is operational",
  "version": "2.0"
}
```

## Usage Tips

### For Best Results

1. **Use a complete resume**: Include all standard sections
2. **Format properly**: Use clear section headings
3. **Include contact info**: Email and phone number
4. **Quantify achievements**: Use numbers and percentages
5. **List relevant skills**: Both technical and soft skills
6. **Use action verbs**: Start bullet points with strong verbs

### What to Avoid

- Excessive formatting or special characters
- Missing essential sections (Experience, Education, Skills)
- Vague descriptions without specific achievements
- Typos and grammatical errors
- Inconsistent date formats

## Privacy & Security

- **No data storage**: Resume data is processed in real-time and immediately discarded
- **No tracking**: We don't track or store personal information
- **Secure processing**: All data stays within the session
- **No third parties**: Your resume is never sent to external services

## Development

### Running Tests

```bash
pytest tests/
```

### Code Structure

- `backend/resume_analyzer.py`: Core analysis algorithms
- `assets/js/main.js`: Client-side interaction logic
- `assets/css/main.css`: Styling and responsive design
- `api/index.py`: API server and routes

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Version History

### Version 2.0.0 (Current)
- Complete redesign with professional UI
- Honest scoring algorithms without fake data
- Multi-page navigation
- Improved error handling
- Mobile-responsive design
- Download report functionality

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing issues for solutions

## Acknowledgments

Built with:
- FastAPI for the backend API
- Vercel for deployment
- PyPDF2 for PDF processing
- Modern web standards (HTML5, CSS3, ES6+)

---

**Note**: This tool provides guidance based on general resume best practices. Always tailor your resume to specific job requirements and industries.

Made with care for job seekers everywhere.
