# AI Resume Analyzer Setup Script for Windows PowerShell
# Run this script to set up the development environment

Write-Host "🤖 Setting up AI Resume Analyzer..." -ForegroundColor Cyan

# Check if Python is available
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Check if activation was successful
if ($env:VIRTUAL_ENV) {
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host "⬆️ Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "📚 Installing requirements..." -ForegroundColor Yellow
pip install -r requirements-dev.txt

# Check if requirements were installed successfully
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Requirements installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install requirements" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "  streamlit run app.py" -ForegroundColor White
Write-Host ""
Write-Host "To run the API server:" -ForegroundColor Cyan
Write-Host "  uvicorn api.analyze:app --reload --port 8000" -ForegroundColor White
Write-Host ""
Write-Host "To run tests:" -ForegroundColor Cyan
Write-Host "  pytest tests/" -ForegroundColor White
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Yellow