@echo off
echo 🚀 Starting Modern AI Resume Analyzer...
echo =====================================

echo 📍 Starting application on port 8507...

REM Start the modern streamlit app with proper path
".\.venv\Scripts\python.exe" -m streamlit run app.py --server.port 8507 --server.headless false

pause