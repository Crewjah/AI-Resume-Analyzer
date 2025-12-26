# Deployment Guide

This guide provides instructions for deploying the AI Resume Analyzer on various platforms.

## Table of Contents

- [Streamlit Cloud](#streamlit-cloud)
- [Vercel](#vercel)
- [Heroku](#heroku)
- [Docker](#docker)
- [Local Production](#local-production)

## Streamlit Cloud

Streamlit Cloud is the easiest way to deploy Streamlit applications.

### Prerequisites

- GitHub account
- GitHub repository with your code

### Steps

1. **Prepare Your Repository**
   - Ensure `requirements.txt` is up to date
   - Make sure `app.py` is in the root directory
   - Push all changes to GitHub

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `Crewjah/AI-Resume-Analyzer`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Configure Advanced Settings** (Optional)
   - Python version: 3.9 or higher
   - Add secrets if needed in Advanced settings

4. **Access Your App**
   - Your app will be available at: `https://your-app-name.streamlit.app`

### Updating Your App

Changes pushed to your GitHub repository will automatically redeploy the app.

## Vercel (FastAPI Function)

This project deploys only the FastAPI serverless function on Vercel. The Streamlit UI is not hosted on Vercel; use Streamlit Cloud (see above) or another host for the UI.

### What’s deployed
- API Function: `api/analyze.py` (FastAPI, handles file upload + analysis)
- Deps: `fastapi`, `uvicorn`, `python-multipart`, `PyPDF2` (plus any analyzer deps in `backend/`)

### Configuration
- `vercel.json` defines a functions-only setup and Python 3.11 runtime.
- The function is served at `/api/analyze` externally.
- Inside the ASGI app, routes are relative to the function root:
   - `POST /` → analyze upload
   - `GET /health` → health check

### One-time setup
1. Ensure these files exist:
    - `api/analyze.py`
    - `requirements.txt` (includes API and analyzer dependencies)
    - `backend/` modules (included via `includeFiles`)
2. Push to GitHub and connect the repo to Vercel.

### Deploy steps
- Push to `main`. Vercel will:
   - Package `api/analyze.py` as a Python function
   - Install `requirements.txt` into the function
   - Bundle `backend/**` into the function

### Verify deployment
Replace `<your-deployment>` with your Vercel URL.
```bash
# Health
curl -s https://<your-deployment>/api/analyze/health

# Analyze (PDF upload)
curl -s -X POST https://<your-deployment>/api/analyze \
   -F "file=@/path/to/resume.pdf" | jq
```

### Local development (API)
```bash
pip install -r requirements.txt
uvicorn api.analyze:app --reload --port 8000
# Then test: curl -s http://localhost:8000/health
```

### Streamlit note
Streamlit is for local experimentation and separate hosting. To run locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Heroku

### Prerequisites

- Heroku account
- Heroku CLI installed

### Setup Files

1. **Create `Procfile`**
   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. **Create `setup.sh`**
   ```bash
   mkdir -p ~/.streamlit/

   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Create `runtime.txt`**
   ```
   python-3.9.16
   ```

### Deployment Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Add Python Buildpack**
   ```bash
   heroku buildpacks:set heroku/python
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

### Troubleshooting Heroku

- Check logs: `heroku logs --tail`
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

## Docker

### Create Dockerfile

Create a file named `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Create `.dockerignore`

```
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
.git/
.gitignore
README.md
.vscode/
.idea/
```

### Build and Run

1. **Build Docker Image**
   ```bash
   docker build -t ai-resume-analyzer .
   ```

2. **Run Container**
   ```bash
   docker run -p 8501:8501 ai-resume-analyzer
   ```

3. **Access Application**
   - Open browser to `http://localhost:8501`

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - .:/app
    environment:
      - PYTHONUNBUFFERED=1
```

Run with:
```bash
docker-compose up
```

## Local Production

### Using Gunicorn (Not Recommended for Streamlit)

Streamlit has its own server. For production locally:

1. **Install Production Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run with Production Config**
   ```bash
   streamlit run app.py --server.headless true --server.port 8501
   ```

3. **Use Process Manager** (PM2 or Supervisor)

   With PM2:
   ```bash
   npm install -g pm2
   pm2 start "streamlit run app.py" --name ai-resume-analyzer
   pm2 save
   pm2 startup
   ```

## Environment Variables

### Setting Up Secrets

For sensitive data, use Streamlit secrets:

1. **Local Development**
   Create `.streamlit/secrets.toml`:
   ```toml
   [secrets]
   api_key = "your-api-key"
   ```

2. **Streamlit Cloud**
   - Go to app settings
   - Add secrets in the Secrets section

3. **Access in Code**
   ```python
   import streamlit as st
   api_key = st.secrets["api_key"]
   ```

## Performance Optimization

### For Production Deployment

1. **Enable Caching**
   ```python
   @st.cache_data
   def expensive_computation():
       # Your code here
       pass
   ```

2. **Optimize File Size**
   - Use `.dockerignore` and `.gitignore`
   - Remove unnecessary files
   - Minimize dependencies

3. **Configure Server Settings**
   ```toml
   [server]
   maxUploadSize = 10
   maxMessageSize = 10
   enableCORS = false
   enableXsrfProtection = true
   ```

## Monitoring

### Check Application Health

1. **Logs**
   - Streamlit Cloud: View in dashboard
   - Heroku: `heroku logs --tail`
   - Docker: `docker logs container_id`

2. **Health Endpoints**
   ```
   /_stcore/health
   ```

## SSL/HTTPS

Most platforms (Streamlit Cloud, Heroku, Vercel) provide SSL automatically.

For custom domains:
- Configure SSL certificate
- Update DNS settings
- Enable HTTPS redirect

## Troubleshooting

### Common Issues

1. **Module Not Found**
   - Ensure all dependencies in `requirements.txt`
   - Check Python version compatibility

2. **Port Issues**
   - Use environment variable `$PORT` for cloud platforms
   - Check port configuration in cloud settings

3. **Memory Errors**
   - Optimize code for memory usage
   - Use caching effectively
   - Consider upgrading plan

4. **SpaCy Model Download**
   - Ensure model downloads in build process
   - Check build logs for errors

## Best Practices

- Use version control (Git)
- Test before deploying
- Monitor application performance
- Keep dependencies updated
- Use environment variables for sensitive data
- Enable error tracking
- Set up automated backups
- Document deployment process

## Support

For deployment issues:
- Check platform documentation
- Review application logs
- Open issue on GitHub
- Contact platform support

## Recommended Platform

**For AI Resume Analyzer, we recommend Streamlit Cloud** because:
- Built specifically for Streamlit apps
- Easy deployment process
- Automatic SSL/HTTPS
- Free tier available
- Seamless GitHub integration
- No configuration needed

---

Last updated: December 2026
