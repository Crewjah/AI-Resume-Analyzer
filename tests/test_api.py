import requests
import os
import time

BASE = os.environ.get('TEST_API_BASE', 'http://127.0.0.1:5000')


def test_health():
    r = requests.get(f"{BASE}/health")
    assert r.status_code == 200
    data = r.json()
    assert data.get('status') == 'healthy'


def test_analyze_empty(tmp_path):
    # create a tiny text file and post it
    p = tmp_path / "small.txt"
    p.write_text("short")
    with open(p, 'rb') as fh:
        r = requests.post(f"{BASE}/analyze", files={'file': fh})
    assert r.status_code == 400
    data = r.json()
    assert 'error' in data


def test_analyze_sample_resume(tmp_path):
    # Create a simple resume-like txt
    content = "\n".join(["Experienced developer with 5 years of experience in Python, Docker, AWS, and SQL."] * 10)
    p = tmp_path / "resume.txt"
    p.write_text(content)
    with open(p, 'rb') as fh:
        r = requests.post(f"{BASE}/analyze", files={'file': fh})
    assert r.status_code == 200
    data = r.json()
    assert 'ats_score' in data
    assert data.get('skill_count', 0) >= 1
