docker build -t ai-resume-analyzer:local .
docker run -d --name ai-resume-container -p 5000:8000 ai-resume-analyzer:local
docker build -t ai-resume-analyzer:local .
docker run -d --name ai-resume-container -p 5000:8000 ai-resume-analyzer:local
git clone https://github.com/Crewjah/AI-Resume-Analyzer.git
docker build -t ai-resume-analyzer:local .
docker run --rm -p 5000:5000 ai-resume-analyzer:local
docker-compose up --build
ai-resume-analyzer/
AI Resume Analyzer — clean split frontend and backend
====================================================

Static frontend (Vercel-ready) + Flask backend API. Upload a resume (PDF/DOCX/TXT), optional job description, get ATS score, skills, keywords, and recommendations.

Project layout
- `frontend/` – static site (HTML/JS/CSS). Deploy to Vercel or any static host.
- `backend/` – Flask API (`/analyze`, `/health`). Deploy to Render/Railway/Fly/Heroku.
- `src/` – core analyzer logic (shared).
- `tests/` – pytest suite; auto-starts backend on port 5000 during tests.
- `archive/legacy/` – archived old files; safe to ignore.

Quick start (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python backend/app.py  # runs on http://localhost:5000

# Serve frontend (simple static)
python -m http.server 8000 -d frontend
# Open http://localhost:8000 and ensure API_BASE points to backend (see frontend/assets/js/config.js)
```

Testing
```bash
pytest -q
```
Tests spin up the backend automatically on 127.0.0.1:5000.

Deployment (short)
- Backend (Render example): Build `pip install -r requirements.txt`; start `gunicorn backend.app:app --bind 0.0.0.0:$PORT`.
- Frontend (Vercel): Set `window.API_BASE` in `frontend/assets/js/config.js` to your backend URL; deploy static folder `frontend/`.
See `docs/DEPLOYMENT.md` for detailed steps.

Notes
- PDF parsing prefers `pypdf` with `PyPDF2` fallback.
- CORS is enabled in the backend for cross-origin frontend calls.
- Analyzer lives in `src/analyzer.py`; API is a thin wrapper in `backend/app.py`.
flake8 .
```

## 📈 Roadmap

### Upcoming Features
- [ ] **Multi-language Support** - Resume analysis in multiple languages
- [ ] **PDF Report Generation** - Downloadable analysis reports
- [ ] **Resume Builder** - AI-powered resume creation tool
- [ ] **Batch Processing** - Analyze multiple resumes at once
- [ ] **API Integration** - REST API for external applications
- [ ] **Advanced ML Models** - Integration with transformer models
- [ ] **Resume Templates** - Industry-specific resume templates
- [ ] **Performance Tracking** - Historical analysis and improvement tracking

### Technical Improvements
- [ ] **Caching System** - Redis integration for faster analysis
- [ ] **Database Support** - PostgreSQL for data persistence
- [ ] **User Authentication** - User accounts and saved analyses
- [ ] **Docker Deployment** - Containerized deployment options
- [ ] **Cloud Integration** - AWS/Azure deployment guides

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🌟 Acknowledgments

- **Streamlit Team** - For the amazing web framework
- **spaCy Team** - For powerful NLP capabilities
- **Plotly Team** - For beautiful interactive charts
- **Open Source Community** - For inspiration and contributions

---

<div align="center">

**Made with ❤️ by the AI Resume Analyzer Team**

[![GitHub stars](https://img.shields.io/github/stars/Crewjah/ai-resume-analyzer?style=social)](https://github.com/Crewjah/AI-Resume-Analyzer).

</div>
