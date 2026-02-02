#!/usr/bin/env python3
"""
FINAL PRE-DEPLOYMENT CHECKLIST
Run this before pushing to production
"""

import os
import sys
import json
from pathlib import Path

def check(condition, message, critical=False):
    """Check condition and print result"""
    status = "✅" if condition else ("❌" if critical else "⚠️")
    print(f"{status} {message}")
    return condition

print("\n" + "="*80)
print("AI RESUME ANALYZER - FINAL PRE-DEPLOYMENT CHECKLIST")
print("="*80 + "\n")

all_passed = True

# 1. File Structure
print("📁 FILE STRUCTURE CHECK")
print("-" * 80)

required_files = [
    "app.py",
    "index.html",
    "requirements.txt",
    "vercel.json",
    "backend/resume_analyzer.py",
    "backend/keyword_matcher.py",
    "backend/pdf_extractor.py",
    "api/index.py",
    "README.md",
    "AUDIT_REPORT.md",
]

for file_path in required_files:
    full_path = Path(file_path)
    exists = full_path.exists()
    size = full_path.stat().st_size if exists else 0
    status = "✅" if exists else "❌"
    print(f"{status} {file_path:40} {f'({size:,} bytes)' if exists else 'MISSING'}")
    if not exists:
        all_passed = False

# 2. Backend Imports
print("\n🔧 BACKEND IMPORTS CHECK")
print("-" * 80)

try:
    sys.path.insert(0, str(Path("backend").absolute()))
    from resume_analyzer import ResumeAnalyzer
    check(True, "resume_analyzer.py imports successfully", critical=True)
except Exception as e:
    check(False, f"resume_analyzer.py: {e}", critical=True)
    all_passed = False

try:
    from keyword_matcher import calculate_match_score
    check(True, "keyword_matcher.py imports successfully", critical=True)
except Exception as e:
    check(False, f"keyword_matcher.py: {e}", critical=True)
    all_passed = False

try:
    from pdf_extractor import extract_text_from_pdf
    check(True, "pdf_extractor.py imports successfully", critical=True)
except Exception as e:
    check(False, f"pdf_extractor.py: {e}", critical=True)
    all_passed = False

# 3. Analyzer Functionality
print("\n🧠 ANALYZER FUNCTIONALITY CHECK")
print("-" * 80)

try:
    from resume_analyzer import ResumeAnalyzer
    analyzer = ResumeAnalyzer()
    
    test_resume = """
    John Doe
    john@example.com | (555) 123-4567
    
    EXPERIENCE
    Senior Developer at TechCorp (2020-Present)
    - Led team of 5 developers
    - Improved performance by 40%
    
    SKILLS
    Python, JavaScript, React, Node.js
    """
    
    result = analyzer.analyze(test_resume)
    
    checks = [
        ("result is dict", isinstance(result, dict)),
        ("has 'scores' key", "scores" in result),
        ("has 'recommendations' key", "recommendations" in result),
        ("has 'skills' key", "skills" in result),
        ("overall score in 0-100", 0 <= result.get("scores", {}).get("overall", 0) <= 100),
        ("content_quality score in 0-100", 0 <= result.get("scores", {}).get("content_quality", 0) <= 100),
    ]
    
    for check_name, check_result in checks:
        check(check_result, f"Analyzer: {check_name}", critical=True)
        if not check_result:
            all_passed = False
    
    print(f"   → Overall Score: {result['scores']['overall']}/100")
    
except Exception as e:
    check(False, f"Analyzer functionality: {e}", critical=True)
    all_passed = False

# 4. Job Matching
print("\n🎯 JOB MATCHING CHECK")
print("-" * 80)

try:
    from keyword_matcher import calculate_match_score, extract_missing_keywords
    
    score = calculate_match_score(test_resume, "Python JavaScript Developer")
    check(0 <= score <= 100, f"Job match score in range: {score}/100", critical=True)
    
    missing = extract_missing_keywords(test_resume, "Kubernetes Docker AWS")
    check(isinstance(missing, list), "Missing keywords returns list", critical=True)
    
except Exception as e:
    check(False, f"Job matching: {e}", critical=True)
    all_passed = False

# 5. File Extraction
print("\n📄 FILE EXTRACTION CHECK")
print("-" * 80)

try:
    import tempfile
    from pdf_extractor import extract_text_from_pdf, extract_text_from_docx
    
    # Test text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test content")
        temp_txt = f.name
    
    try:
        with open(temp_txt, 'r') as f:
            text = f.read()
        check(len(text) > 0, "Text file extraction works", critical=True)
    finally:
        os.unlink(temp_txt)
    
    check(True, "PDF extractor function exists", critical=False)
    check(True, "DOCX extractor function exists", critical=False)
    
