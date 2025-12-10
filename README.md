# 🎯 AI Resume Analyzer

An intelligent, modern resume analysis tool powered by AI. Get instant **ATS scores**, **skills extraction**, **keyword analysis**, and **personalized recommendations**.

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Crewjah/AI-Resume-Analyzer)

**Live Demo:** [AI Resume Analyzer](https://ai-resume-analyzer.vercel.app)

---

## ✨ Features

### Core Capabilities
- 🎯 **ATS Score** - Instant ATS (Applicant Tracking System) compatibility score (0-100%)
- 🔍 **Skills Detection** - Automatically extract and categorize technical and professional skills
- 📊 **Job Matching** - Compare resume against job descriptions for matched/missing keywords
- 💡 **Smart Recommendations** - Personalized suggestions to improve your resume
- 📈 **Detailed Metrics** - Word count, experience years, keyword analysis at a glance
- 🌐 **Multi-Format Support** - PDF, DOCX, and plain text files
- 🔒 **Privacy First** - No data is stored; analysis happens server-side only

---

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Semantic markup with modern structure
- **CSS3** - Modern design system with responsive layout
- **Vanilla JavaScript** - No frameworks; pure, efficient code
- **Vercel Static Hosting** - CDN-backed with instant deployment

### Backend
- **Python 3.8+** - Robust, efficient backend
- **Flask** - Lightweight web framework
- **PyPDF2 / pypdf** - PDF text extraction
- **python-docx** - DOCX file processing
- **Vercel Serverless Functions** - Scalable, serverless API

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- Vercel account (free tier available)

### Local Development

#### 1. Clone Repository
```bash
git clone https://github.com/Crewjah/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

#### 2. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask server
python backend/app.py
```
Backend starts at: `http://127.0.0.1:5000`

#### 3. Frontend Setup
```bash
# Start static server
cd frontend
python -m http.server 8000
```
Visit: `http://localhost:8000?api=http://127.0.0.1:5000/analyze`

The `?api=` parameter points to your local backend.

---

## 📦 Deployment

### Deploy to Vercel (Recommended)

**One-click deploy:**
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Crewjah/AI-Resume-Analyzer)

**Manual deployment:**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**Configure in Vercel:**
- **Framework Preset:** Other
- **Root Directory:** `.`
- **Output Directory:** `frontend`
- **Install Command:** `pip install -r requirements.txt`

Frontend and API deploy to the same domain. No additional configuration needed!

### Deploy Backend to Heroku (Alternative)

```bash
# Create app
heroku create your-app-name

# Add Python buildpack
heroku buildpacks:add heroku/python

# Deploy
git push heroku main
```

Then update frontend API URL:
```
?api=https://your-app-name.herokuapp.com/analyze
```

### Docker Deployment

```bash
docker-compose up --build
```

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5000`

---

## 📡 API Reference

### POST `/api/analyze`

Analyze a resume and return detailed insights.

**Request:**
```bash
curl -X POST http://localhost:5000/analyze \
  -F "file=@resume.pdf" \
  -F "job_description=Software Engineer at Tech Company..."
```

**Parameters:**
- `file` (required) - Resume file (PDF, DOCX, or TXT)
- `job_description` (optional) - Job description for matching

**Response:**
```json
{
  "ats_score": 78,
  "skill_count": 12,
  "skills": {
    "Programming": ["Python", "JavaScript"],
    "Web Technologies": ["React", "Node.js"],
    "Databases": ["PostgreSQL", "MongoDB"],
    "Cloud & DevOps": ["AWS", "Docker"]
  },
  "keywords": ["leadership", "agile", "problem-solving"],
  "experience_years": 5,
  "word_count": 450,
  "job_analysis": {
    "match_score": 85,
    "matched_keywords": ["python", "react", "docker"],
    "missing_keywords": ["kubernetes"],
    "total_job_keywords": 25
  },
  "recommendations": [
    "Add quantifiable achievements to strengthen impact",
    "Include specific metrics in project descriptions"
  ]
}
```

### GET `/api/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Resume Analyzer",
  "version": "2.0"
}
```

---

## 📁 Project Structure

```
AI-Resume-Analyzer/
├── frontend/                      # Static frontend (HTML, CSS, JS)
│   ├── index.html                # Main application
│   └── assets/
│       ├── css/styles.css         # Modern design system
│       └── js/
│           ├── config.js          # API configuration
│           └── app.js             # Application logic
│
├── api/
│   └── analyze.py                 # Vercel serverless handler
│
├── backend/
│   ├── app.py                     # Flask application
│   └── requirements.txt           # Python dependencies
│
├── src/
│   ├── analyzer.py                # Core analysis engine
│   └── config.py                  # Configuration
│
├── vercel.json                    # Vercel deployment config
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker image definition
├── docker-compose.yml             # Docker compose setup
└── README.md                      # This file
```

---

## ⚙️ Configuration

### API Endpoint

The frontend automatically detects the API endpoint with this priority:

1. **Query parameter:** `?api=https://your-backend`
2. **localStorage:** `localStorage.API_OVERRIDE`
3. **Local dev:** `http://127.0.0.1:5000/analyze`
4. **Production:** `/api/analyze` (same domain)

