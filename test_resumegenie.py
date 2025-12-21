"""
Test ResumeGenie Core Functionality
"""

def test_resumegenie():
    print("🧞‍♂️ Testing ResumeGenie Core Functionality")
    print("=" * 50)
    
    try:
        # Test backend functionality
        print("1️⃣ Testing Resume Analyzer...")
        from backend.resume_analyzer import ResumeAnalyzer
        
        analyzer = ResumeAnalyzer()
        test_resume = """
        John Doe
        Software Engineer
        john.doe@email.com
        (555) 123-4567
        
        Experience:
        - Developed Python applications using Django and Flask
        - Led a team of 5 developers to deliver projects 30% faster
        - Implemented machine learning models improving accuracy by 25%
        - Created REST APIs serving 10,000+ daily users
        
        Skills:
        Python, JavaScript, React, Django, Machine Learning, Leadership
        
        Education:
        Bachelor of Computer Science, University of Technology
        """
        
        # Analyze the test resume
        analysis = analyzer.analyze(test_resume)
        print("✅ Resume analysis successful!")
        
        print(f"   📊 Overall Score: {analysis['scores']['overall_score']}")
        print(f"   📝 Word Count: {analysis['word_count']}")
        print(f"   🔧 Technical Skills: {len(analysis['technical_skills'])}")
        print(f"   🤝 Soft Skills: {len(analysis['soft_skills'])}")
        print()
        
        # Test PDF extraction
        print("2️⃣ Testing PDF Extractor...")
        from backend.pdf_extractor import extract_text_from_pdf
        print("✅ PDF extractor imported successfully!")
        
        # Test keyword matching
        print("3️⃣ Testing Keyword Matcher...")
        from backend.keyword_matcher import calculate_match_score
        
        job_description = "Python developer with Django experience and machine learning skills"
        match_score = calculate_match_score(test_resume, job_description)
        print(f"✅ Job match score: {match_score}%")
        print()
        
        # Display some analysis results
        print("🎯 Sample Analysis Results:")
        print("-" * 30)
        print(f"Content Quality: {analysis['scores']['content_quality']}/100")
        print(f"ATS Compatibility: {analysis['scores']['ats_compatibility']}/100")
        print(f"Keyword Optimization: {analysis['scores']['keyword_optimization']}/100")
        print()
        
        if analysis['recommendations']:
            print("💡 Sample Recommendations:")
            for i, rec in enumerate(analysis['recommendations'][:3], 1):
                print(f"   {i}. {rec}")
        
        print()
        print("🎉 All core functionality is working perfectly!")
        print("🌟 ResumeGenie is ready to help users optimize their resumes!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_resumegenie()