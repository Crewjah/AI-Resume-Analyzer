"""
Unit tests for the resume analyzer module.
"""
import sys
from pathlib import Path

# Ensure project root on sys.path for imports
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from backend.resume_analyzer import ResumeAnalyzer


class TestResumeAnalyzer:
    """Test suite for ResumeAnalyzer class."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.analyzer = ResumeAnalyzer()
    
    def test_initialization(self):
        """Test analyzer initialization."""
        assert self.analyzer.technical_skills
        assert self.analyzer.soft_skills
        assert len(self.analyzer.technical_skills) > 30
        assert len(self.analyzer.soft_skills) > 10
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        dirty_text = "  Hello  World!!!  @#$%  "
        clean_text = self.analyzer._clean_text(dirty_text)
        
        # Text should be lowercased and cleaned
        assert "hello" in clean_text
        assert "world" in clean_text
        assert not clean_text.startswith(" ")
        assert not clean_text.endswith(" ")

    def test_extract_skills(self):
        """Test skills extraction."""
        text = "I have experience with Python, JavaScript, leadership, and teamwork."
        skills = self.analyzer._extract_skills(text.lower())
        
        assert "Python" in skills
        assert "Javascript" in skills or "JavaScript" in skills
        assert "Leadership" in skills
        assert "Teamwork" in skills
    
    def test_extract_keywords(self):
        """Test keyword extraction."""
        text = "python developer with experience in web development and software engineering"
        keywords = self.analyzer._extract_keywords(text)
        
        assert isinstance(keywords, dict)
        assert len(keywords) > 0
        # Should filter out stopwords
        assert "with" not in keywords
        assert "the" not in keywords
    
    def test_content_score_calculation(self):
        """Test content score calculation."""
        # Test optimal word count
        optimal_text = " ".join(["word"] * 500)  # 500 words
        score = self.analyzer._calculate_content_score(optimal_text)
        assert score >= 85
        
        # Test too short
        short_text = " ".join(["word"] * 50)  # 50 words
        score = self.analyzer._calculate_content_score(short_text)
        assert score <= 80
    
    def test_keyword_score_calculation(self):
        """Test keyword score calculation."""
        # Test good keyword diversity
        many_keywords = {f"keyword{i}": 1 for i in range(20)}
        score = self.analyzer._calculate_keyword_score(many_keywords)
        assert score >= 90
        
        # Test poor keyword diversity
        few_keywords = {"keyword1": 5}
        score = self.analyzer._calculate_keyword_score(few_keywords)
        assert score <= 70
    
    def test_ats_score_calculation(self):
        """Test ATS score calculation."""
        # Test good ATS text
        good_text = "experience education skills projects john.doe@email.com"
        score = self.analyzer._calculate_ats_score(good_text)
        assert score >= 70
        
        # Test poor ATS text (no email, no sections)
        poor_text = "just some random text with no structure"
        score = self.analyzer._calculate_ats_score(poor_text)
        assert score <= 70
    
    def test_structure_score_calculation(self):
        """Test structure score calculation."""
        # Test well-structured resume
        structured_text = "john@email.com experience at company education degree from university skills python java 2020 2021"
        score = self.analyzer._calculate_structure_score(structured_text)
        assert score >= 70
        
        # Test poorly structured resume
        unstructured_text = "just some text without any structure"
        score = self.analyzer._calculate_structure_score(unstructured_text)
        assert score <= 70
    
    def test_completeness_score_calculation(self):
        """Test completeness score calculation."""
        # Test complete resume
        complete_text = "john@email.com experience software engineer education computer science skills python 2020"
        score = self.analyzer._calculate_completeness_score(complete_text)
        assert score >= 70
        
        # Test incomplete resume
        incomplete_text = "some experience"
        score = self.analyzer._calculate_completeness_score(incomplete_text)
        assert score <= 50
    
    def test_recommendations_generation(self):
        """Test recommendation generation."""
        # Test that recommendations are generated during analysis
        short_text = "python developer with 2 years experience"
        result = self.analyzer.analyze(short_text)
        
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)
        assert len(result["recommendations"]) > 0

    def test_full_analysis(self):
        """Test complete analysis workflow."""
        sample_resume = """
        John Doe
        Software Engineer
        john.doe@email.com
        
        Experience:
        Software Engineer at Tech Company (2020-2023)
        - Developed web applications using Python and JavaScript
        - Led team of 5 developers
        - Improved system performance by 30%
        
        Education:
        Bachelor of Science in Computer Science
        University of Technology (2016-2020)
        
        Skills:
        Python, JavaScript, React, AWS, Docker, Machine Learning
        Leadership, Team Management, Problem Solving
        """
        
        result = self.analyzer.analyze(sample_resume)
        
        # Verify result structure - scores are nested in 'scores' dict
        assert "scores" in result
        assert "technical_skills" in result
        assert "soft_skills" in result
        assert "recommendations" in result
        assert "word_count" in result
        
        # Verify score ranges in nested structure
        for score_key in ["overall_score", "content_quality", "keyword_optimization", "ats_compatibility", "structure_score", "completeness"]:
            assert 0 <= result["scores"][score_key] <= 100
        
        # Should detect multiple skills combined
        total_skills = len(result["technical_skills"]) + len(result["soft_skills"])
        assert total_skills >= 3
        
        # Should have reasonable word count
        assert result["word_count"] > 50
        
        # Should provide recommendations
        assert len(result["recommendations"]) > 0