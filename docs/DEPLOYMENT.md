# Deployment Guide

This repo now separates frontend (static) and backend (Flask API).

- Frontend: `frontend/` — static HTML/JS/CSS, ideal for Vercel or any static host.
- Backend: `backend/` — Flask API (`/analyze`, `/health`). Host on Render, Railway, Fly.io, or any Python-friendly host.

## Backend (Render example)

1. Create a new Web Service on Render.
2. Connect this repository and pick the `main` branch.
3. Environment:
   - Runtime: Python 3.12+
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn backend.app:app --bind 0.0.0.0:$PORT`
4. Set environment variables as needed (none required by default).
5. Deploy and note the public URL (e.g., `https://ai-resume-backend.onrender.com`).

## Frontend (Vercel static)

1. In `frontend/assets/js/config.js`, set `window.API_BASE` to your backend URL, e.g.:
   ```js
   window.API_BASE = 'https://ai-resume-backend.onrender.com';
   ```
2. Push changes, then import the project into Vercel.
3. Framework preset: “Other”. Build command: none (static). Output directory: `frontend`.
4. Deploy. Your site will be served from the Vercel URL and call the backend API.

## Local development

```bash
# Backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_ENV=development
python backend/app.py  # runs on http://localhost:5000

# Frontend
# Open frontend/index.html in a browser, or serve it:
python -m http.server 8000 -d frontend
```

## Tests

```bash
pytest -q
```

Tests auto-start the backend locally on port 5000 for integration checks.
