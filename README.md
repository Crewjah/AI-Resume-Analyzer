# AI Resume Analyzer

An AI-powered web application that analyzes resumes using Natural Language Processing (NLP) and Machine Learning to provide actionable insights and improvement recommendations.

## Overview

AI Resume Analyzer helps job seekers optimize their resumes by:
- Extracting and evaluating skills using NLP
- Calculating keyword density and relevance
- Matching resumes with job descriptions
- Providing ATS (Applicant Tracking System) compatibility scores
- Offering personalized improvement suggestions

## Features

- **Smart Resume Analysis**: Uses SpaCy and NLP to extract skills, keywords, and key information
- **Job Matching**: Calculates compatibility score between resume and job description using TF-IDF and cosine similarity
- **ATS Compatibility Check**: Ensures your resume passes through Applicant Tracking Systems
- **Visual Analytics**: Interactive charts and graphs using Plotly
- **Real-time Feedback**: Instant analysis with actionable recommendations
- **Modern UI**: Clean, responsive interface with smooth animations

## Tech Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python
- **NLP**: SpaCy, Transformers
- **ML**: Scikit-learn (TF-IDF, Cosine Similarity)
- **Data Processing**: Pandas, NumPy
- **PDF Processing**: PyPDF2
- **Visualization**: Plotly
- **Version Control**: Git, GitHub

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Crewjah/AI-Resume-Analyzer.git
   cd AI-Resume-Analyzer
   ```

2. **Run setup script** (Linux/Mac)
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Manual setup** (Windows or alternative)
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Download SpaCy model
   python -m spacy download en_core_web_sm
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   - Open your browser and navigate to `http://localhost:8501`

## Usage

1. **Upload Resume**: Click on the file uploader and select your resume (PDF format)
2. **Add Job Description** (Optional): Paste the job description to get a match score
3. **Analyze**: Click the "Analyze Resume" button
4. **Review Results**: 
   - View your overall score and individual metric scores
   - Check identified skills and keywords
   - Read personalized recommendations
   - Analyze score breakdown with visual charts

## Project Structure

```
AI-Resume-Analyzer/
├── app.py                      # Main Streamlit application
├── backend/                    # Backend modules
│   ├── __init__.py
│   ├── resume_analyzer.py     # Core analysis logic
│   ├── pdf_extractor.py       # PDF text extraction
│   └── keyword_matcher.py     # Job matching algorithms
├── .streamlit/                 # Streamlit configuration
│   └── config.toml
├── docs/                       # Documentation
│   ├── CONTRIBUTING.md
│   ├── API.md
│   └── DEPLOYMENT.md
├── requirements.txt            # Python dependencies
├── setup.sh                    # Setup script
├── .gitignore
└── README.md
```

## Scoring Metrics

The application evaluates resumes across multiple dimensions:

- **Overall Score**: Weighted average of all metrics
- **Content Quality**: Word count, action verbs, structure
- **Keyword Optimization**: Keyword diversity and relevance
- **ATS Compatibility**: Format and structure for ATS systems
- **Structure Score**: Presence of key sections and proper formatting
- **Completeness**: Essential information coverage
- **Job Match Score**: Similarity with job description (when provided)

## Contributing

We welcome contributions from the community! This project is part of Social Winter of Code 2026.

### How to Contribute

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Open a Pull Request

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=backend tests/
```

### Code Style

We follow PEP 8 style guidelines. Format your code using:

```bash
pip install black flake8
black .
flake8 .
```

## Deployment

### Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select the main file (`app.py`)
5. Deploy

### Deploy on Vercel

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed Vercel deployment instructions.

## Known Limitations

- Currently supports PDF files only
- Best results with text-based PDFs (not scanned images)
- English language resumes only
- Requires internet connection for initial model download

## Future Enhancements

- Support for DOCX and TXT file formats
- Multi-language support
- Resume template suggestions
- Industry-specific analysis
- Resume comparison feature
- Export detailed reports as PDF

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Social Winter of Code 2026 for the opportunity
- SpaCy and Hugging Face for NLP models
- Streamlit for the amazing framework
- All contributors and supporters

## Contact

- **Project Maintainer**: Crewjah
- **GitHub**: [https://github.com/Crewjah/AI-Resume-Analyzer](https://github.com/Crewjah/AI-Resume-Analyzer)
- **Issues**: [GitHub Issues](https://github.com/Crewjah/AI-Resume-Analyzer/issues)

## Support

If you find this project helpful, please consider:
- Giving it a star on GitHub
- Sharing it with others
- Contributing to the codebase
- Reporting bugs and suggesting features

---

Made with Python and Streamlit | Social Winter of Code 2026
