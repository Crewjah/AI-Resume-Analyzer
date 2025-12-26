# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive Streamlit web application (`app.py`)
- Interactive visualizations with Plotly charts
- Job matching functionality with similarity scoring
- Enhanced test suite with comprehensive unit tests
- GitHub issue templates for better contribution management
- Pull request template for standardized contributions
- PowerShell setup script for Windows users
- Additional test files for better coverage

### Changed
- Updated requirements.txt to include all necessary dependencies
- Enhanced requirements-dev.txt with development tools
- Improved test coverage and added multiple test scenarios

### Fixed
- Missing main Streamlit application implementation
- Dependency mismatches between documentation and requirements

## [1.0.0] - 2026-12-20

### Added
- Initial release of AI Resume Analyzer
- Core resume analysis engine with NLP capabilities
- FastAPI backend for serverless deployment
- PDF text extraction functionality
- Job description matching algorithms
### Planned
- DOCX file format support
- Resume comparison feature
- Dark mode UI theme
- Enhanced NLP with advanced models
- Persistent storage option

## [2.0.0] - 2025-12-26

- Comprehensive documentation (API, Contributing, Deployment guides)
- **Multi-Page Application**: 4-page Streamlit interface (Upload, Results, Job Matching, Settings)
- **Multi-File Upload**: Analyze multiple resumes simultaneously with file management
- **Session State Management**: Maintain analysis results across pages
- **Interactive Visualizations**: Radar, Bar, Donut, and Gauge charts using Plotly 5.18.0
- **File Management**: Remove individual files with delete buttons
- **Export Functionality**: Download results as CSV and JSON
- **Customizable Weights**: Adjust analysis parameters in Settings page
- **Quick Statistics Dashboard**: Overview metrics on Results page
- **Job Match Threshold**: Adjustable threshold slider for job matching
- **Professional UI/UX**: Custom CSS with Inter font and Font Awesome icons
  - Keyword optimization scoring
  - ATS compatibility checking
- **Application Structure**: Reorganized into multi-page architecture
- **File Size Limit**: Standardized to 5MB per file
- **Port Configuration**: Default port changed to 8502
- **UI Theme**: Upgraded to professional gradient design (#F5F7FA to #C3CFE2)
- **Chart API**: Updated to use `use_container_width=True` instead of deprecated `width='stretch'`
- **Version Display**: Consistent v2.0.0 across all pages
- **Job Matching**: TF-IDF and cosine similarity algorithms
- **Recommendations**: Personalized improvement suggestions
- **Critical Bug**: Fixed `StreamlitInvalidWidthError` with `st.dataframe(width=None)`
- **Chart Rendering**: Replaced deprecated plotly chart width parameters
- **Version Consistency**: Standardized version number to v2.0.0
- **Navigation States**: Fixed sidebar active state inconsistencies
- **Job Matching**: Improved button placement and flow
- **Documentation**: Updated all docs to remove fake/outdated information

### Removed
- Deprecated width parameters from plotly charts
- Fake performance statistics from documentation
- Outdated deployment instructions

### Technical Details
- **Dependencies**: Streamlit 1.52.2, Plotly 5.18.0, Pandas 2.3.3, PyPDF2 3.0.1
- **Code Size**: 1022 lines in main app.py
- **Pages**: 4 dedicated pages with navigation
- **Charts**: 4 visualization types (Radar, Bar, Donut, Gauge)
- **File Formats**: PDF and TXT support
### Technical Stack
- **Backend**: Python, FastAPI
- **Frontend**: Streamlit, HTML/CSS/JavaScript
*Note: This version predates current v2.0.0 release*

- **ML/NLP**: Scikit-learn, Custom algorithms
- **Visualization**: Plotly
- **PDF Processing**: PyPDF2
- **CI/CD**: GitHub Actions

### Documentation
- Professional README with usage instructions
- Project architecture and design decisions

### Planned Features
- [ ] Support for DOCX and other document formats
- [ ] Multi-language resume analysis
### v2.0.0 - Major Update (December 26, 2025)
This release represents a complete overhaul of the application with a modern multi-page interface and enhanced user experience.

**Major Highlights:**
- Multi-page Streamlit application with sidebar navigation
- Interactive Plotly visualizations on all pages
- Multi-file upload and analysis capabilities
- Customizable analysis weights and settings
- Professional UI with custom CSS and animations
- Comprehensive bug fixes and stability improvements

**Breaking Changes:**
- Application structure completely reorganized
- Default port changed from 8501 to 8502
- File size limit reduced to 5MB per file

**Migration Guide:**
- No migration needed for new installations
- Existing users: Simply pull latest code and restart application
- All analysis features remain compatible

**Getting Started:**
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run application: `streamlit run app.py --server.port 8502`
4. Access at `http://localhost:8502`

- [ ] Industry-specific scoring models
Initial foundational release with basic analysis capabilities.
We welcome contributions from the community! This project is part of Social Winter of Code 2026.

- 🐛 [Report bugs](https://github.com/Crewjah/AI-Resume-Analyzer/issues/new?template=bug_report.md)
- 💡 [Request features](https://github.com/Crewjah/AI-Resume-Analyzer/issues/new?template=feature_request.md)
- 👩‍💻 [Contribute code](https://github.com/Crewjah/AI-Resume-Analyzer/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
- 📖 [Improve documentation](docs/CONTRIBUTING.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Social Winter of Code 2026 for providing the platform
- Open source community for inspiration and contributions
- All contributors who help improve this project

---

**Made with ❤️ by the AI Resume Analyzer team**