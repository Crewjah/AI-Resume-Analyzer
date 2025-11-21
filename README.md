# 🤖 AI Resume Analyzer

![AI Resume Analyzer](https://img.shields.io/badge/AI-Resume%20Analyzer-blue?style=for-the-badge&logo=artificial-intelligence)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)
![Machine Learning](https://img.shields.io/badge/ML-Powered-orange?style=for-the-badge&logo=tensorflow)

A beautiful, modern web application that uses **Natural Language Processing (NLP)** and **Machine Learning** to analyze resumes intelligently. Get comprehensive insights, ATS compatibility scores, and personalized recommendations to improve your resume.

## ✨ Features

### 🎯 Core Analysis
- **Smart Resume Parsing** - Extracts text from PDF, DOCX, and TXT files
- **Skills Detection** - Identifies technical and soft skills with confidence scores
- **ATS Compatibility** - Calculates Applicant Tracking System compatibility score
- **Job Matching** - Compares resume against job descriptions for compatibility
- **Experience Analysis** - Extracts and analyzes work experience and education

### 🎨 Beautiful UI/UX
- **Modern Design** - Gradient backgrounds and smooth animations
- **Responsive Layout** - Works perfectly on desktop and mobile
- **Interactive Charts** - Plotly-powered visualizations and gauges
- **Real-time Analysis** - Live progress indicators and animated metrics
- **Dark/Light Theme** - Beautiful color schemes with CSS animations

### 📊 Advanced Analytics
- **Skill Radar Charts** - Visual representation of skill categories
- **Compatibility Gauges** - Beautiful score displays with color coding
- **Keyword Analysis** - Missing and matching keyword identification
- **Sentiment Analysis** - Resume tone and writing style evaluation
- **Industry Matching** - Industry-specific keyword optimization

### 💡 AI-Powered Recommendations
- **Personalized Suggestions** - Tailored improvement recommendations
- **Priority-Based** - High, medium, and low priority suggestions
- **Industry-Specific** - Recommendations based on target industry
- **Actionable Insights** - Clear steps to improve resume effectiveness

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download spaCy model**
```bash
python -m spacy download en_core_web_sm
```

5. **Run the application**
```bash
streamlit run app.py
```

6. **Open in browser**
Visit `http://localhost:8501` to use the application

## 🎨 UI Showcase

### Modern Gradient Design
- **Primary Colors**: Purple to Blue gradient (#667eea → #764ba2)
- **Accent Colors**: Pink to Purple gradient (#ff9a9e → #f093fb)
- **Success/Warning/Error**: Green (#0be881), Yellow (#feca57), Red (#ff6b6b)

### Smooth Animations
- **Slide-in effects** for headers and cards
- **Bounce-in animations** for metrics
- **Pulse effects** for upload areas
- **Hover transformations** for interactive elements

### Interactive Components
- **Animated progress bars** during analysis
- **Real-time gauges** for scores
- **Radar charts** for skill visualization
- **Responsive cards** with hover effects

## 📁 Project Structure

```
ai-resume-analyzer/
├── app.py                 # Main Streamlit application
├── resume_analyzer.py     # Core NLP and ML analysis
├── ui_components.py       # Beautiful UI components and charts
├── config.py             # Configuration and settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── assets/              # Static assets (if any)
```

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **Streamlit** - Web framework for rapid development
- **spaCy** - Advanced NLP processing
- **scikit-learn** - Machine learning algorithms
- **Pandas/NumPy** - Data manipulation and analysis

### Frontend & Visualization
- **Plotly** - Interactive charts and graphs
- **Custom CSS** - Modern styling with animations
- **Google Fonts** - Beautiful typography (Poppins)
- **Responsive Design** - Mobile-friendly interface

### NLP & AI Features
- **TextBlob** - Sentiment analysis and text processing
- **TF-IDF Vectorization** - Document similarity matching
- **Cosine Similarity** - Job description matching
- **Regex Patterns** - Information extraction
- **Keyword Density Analysis** - Content optimization

## 📊 Analysis Features

### Resume Parsing
- Extracts text from PDF, DOCX, and TXT files
- Identifies resume sections (Experience, Education, Skills, etc.)
- Extracts contact information and personal details

### Skill Analysis
- **600+ Skills Database** across 6 categories
- Confidence scoring based on frequency and context
- Category-wise skill distribution analysis
- Industry-specific skill recommendations

### ATS Optimization
- Keyword density analysis
- Format compatibility checking
- Section completeness evaluation
- Contact information validation
- Length and readability assessment

### Job Matching
- Semantic similarity analysis with job descriptions
- Missing keyword identification
- Matching keyword highlighting
- Compatibility percentage calculation

## 🎯 Usage Examples

### Basic Analysis
1. Upload your resume (PDF/DOCX/TXT)
2. Select analysis type and depth
3. Choose target industry
4. Click "Analyze Resume"
5. Review comprehensive results

### Job Matching
1. Upload resume
2. Paste job description
3. Run complete analysis
4. See matching and missing keywords
5. Get tailored recommendations

### Skill Enhancement
1. Review detected skills
2. Check skill category distribution
3. See confidence scores
4. Follow improvement suggestions
5. Re-analyze updated resume

## 🔧 Configuration

### Analysis Settings
- **Depth Levels**: 1-5 (affects recommendation detail)
- **Industry Focus**: Technology, Finance, Healthcare, etc.
- **File Size Limit**: 10MB maximum
- **Text Length**: 100-50,000 characters

### UI Customization
- Modify colors in `config.py`
- Adjust chart settings
- Configure animation timing
- Set theme preferences

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit changes** (`git commit -m 'Add AmazingFeature'`)
4. **Push to branch** (`git push origin feature/AmazingFeature`)
5. **Open Pull Request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .

# Check code quality
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

## 🙋‍♂️ Support

Having issues? We're here to help!

- **📧 Email**: support@ai-resume-analyzer.com
- **🐛 Bug Reports**: [GitHub Issues](https://github.com/yourusername/ai-resume-analyzer/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-resume-analyzer/discussions)
- **📚 Documentation**: [Wiki](https://github.com/yourusername/ai-resume-analyzer/wiki)

## 🌟 Acknowledgments

- **Streamlit Team** - For the amazing web framework
- **spaCy Team** - For powerful NLP capabilities
- **Plotly Team** - For beautiful interactive charts
- **Open Source Community** - For inspiration and contributions

---

<div align="center">

**Made with ❤️ by the AI Resume Analyzer Team**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-resume-analyzer?style=social)](https://github.com/yourusername/ai-resume-analyzer)
[![Twitter Follow](https://img.shields.io/twitter/follow/yourusername?style=social)](https://twitter.com/yourusername)

</div>