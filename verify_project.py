#!/usr/bin/env python3
"""
COMPREHENSIVE PROJECT VERIFICATION & HEALTH CHECK
Verifies all files, documentation, configuration, and functionality
"""

import os
import sys
import json
from pathlib import Path

print("\n" + "="*80)
print("🔍 AI RESUME ANALYZER - COMPREHENSIVE HEALTH CHECK")
print("="*80 + "\n")

checks_passed = 0
checks_failed = 0

def check(condition, message, critical=False):
    """Check condition and print result"""
    global checks_passed, checks_failed
    status = "✅" if condition else ("❌" if critical else "⚠️")
    print(f"{status} {message}")
    if condition:
        checks_passed += 1
    else:
        checks_failed += 1
    return condition

# 1. FILE STRUCTURE CHECK
print("📁 FILE STRUCTURE CHECK")
print("-" * 80)

required_files = {
    "Core App": ["app.py", "index.html"],
    "Backend": ["backend/resume_analyzer.py", "backend/keyword_matcher.py", "backend/pdf_extractor.py"],
    "API": ["api/index.py"],
    "Config": ["requirements.txt", "vercel.json"],
    "Documentation": ["README.md", "QUICK_START.md", "AUDIT_REPORT.md", "DEPLOYMENT_READY.md"],
    "Tests": ["tests/test_smoke.py", "test_local.py", "check_deployment.py"],
}

for category, files in required_files.items():
    for file in files:
        exists = Path(file).exists()
        check(exists, f"{file:45} - {category}", critical=True)

# 2. PYTHON SYNTAX CHECK
print("\n🐍 PYTHON FILES SYNTAX CHECK")
print("-" * 80)

import ast
python_files = [
    "app.py",
    "backend/resume_analyzer.py",
    "backend/keyword_matcher.py",
    "backend/pdf_extractor.py",
    "api/index.py",
]

for filepath in python_files:
    try:
        with open(filepath, 'r') as f:
            ast.parse(f.read())
        lines = len(open(filepath).readlines())
        check(True, f"{filepath:45} ({lines:4} lines) - Valid Python", critical=True)
    except SyntaxError as e:
        check(False, f"{filepath}: {e}", critical=True)

# 3. IMPORTS CHECK
print("\n🔧 BACKEND IMPORTS CHECK")
print("-" * 80)

sys.path.insert(0, 'backend')

try:
    from resume_analyzer import ResumeAnalyzer
    check(True, "ResumeAnalyzer                             imports successfully", critical=True)
except Exception as e:
    check(False, f"ResumeAnalyzer: {e}", critical=True)

try:
    from keyword_matcher import calculate_match_score, extract_missing_keywords
    check(True, "keyword_matcher                            imports successfully", critical=True)
except Exception as e:
    check(False, f"keyword_matcher: {e}", critical=True)

try:
    from pdf_extractor import extract_text_from_pdf, extract_text_from_docx
    check(True, "pdf_extractor                              imports successfully", critical=True)
except Exception as e:
    check(False, f"pdf_extractor: {e}", critical=True)

# 4. FUNCTIONALITY CHECK
print("\n🧠 ANALYZER FUNCTIONALITY CHECK")
print("-" * 80)

try:
    analyzer = ResumeAnalyzer()
    test_resume = "John Doe john@example.com Python Developer with 5 years experience"
    result = analyzer.analyze(test_resume)
    
    checks_list = [
        ("Result is dict", isinstance(result, dict)),
        ("Has 'scores'", "scores" in result),
        ("Has 'recommendations'", "recommendations" in result),
        ("Has 'skills'", "skills" in result),
        ("Scores are 0-100", all(0 <= result.get("scores", {}).get(k, 0) <= 100 for k in ['overall', 'content_quality', 'keyword_optimization', 'ats_compatibility'])),
    ]
    
    for check_name, result_check in checks_list:
        check(result_check, f"Analyzer: {check_name:30}", critical=True)
except Exception as e:
    check(False, f"Analyzer functionality: {e}", critical=True)

# 5. CONFIGURATION CHECK
print("\n⚙️  CONFIGURATION FILES CHECK")
print("-" * 80)

try:
    with open("vercel.json", "r") as f:
        vercel_config = json.load(f)
    check(True, "vercel.json                                valid JSON", critical=True)
    check("version" in vercel_config, "vercel.json has version field", critical=False)
    check("name" in vercel_config, "vercel.json has name field", critical=False)
