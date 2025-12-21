#!/usr/bin/env python3
"""Test the new modern app"""

import subprocess
import sys
import time

def main():
    """Test the modern resume analyzer"""
    try:
        print("🚀 Testing Modern AI Resume Analyzer...")
        
        # Import test
        from backend.resume_analyzer import ResumeAnalyzer
        print("✅ Backend imported successfully")
        
        # Test analyzer
        analyzer = ResumeAnalyzer()
        sample_text = """
        John Smith
        Software Engineer  
        john.smith@email.com
        (555) 123-4567
        
        EXPERIENCE
        Senior Developer at TechCorp (2020-2023)
        - Developed React applications with 50% performance improvement
        - Led team of 8 developers on $3M project
        - Implemented CI/CD pipeline reducing deployment time by 40%
        
        EDUCATION
        BS Computer Science, MIT (2018)
        
        SKILLS
        Python, React, AWS, Docker, Kubernetes, Leadership, Agile
        """
        
        print("🧪 Testing resume analysis...")
        result = analyzer.analyze(sample_text)
        
        if result and 'scores' in result:
            scores = result['scores']
            print("✅ Analysis working!")
            print(f"Overall Score: {scores.get('overall_score', 0)}/100")
            print(f"Content: {scores.get('content_quality', 0)}/100")
            print(f"Keywords: {scores.get('keyword_optimization', 0)}/100")
            print(f"ATS: {scores.get('ats_compatibility', 0)}/100")
            print(f"Structure: {scores.get('structure_score', 0)}/100")
            print(f"Completeness: {scores.get('completeness', 0)}/100")
            print(f"Skills Found: {len(result.get('technical_skills', [])) + len(result.get('soft_skills', []))}")
            print("\n🎉 Ready to start the modern app!")
            
            # Start Streamlit
            print("🚀 Starting Streamlit...")
            cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8507"]
            process = subprocess.Popen(cmd)
            print("✅ Application started! Check http://localhost:8507")
            return process
            
        else:
            print("❌ Analysis failed")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    process = main()
    if process:
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
            process.terminate()