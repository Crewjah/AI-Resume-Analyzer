# Contributing to AI Resume Analyzer

Thank you for your interest in contributing to AI Resume Analyzer! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. We expect all contributors to:

- Be respectful and considerate
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Accept responsibility for mistakes
- Prioritize the community's best interests

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- GitHub account
- Basic understanding of NLP concepts (helpful but not required)

### Setting Up Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-Resume-Analyzer.git
   cd AI-Resume-Analyzer
   ```

3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/Crewjah/AI-Resume-Analyzer.git
   ```

4. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

## How to Contribute

### Reporting Bugs

If you find a bug:

1. Check if the issue already exists in [GitHub Issues](https://github.com/Crewjah/AI-Resume-Analyzer/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Your environment details (OS, Python version, etc.)

### Suggesting Features

For feature requests:

1. Check existing issues and discussions
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach
   - Any relevant examples

### Contributing Code

Areas where you can contribute:

- **Bug fixes**: Fix reported issues
- **New features**: Implement planned features
- **Documentation**: Improve docs, add examples
- **Tests**: Add or improve test coverage
- **Performance**: Optimize existing code
- **UI/UX**: Enhance user interface and experience

## Development Workflow

1. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes**:
   - Write clean, documented code
   - Follow coding standards
   - Add tests for new features
   - Update documentation

3. **Test your changes**:
   ```bash
   # Run the application
   streamlit run app.py
   
   # Run tests (if available)
   pytest tests/
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Type: Brief description"
   ```

5. **Keep your branch updated**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Keep functions focused and concise
- Add docstrings to all functions and classes

Example:
```python
def calculate_score(text: str, keywords: List[str]) -> int:
    """
    Calculate the relevance score based on keyword matching.
    
    Args:
        text: The text to analyze
        keywords: List of keywords to match
        
    Returns:
        Score as integer between 0 and 100
    """
    # Implementation
    pass
```

### Code Formatting

Use Black for code formatting:
```bash
pip install black
black .
```

Use Flake8 for linting:
```bash
pip install flake8
flake8 .
```

### Documentation

- Add comments for complex logic
- Update README.md for significant changes
- Document new features in docs/
- Include docstrings with type hints

## Commit Guidelines

Follow conventional commit format:

```
type: subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: Add support for DOCX file format

fix: Resolve PDF extraction error for scanned documents

docs: Update installation instructions for Windows

refactor: Simplify keyword extraction logic
```

## Pull Request Process

### Before Submitting

- Ensure your code follows the style guide
- All tests pass
- Documentation is updated
- Commit messages are clear
- Branch is up to date with main

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged
4. Your contribution will be acknowledged

## Project Structure

```
AI-Resume-Analyzer/
├── app.py                 # Main Streamlit app
├── backend/               # Core backend logic
│   ├── resume_analyzer.py
│   ├── pdf_extractor.py
│   └── keyword_matcher.py
├── docs/                  # Documentation
├── tests/                 # Test files
└── requirements.txt       # Dependencies
```

## Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=backend tests/

# Run specific test file
pytest tests/test_analyzer.py
```

### Writing Tests

- Write tests for new features
- Ensure good code coverage
- Use descriptive test names
- Include edge cases

Example:
```python
def test_extract_skills_from_resume():
    """Test skill extraction from sample resume text."""
    analyzer = ResumeAnalyzer()
    text = "Python, Java, Machine Learning, Docker"
    skills = analyzer._extract_skills(text)
    
    assert 'Python' in skills
    assert 'Java' in skills
    assert len(skills) > 0
```

## Need Help?

- Check existing documentation
- Ask in GitHub Discussions
- Open an issue for clarification
- Reach out to maintainers

## Recognition

All contributors will be:
- Listed in the project contributors
- Acknowledged in release notes
- Appreciated for their valuable time and effort

Thank you for contributing to AI Resume Analyzer!
