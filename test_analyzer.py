#!/usr/bin/env python3
"""Test the resume analyzer"""

from backend.resume_analyzer import ResumeAnalyzer

# Sample resume text
sample_resume = """
John Doe
Email: john@example.com
Phone: 555-123-4567

Professional Summary:
Experienced Software Engineer with 5 years of experience in web development.
Led team of 5 developers and increased productivity by 30%.

Skills:
- Programming: Python, JavaScript, React, Node.js
- Databases: MySQL, PostgreSQL, MongoDB
- Tools: Git, Docker, Jenkins
- Soft Skills: Leadership, Communication, Problem Solving

Experience:
Senior Developer at Tech Corp (2020-2024)
- Developed scalable web applications using React and Node.js
- Implemented CI/CD pipeline reducing deployment time by 40%
- Managed team of 5 junior developers
- Increased code quality and reduced bugs by 25%

Education:
Bachelor of Computer Science, University Name (2016-2020)
"""

# Test analyzer
print("Testing AI Resume Analyzer...")
print("=" * 50)

analyzer = ResumeAnalyzer()
result = analyzer.analyze(sample_resume)

print("\nAnalysis Results:")
print("-" * 50)
print(f"Overall Score: {result['scores']['overall_score']}%")
print(f"Content Quality: {result['scores']['content_quality']}%")
print(f"Keyword Optimization: {result['scores']['keyword_optimization']}%")
print(f"ATS Compatibility: {result['scores']['ats_compatibility']}%")
print(f"Structure: {result['scores']['structure_score']}%")
print(f"Completeness: {result['scores']['completeness']}%")

print(f"\nTechnical Skills Found: {len(result['technical_skills'])}")
print(f"Technical Skills: {', '.join(result['technical_skills'][:10])}")

print(f"\nSoft Skills Found: {len(result['soft_skills'])}")
print(f"Soft Skills: {', '.join(result['soft_skills'][:5])}")

print(f"\nAction Verbs Count: {result['action_verbs_count']}")
print(f"Word Count: {result['word_count']}")

print(f"\nRecommendations ({len(result['recommendations'])}):")
for i, rec in enumerate(result['recommendations'], 1):
    print(f"{i}. {rec}")

print("\n" + "=" * 50)
print("Test completed successfully!")
