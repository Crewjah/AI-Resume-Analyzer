import sys
from pathlib import Path

# Ensure project root on sys.path for imports
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.resume_analyzer import ResumeAnalyzer


def test_analyzer_basic_output():
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