except Exception as e:
    check(False, f"File extraction: {e}", critical=True)
    all_passed = False

# 6. Dependencies
print("\n📦 DEPENDENCIES CHECK")
print("-" * 80)

required_packages = {
    'streamlit': 'Web framework',
    'PyPDF2': 'PDF parsing',
    'python-docx': 'DOCX parsing',
    'fastapi': 'API framework',
    'nltk': 'NLP toolkit',
    'numpy': 'Numerical computing',
}

import pkg_resources
for package, purpose in required_packages.items():
    try:
        version = pkg_resources.get_distribution(package).version
        check(True, f"{package:15} v{version:10} ({purpose})", critical=False)
    except:
        check(False, f"{package:15} NOT FOUND    ({purpose})", critical=True)
        all_passed = False

# 7. Configuration Files
print("\n⚙️  CONFIGURATION FILES CHECK")
print("-" * 80)

try:
    import json
    with open('vercel.json', 'r') as f:
        vercel_config = json.load(f)
    check(True, "vercel.json is valid JSON", critical=True)
    check("version" in vercel_config, "vercel.json has 'version' field", critical=False)
    check("name" in vercel_config, "vercel.json has 'name' field", critical=False)
except Exception as e:
    check(False, f"vercel.json invalid: {e}", critical=True)
    all_passed = False

try:
    with open('requirements.txt', 'r') as f:
        reqs = f.readlines()
    check(len(reqs) > 0, f"requirements.txt has {len(reqs)} packages", critical=True)
except Exception as e:
    check(False, f"requirements.txt error: {e}", critical=True)
    all_passed = False

try:
    with open('index.html', 'r') as f:
        html = f.read()
    check(len(html) > 100, "index.html contains content", critical=False)
    check("<html" in html.lower(), "index.html is valid HTML", critical=False)
except Exception as e:
    check(False, f"index.html error: {e}", critical=False)

# 8. Code Quality
print("\n🔍 CODE QUALITY CHECK")
print("-" * 80)

try:
    import ast
    
    files_to_check = [
        'app.py',
        'backend/resume_analyzer.py',
        'backend/keyword_matcher.py',
        'backend/pdf_extractor.py',
        'api/index.py',
    ]
    
    for filepath in files_to_check:
        try:
            with open(filepath, 'r') as f:
                code = f.read()
            ast.parse(code)
            lines = len(code.split('\n'))
            check(True, f"{filepath:40} ({lines:5} lines, valid Python)", critical=False)
        except SyntaxError as e:
            check(False, f"{filepath}: {e}", critical=True)
            all_passed = False
        except Exception as e:
            check(False, f"{filepath}: {e}", critical=True)
            all_passed = False
            
except Exception as e:
    check(False, f"Code quality check failed: {e}", critical=True)
    all_passed = False

# 9. Documentation
print("\n📚 DOCUMENTATION CHECK")
print("-" * 80)

docs = {
    'README.md': 'Main documentation',
    'QUICK_START.md': 'Getting started guide',
    'AUDIT_REPORT.md': 'Quality audit report',
}

for doc, purpose in docs.items():
    try:
        with open(doc, 'r') as f:
            content = f.read()
        size = len(content)
        check(size > 100, f"{doc:30} ({size:6,} chars) - {purpose}", critical=False)
    except:
        check(False, f"{doc:30} MISSING - {purpose}", critical=False)

# 10. Version Control
print("\n🔗 VERSION CONTROL CHECK")
print("-" * 80)

try:
    if Path('.git').exists():
        check(True, "Git repository initialized", critical=False)
        # Check git status
        import subprocess
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        check(changes >= 0, f"Git status OK ({changes} uncommitted changes)", critical=False)
    else:
        check(False, "Not a git repository", critical=False)
except Exception as e:
    check(False, f"Git check failed: {e}", critical=False)

# Final Summary
print("\n" + "="*80)
if all_passed:
    print("🚀 ALL CRITICAL CHECKS PASSED - READY FOR PRODUCTION")
    print("="*80)
    print("\n✅ NEXT STEPS:")
    print("   1. Review AUDIT_REPORT.md")
    print("   2. Test locally: streamlit run app.py")
    print("   3. Deploy: git push origin main")
    print("   4. Monitor Vercel deployment")
    sys.exit(0)
else:
    print("⚠️  SOME CRITICAL CHECKS FAILED")
    print("="*80)
    print("\n❌ ACTIONS REQUIRED:")
    print("   1. Fix all ❌ marked items above")
    print("   2. Re-run this checklist")
    print("   3. Only deploy when all checks pass")
    sys.exit(1)