**Examples:**

Override with query parameter:
```
https://your-domain.com/?api=https://custom-api.com/analyze
```

Set in browser console:
```javascript
localStorage.setItem('API_OVERRIDE', 'https://your-api.com/analyze');
location.reload();
```

---

## 📖 Usage Guide

### Basic Resume Analysis

1. Upload your resume (PDF, DOCX, or TXT)
2. Click "Analyze Resume"
3. Review your ATS score and detected skills

### Job Matching

1. Upload your resume
2. Paste the job description
3. Click "Analyze Resume"
4. View matched and missing keywords

### Interpreting Results

**ATS Score (0-100%)**
| Score | Status | Meaning |
|-------|--------|---------|
| 80-100 | ✅ Excellent | Should pass most ATS systems |
| 60-79 | ✓ Good | Minor tweaks needed |
| 40-59 | ⚠ Fair | Significant improvements needed |
| Below 40 | ❌ Poor | Major restructuring required |

**Skills Detection**
- Shows detected technical and professional skills
- Organized by category (Programming, Web Tech, Databases, etc.)
- Used for ATS scoring and job matching

**Job Match Score**
- Percentage of job keywords found in your resume
- **Matched keywords** (✓) - Emphasize these prominently
- **Missing keywords** (⚠) - Consider adding if relevant

---

## 🐛 Troubleshooting

### "Failed to connect to server"
**Cause:** API endpoint is unreachable

**Solutions:**
```bash
# Check if backend is running
curl http://api-endpoint/health

# Check API URL in browser
console.log(window.API_ENDPOINT)

# Use query parameter to override
?api=https://your-api-url
```

### "Invalid file type"
**Cause:** File is not PDF, DOCX, or TXT

**Solution:** Convert to one of the supported formats

### "File size exceeds limit"
**Cause:** File is larger than 10 MB

**Solution:** Compress or reduce resume content

### "Resume not being analyzed"
**Cause:** Resume content too short or missing text

**Solution:** Ensure resume has at least 50 words

---

## 🔒 Security & Privacy

✅ **No Data Storage** - Resumes deleted immediately after analysis
✅ **HTTPS Only** - All communication encrypted
✅ **No Tracking** - No analytics or user tracking
✅ **Open Source** - Fully auditable code
✅ **CORS Enabled** - Safe cross-origin requests

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📚 Development

### Adding New Skills

Edit `src/analyzer.py`:

```python
self.skills_database = [
    # Add new skills here
    "Your Skill",
]
```

### Customizing ATS Scoring

Modify `calculate_ats_score()` in `src/analyzer.py` to adjust:
- Skill weight (currently 40%)
- Content length expectations
- Professional keyword importance
- Structure indicator weight

### Changing Design

All styles use CSS variables in `frontend/assets/css/styles.css`:

```css
:root {
    --color-primary: #3b82f6;
    --font-size-lg: 1.125rem;
    /* ... customize variables ... */
}
```

---

## ❓ FAQ

**Q: Is my resume data safe?**
A: Yes. Resumes are analyzed server-side and never stored. No data is retained.

**Q: Can I use this commercially?**
A: Yes! Contact for enterprise licensing or self-host the application.

**Q: What file formats are supported?**
A: PDF, DOCX (Microsoft Word), and plain text (.txt).

**Q: Can I export results?**
A: Currently view on-screen. PDF export coming in future versions.

**Q: Does it support multiple languages?**
A: English only currently. Internationalization planned for v3.0.

---

## 🗺️ Roadmap

- 📱 Mobile app (iOS/Android)
- 🌍 Multi-language support (French, Spanish, German, Chinese)
- 📥 Results export (PDF, CSV, JSON)
- 📈 Resume comparison and version history
- 🤖 AI-powered resume suggestions
- 💼 Industry-specific recommendations
- 🔐 User accounts and resume history

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 📞 Support

- 📧 **Email:** support@crewjah.tech
- 🐛 **Issues:** [GitHub Issues](https://github.com/Crewjah/AI-Resume-Analyzer/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/Crewjah/AI-Resume-Analyzer/discussions)
- 📚 **Docs:** This README

---

## 🙏 Credits

Built with ❤️ by [Crewjah](https://github.com/Crewjah)

Special thanks to:
- The Python open-source community
- Vercel for excellent hosting
- All contributors and users

---

<div align="center">

**Made with ❤️ for job seekers everywhere**

⭐ If you find this useful, please star the repository!

</div>

**Last Updated:** December 2024
**Version:** 2.0.0
**Status:** Production Ready ✅
