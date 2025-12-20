import sys
from pathlib import Path

# Ensure project root on sys.path for imports
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.resume_analyzer import ResumeAnalyzer
from backend.pdf_extractor import extract_text_from_pdf, get_pdf_metadata
from backend.keyword_matcher import calculate_match_score, extract_missing_keywords
import io


def test_analyzer_basic_output():
    """Test basic analyzer functionality."""
    analyzer = ResumeAnalyzer()
    sample_text = "Software engineer with experience in Python, AWS, Docker. Led projects and improved performance by 20%."
    result = analyzer.analyze(sample_text)

    expected_keys = {
        "overall_score",
        "content_score",
        "keyword_score",
        "ats_score",
        "structure_score",
        "completeness_score",
        "skills",
        "keywords",
        "recommendations",
        "word_count",
    }

    assert expected_keys.issubset(result.keys())
    assert isinstance(result["overall_score"], int)
    assert result["overall_score"] <= 100
    assert result["overall_score"] >= 0


def test_skills_extraction():
    """Test skills extraction functionality."""
    analyzer = ResumeAnalyzer()
    text_with_skills = "Proficient in Python, JavaScript, React, AWS, machine learning, and project management."
    result = analyzer.analyze(text_with_skills)
    
    # Should detect some skills
    assert len(result["skills"]) > 0
    
    # Check for specific skills
    skills_lower = [skill.lower() for skill in result["skills"]]
    assert any("python" in skill for skill in skills_lower)


def test_empty_text():
    """Test analyzer with empty text."""
    analyzer = ResumeAnalyzer()
    result = analyzer.analyze("")
    
    # Should still return valid structure
    assert isinstance(result, dict)
    assert "overall_score" in result
    assert result["word_count"] == 0


def test_keyword_matcher():
    """Test job matching functionality."""
    resume_text = "Python developer with Django experience and AWS skills"
    job_description = "Looking for Python developer with Django and cloud experience"
    
    score = calculate_match_score(resume_text, job_description)
    
    assert isinstance(score, int)
    assert 0 <= score <= 100
    assert score > 0  # Should have some match


def test_missing_keywords():
    """Test missing keywords extraction."""
    resume_text = "Python developer with experience"
    job_description = "Looking for Python developer with React, AWS, and Docker experience"
    
    missing = extract_missing_keywords(resume_text, job_description)
    
    assert isinstance(missing, list)
    # Should identify React, AWS, Docker as missing
    assert len(missing) > 0


def test_pdf_extractor_error_handling():
    """Test PDF extractor error handling."""
    # Test with invalid data
    invalid_data = io.BytesIO(b"This is not a PDF")
    result = extract_text_from_pdf(invalid_data)
    
    # Should return error message
    assert "Error" in result


def test_score_boundaries():
    """Test that all scores are within valid boundaries."""
    analyzer = ResumeAnalyzer()
    
    # Test with various text lengths
    test_texts = [
        "Short.",
        "This is a medium length resume with some skills like Python and project management experience.",
        "This is a very long resume text that contains many details about experience, education, skills including Python, Java, JavaScript, React, AWS, Docker, machine learning, project management, leadership, communication, teamwork, and many other technical and soft skills that should be detected by the analyzer. It also includes action verbs like developed, managed, led, achieved, implemented, created, designed, improved, analyzed, collaborated, coordinated, and established which should boost the content score."
    ]
    
    for text in test_texts:
        result = analyzer.analyze(text)
        
        # Check all scores are within bounds
        for key in ["overall_score", "content_score", "keyword_score", "ats_score", "structure_score", "completeness_score"]:
            score = result[key]
            assert 0 <= score <= 100, f"{key} score {score} is out of bounds for text length {len(text)}"


def test_recommendations_generation():
    """Test that recommendations are generated."""
    analyzer = ResumeAnalyzer()
    short_text = "Python developer"
    result = analyzer.analyze(short_text)
    
    # Should have recommendations for improvement
    assert len(result["recommendations"]) > 0
    assert all(isinstance(rec, str) for rec in result["recommendations"])
    assert len(result["recommendations"]) <= 6  # Max 6 recommendations
