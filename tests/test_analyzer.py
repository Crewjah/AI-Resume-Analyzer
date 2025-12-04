import pytest
from src.analyzer import ResumeAnalyzer


def test_validate_empty_text():
    ra = ResumeAnalyzer()
    res = ra.validate_resume_text("")
    assert res['valid'] is False
    assert 'No text' in res['reason'] or 'could not' in res['reason']


def test_validate_short_text():
    ra = ResumeAnalyzer()
    short = "John Doe\nDeveloper\nEmail: john@example.com"
    res = ra.validate_resume_text(short)
    assert res['valid'] is False
    assert 'too short' in res['reason']


def test_validate_good_text():
    ra = ResumeAnalyzer()
    # Construct a minimal plausible resume-like text (~60 words)
    words = ["Experienced"] * 60
    text = " ".join(words)
    res = ra.validate_resume_text(text)
    assert res['valid'] is True


def test_detect_skills_word_boundary():
    ra = ResumeAnalyzer()
    text = "I used C and Python in projects. Also familiar with Docker and AWS."
    skills = ra.detect_skills(text)
    names = [s['name'] for s in skills]
    assert 'Python' in names
    assert 'Docker' in names
    assert 'AWS' in names
    # Ensure 'SQL' is not detected accidentally
    assert 'SQL' not in names