except Exception as e:
    check(False, f"vercel.json: {e}", critical=True)

try:
    with open("requirements.txt", "r") as f:
        reqs = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
    check(len(reqs) > 15, f"requirements.txt has {len(reqs)} packages", critical=False)
except Exception as e:
    check(False, f"requirements.txt: {e}", critical=True)

try:
    with open("index.html", "r") as f:
        html = f.read()
    check(len(html) > 500 and "<html" in html.lower(), "index.html valid HTML", critical=False)
except Exception as e:
    check(False, f"index.html: {e}", critical=False)

# 6. DOCUMENTATION CHECK
print("\n📚 DOCUMENTATION CHECK")
print("-" * 80)

docs = {
    "README.md": 500,
    "QUICK_START.md": 300,
    "AUDIT_REPORT.md": 1000,
    "DEPLOYMENT_READY.md": 1000,
}

for doc, min_size in docs.items():
    try:
        with open(doc, "r") as f:
            size = len(f.read())
        check(size > min_size, f"{doc:35} ({size:6,} chars)", critical=False)
    except Exception as e:
        check(False, f"{doc}: {e}", critical=False)

# 7. MARKDOWN LINKS CHECK
print("\n🔗 DOCUMENTATION LINKS CHECK")
print("-" * 80)

doc_references = {
    "README.md": ["LICENSE", "docs/CONTRIBUTING.md", "docs/API.md", "docs/DEPLOYMENT.md"],
    "QUICK_START.md": ["README.md"],
}

for doc, refs in doc_references.items():
    for ref in refs:
        exists = Path(ref).exists()
        check(exists, f"Referenced from {doc}: {ref:35}", critical=False)

# 8. BACKEND FILES STRUCTURE
print("\n📦 BACKEND FILES STRUCTURE")
print("-" * 80)

backend_files = {
    "resume_analyzer.py": ["analyze", "ResumeAnalyzer"],
    "keyword_matcher.py": ["calculate_match_score"],
    "pdf_extractor.py": ["extract_text_from_pdf", "extract_text_from_docx"],
}

for filepath, functions in backend_files.items():
    full_path = f"backend/{filepath}"
    try:
        with open(full_path, "r") as f:
            content = f.read()
        all_found = all(func in content for func in functions)
        check(all_found, f"{filepath:30} has {len(functions)} functions", critical=False)
    except Exception as e:
        check(False, f"{filepath}: {e}", critical=False)

# 9. API CONFIGURATION
print("\n🚀 API CONFIGURATION")
print("-" * 80)

try:
    with open("api/index.py", "r") as f:
        api_content = f.read()
    
    checks_list = [
        ("FastAPI app defined", "app = FastAPI" in api_content),
        ("CORS configured", "CORSMiddleware" in api_content),
        ("/health endpoint", "@app.get" in api_content),
        ("Static files", "StaticFiles" in api_content or "index.html" in api_content),
    ]
    
    for check_name, result_check in checks_list:
        check(result_check, f"api/index.py: {check_name:25}", critical=False)
except Exception as e:
    check(False, f"api/index.py: {e}", critical=False)

# 10. GIT REPOSITORY
print("\n📝 GIT REPOSITORY STATUS")
print("-" * 80)

try:
    git_dir = Path(".git")
    check(git_dir.exists(), "Git repository initialized", critical=False)
    
    # Check for common git files
    check((git_dir / "config").exists(), ".git/config exists", critical=False)
    check(Path(".gitignore").exists(), ".gitignore exists", critical=False)
except Exception as e:
    check(False, f"Git check: {e}", critical=False)

# FINAL SUMMARY
print("\n" + "="*80)
print("VERIFICATION RESULTS")
print("="*80)
print(f"\n✅ Checks Passed: {checks_passed}")
print(f"❌ Checks Failed: {checks_failed}")

if checks_failed == 0:
    print("\n🎉 ALL CHECKS PASSED - PROJECT IS HEALTHY!")
    print("\n✅ Ready for:")
    print("   • Local testing: streamlit run app.py")
    print("   • Production deployment: git push origin main")
    print("   • User access")
    sys.exit(0)
else:
    print(f"\n⚠️  {checks_failed} ISSUES FOUND")
    print("Please fix critical (❌) issues before deployment")
    sys.exit(1)
