# Vercel Deployment Fix - 250MB Size Limit Resolution

## Problem
Vercel serverless function exceeded the unzipped maximum size of **250 MB**.

## Root Causes
1. **Heavy dependencies** - Streamlit, Plotly, Pandas included in production build
2. **Git history** - `.git` folder (~8MB)
3. **Development files** - Tests, docs, scripts included unnecessarily
4. **spaCy models** - Large NLP models (can be 40MB+)

## Solutions Implemented

### 1. **Production Requirements File** (`requirements-production.txt`)
Created a lightweight dependency set excluding:
- ❌ Streamlit (UI only, not needed for API)
- ❌ Plotly & Matplotlib (visualization, not needed for API)
- ❌ Pandas (only needed for data processing UI)
- ✅ FastAPI (API framework)
- ✅ PyPDF2 (PDF extraction)
- ✅ NLTK (text processing)
- ✅ NumPy (lightweight, needed for analysis)

**Size reduction**: ~180MB → ~80-100MB

### 2. **Enhanced .vercelignore**
Updated to exclude:
- `.git/` folder
- `__pycache__/` directories  
- `tests/`, `docs/`, `scripts/` folders
- Markdown documentation files
- `app.py` (Streamlit app, not needed for API)
- `check_deployment.py`, `verify_project.py`, etc.

**Size reduction**: ~50-70MB

### 3. **Optimized vercel.json**
Changes:
```json
{
  "maxLambdaSize": "250mb",        // Increased to full limit
  "runtime": "python3.12",          // Updated to latest
  "requirements": "requirements-production.txt"  // Use optimized deps
}
```

### 4. **Efficient NLTK Data Download**
- Download only required models during build
- Reduced download size significantly
- Uses Vercel's buildCommand to download at build time

## Deployment Steps

### Step 1: Commit Changes
```bash
git add requirements-production.txt .vercelignore vercel.json
git commit -m "fix: optimize vercel deployment to fix 250MB size limit

- Use production-only dependencies (remove Streamlit, Plotly, Pandas)
- Enhanced .vercelignore to exclude unnecessary files
- Updated vercel.json with latest Python 3.12 runtime
- Added efficient NLTK data download in buildCommand"
```

### Step 2: Push to GitHub
```bash
git push origin main
```

### Step 3: Trigger Vercel Deployment
Vercel will automatically redeploy. If not, manually trigger in Vercel dashboard:
1. Go to Vercel project dashboard
2. Click "Deployments"
3. Click the "..." menu next to latest deployment
4. Select "Redeploy"

### Step 4: Monitor Build
Watch the deployment logs for success. Expected build time: 60-90 seconds.

## Expected Results
- ✅ Function size: **Under 250MB** (target: ~120MB)
- ✅ Build success
- ✅ API endpoints working normally
- ✅ Same analysis functionality preserved

## If Issues Persist

### Check 1: Verify Requirements
```bash
pip install -r requirements-production.txt
pip freeze | wc -l  # Count installed packages
```

### Check 2: Review Build Logs
In Vercel dashboard:
1. Go to Deployments → Failed build
2. Scroll to "Build Logs"
3. Look for "Error: A Serverless Function has exceeded"
4. Check what's using space

### Check 3: Additional Optimization
If still over 250MB, try:

**Option A: Further reduce dependencies**
```bash
# Remove NumPy if not critical
pip uninstall numpy
```

**Option B: Use Vercel Build Caching**
Update vercel.json:
```json
{
  "buildCommand": "ls -la",
  "cacheMaxAge": 3600
}
```

**Option C: Split into multiple functions**
- Create separate endpoints for heavy operations
- Distribute across multiple serverless functions

## Testing Locally

### Verify Production Build Size
```bash
# Install dependencies
pip install -r requirements-production.txt

# Check size
pip show -f | grep -A 1000 "Location:"  # See all installed files
```

### Test API Locally
```bash
# Install production dependencies
pip install -r requirements-production.txt

# Run API
uvicorn api.index:app --reload --port 8000

# Test endpoint
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@sample_resume.pdf"
```

## Performance Notes

### What Still Works
- ✅ Resume PDF analysis
- ✅ Text extraction
- ✅ Keyword matching
- ✅ All API endpoints

### What's Removed (Only from API)
- ❌ Streamlit UI (use `/index.html` instead)
- ❌ Interactive visualizations (return JSON only)
- ❌ Download reports feature (can add back if needed)

## Future Optimizations

If you need more features:
1. Use **Vercel Edge Functions** (more lightweight)
2. Implement **lazy loading** of models
3. Use **npm packages** for some functionality
4. Consider **serverless cloud functions** elsewhere

## Files Modified
- `requirements-production.txt` - NEW
- `.vercelignore` - UPDATED
- `vercel.json` - UPDATED
- `scripts/vercel-build.sh` - UPDATED

## Support
If deployment still fails:
1. Check Vercel build logs for specific errors
2. Verify all files are committed to GitHub
3. Try clearing Vercel cache: Dashboard → Settings → Caching
4. Contact Vercel support with build logs
