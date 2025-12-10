docker build -t ai-resume-analyzer:local .
docker run -d --name ai-resume-container -p 5000:8000 ai-resume-analyzer:local
docker build -t ai-resume-analyzer:local .
docker run -d --name ai-resume-container -p 5000:8000 ai-resume-analyzer:local
git clone https://github.com/Crewjah/AI-Resume-Analyzer.git
docker build -t ai-resume-analyzer:local .
docker run --rm -p 5000:5000 ai-resume-analyzer:local
docker-compose up --build
AI Resume Analyzer — clean split frontend and backend
====================================================

Static frontend + Flask backend API. Upload a resume (PDF/DOCX/TXT), optional job description, get ATS score, skills, keywords, and recommendations.

Project layout
- `frontend/` – static site (HTML/JS/CSS). Deploy to Vercel or any static host.
- `backend/` – Flask API (`/analyze`, `/health`). Deploy to Render/Railway/Fly/Heroku/Fly.io.
- `src/` – core analyzer logic (shared).
- `tests/` – pytest suite; auto-starts backend on port 5000 during tests.
- `archive/legacy/` – archived old files; safe to ignore.

Quick start (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Backend
python backend/app.py        # http://127.0.0.1:5000

# Frontend (simple static server)
python -m http.server 8000 -d frontend   # http://127.0.0.1:8000
# In browser, ensure API_BASE points to the backend (see frontend/assets/js/config.js)
```

Testing
```bash
pytest -q
```
Tests auto-start the backend on 127.0.0.1:5000.

Deployment (concise)
- Backend (Render example): build `pip install -r requirements.txt`; start `gunicorn backend.app:app --bind 0.0.0.0:$PORT`.
- Frontend (Vercel): deploy the `frontend/` folder. Configure `window.API_BASE` (or inject via env/script) to your live backend URL. Current default is `https://www.crewjah.tech` (no port) for production and `http://127.0.0.1:5000` locally. Update `frontend/assets/js/config.js` if your backend URL changes.
See `docs/DEPLOYMENT.md` for more detail.

Notes
- PDF parsing prefers `pypdf` with `PyPDF2` fallback.
- CORS is enabled in the backend for cross-origin frontend calls.
- Analyzer lives in `src/analyzer.py`; API is a thin wrapper in `backend/app.py`.
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
