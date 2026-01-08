# Quick Start Guide

## AI Resume Analyzer - Get Started in 5 Minutes

### Deploy to Vercel (2 minutes)

1. **Visit Vercel**
   - Go to https://vercel.com
   - Sign in with GitHub

2. **Import Project**
   - Click "New Project"
   - Select: `Crewjah/AI-Resume-Analyzer`
   - Click "Import"

3. **Deploy**
   - Vercel auto-detects settings from `vercel.json`
   - Click "Deploy"
   - Wait ~90 seconds

4. **Done!**
   - Your app is live at: `https://ai-resume-analyzer-xxx.vercel.app`
   - Share your URL and start analyzing resumes!

### Test Locally (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Run with uvicorn
uvicorn api.index:app --reload

# Open browser
http://localhost:8000
```

### How to Use

1. **Upload Resume**
   - Click "Upload Resume" tab
   - Choose PDF or TXT file (max 5MB)
   - Optionally add job description
   - Click "Analyze Resume"

2. **View Results**
   - See overall score (0-100%)
   - Review score breakdown by category
   - Check detected skills
   - Read recommendations

3. **Download Report**
   - Click "Download Report" for text file
   - Save for future reference

### Features

✅ **5 Scoring Metrics**
- Content Quality
- Keyword Optimization
- ATS Compatibility
- Structure
- Completeness

✅ **Skills Detection**
- Technical skills (Python, JavaScript, etc.)
- Soft skills (Leadership, Communication, etc.)

✅ **Honest Analysis**
- No fake data
- Transparent algorithms
- Genuine recommendations

### Support

- Read: [README.md](README.md) for full documentation
- Deploy: [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide
- Review: [COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md) for project details

---

**Ready to deploy? Just 3 clicks on Vercel! 🚀**
