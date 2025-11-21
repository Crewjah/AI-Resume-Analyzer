# AI Resume Analyzer

A professional web application for analyzing resumes using AI and machine learning. Get insights on ATS compatibility, skills analysis, and job matching.

## Features

- **Resume Analysis**: Upload and analyze resume files
- **ATS Scoring**: Get compatibility scores for Applicant Tracking Systems
- **Skills Detection**: Identify technical and professional skills
- **Job Matching**: Compare resume against job descriptions
- **Recommendations**: Get actionable improvement suggestions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Crewjah/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run streamlit_app.py
```

## Deployment

### Vercel Deployment

1. Push your code to GitHub
2. Connect your GitHub repository to Vercel
3. Vercel will automatically detect the Streamlit app
4. Deploy with default settings

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