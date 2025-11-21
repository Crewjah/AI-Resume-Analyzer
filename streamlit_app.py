import streamlit as st
import pandas as pd
import numpy as np
import re
import io
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Clean CSS without excessive animations
def load_css():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .info-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .score-good { color: #059669; }
    .score-medium { color: #d97706; }
    .score-poor { color: #dc2626; }
    </style>
    """, unsafe_allow_html=True)

class ResumeAnalyzer:
    def __init__(self):
        self.skills_database = [
            # Programming Languages
            "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "PHP", "Ruby", "Go", "Swift",
            # Web Technologies
            "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask",
            # Databases
            "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite",
            # Cloud & DevOps
            "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "Git", "GitHub",
            # Data Science
            "Machine Learning", "Data Analysis", "Pandas", "NumPy", "TensorFlow", "PyTorch",
            # Other Skills
            "Linux", "REST API", "GraphQL", "Microservices", "Agile", "Scrum"
        ]
    
    def extract_text_from_file(self, uploaded_file):
        try:
            if uploaded_file.type == "text/plain":
                return str(uploaded_file.read(), "utf-8")
            elif uploaded_file.type == "application/pdf":
                # For PDF support, you'd need PyPDF2 or similar
                return "PDF parsing requires additional setup. Please use TXT files for now."
            else:
                return uploaded_file.read().decode('utf-8', errors='ignore')
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def analyze_resume(self, resume_text, job_description=""):
        # Basic analysis
        words = resume_text.split()
        word_count = len(words)
        
        # Find skills
        found_skills = []
        text_lower = resume_text.lower()
        
        for skill in self.skills_database:
            if skill.lower() in text_lower:
                count = text_lower.count(skill.lower())
                found_skills.append({
                    'name': skill,
                    'count': count
                })
        
        # Sort by frequency
        found_skills.sort(key=lambda x: x['count'], reverse=True)
        
        # Calculate scores
        ats_score = min(100, len(found_skills) * 8 + 20)
        
        # Job matching
        match_score = 0
        matching_keywords = []
        missing_keywords = []
        
        if job_description:
            job_words = set(job_description.lower().split())
            resume_words = set(resume_text.lower().split())
            common_words = job_words.intersection(resume_words)
            match_score = min(100, len(common_words) * 3)
            
            # Find relevant keywords
            for word in job_words:
                if len(word) > 3 and word.isalpha():
                    if word in resume_words:
                        matching_keywords.append(word)
                    else:
                        missing_keywords.append(word)
        
        # Extract experience
        exp_pattern = r'(\d+)[\+\s]*(?:years?|yrs?)[\s]*(?:of\s*)?(?:experience|exp)'
        exp_match = re.search(exp_pattern, resume_text, re.IGNORECASE)
        experience_years = int(exp_match.group(1)) if exp_match else 0
        
        # Generate recommendations
        recommendations = []
        if ats_score < 60:
            recommendations.append("Add more relevant technical skills to improve ATS compatibility")
        if len(found_skills) < 8:
            recommendations.append("Include more specific skills related to your field")
        if job_description and match_score < 50:
            recommendations.append("Incorporate more keywords from the job description")
        if word_count < 200:
            recommendations.append("Expand your resume with more detailed descriptions")
        
        return {
            'word_count': word_count,
            'skills': found_skills[:15],  # Top 15 skills
            'skill_count': len(found_skills),
            'ats_score': ats_score,
            'match_score': match_score,
            'experience_years': experience_years,
            'matching_keywords': matching_keywords[:10],
            'missing_keywords': missing_keywords[:10],
            'recommendations': recommendations
        }

def main():
    load_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>AI Resume Analyzer</h1>
        <p>Professional resume analysis and optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize analyzer
    analyzer = ResumeAnalyzer()
    
    # Main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=['txt', 'pdf', 'docx'],
            help="Supported formats: TXT, PDF, DOCX"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("Job Description (Optional)")
        job_description = st.text_area(
            "Paste job description for better matching",
            height=150,
            placeholder="Paste the job description here..."
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("Analysis Features")
        st.write("• Skills Detection")
        st.write("• ATS Score Calculation")
        st.write("• Job Matching Analysis")
        st.write("• Professional Recommendations")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis
    if uploaded_file:
        if st.button("Analyze Resume", type="primary"):
            with st.spinner("Analyzing resume..."):
                resume_text = analyzer.extract_text_from_file(uploaded_file)
                results = analyzer.analyze_resume(resume_text, job_description)
            
            st.success("Analysis completed!")
            
            # Results
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                score_class = "score-good" if results['ats_score'] >= 70 else "score-medium" if results['ats_score'] >= 50 else "score-poor"
                st.markdown(f'<div class="metric-card"><h3 class="{score_class}">{results["ats_score"]}</h3><p>ATS Score</p></div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div class="metric-card"><h3>{results["skill_count"]}</h3><p>Skills Found</p></div>', unsafe_allow_html=True)
            
            with col3:
                if results['match_score'] > 0:
                    match_class = "score-good" if results['match_score'] >= 70 else "score-medium" if results['match_score'] >= 50 else "score-poor"
                    st.markdown(f'<div class="metric-card"><h3 class="{match_class}">{results["match_score"]}%</h3><p>Job Match</p></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="metric-card"><h3>-</h3><p>Job Match</p></div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown(f'<div class="metric-card"><h3>{results["experience_years"]}</h3><p>Years Experience</p></div>', unsafe_allow_html=True)
            
            # Detailed results
            tab1, tab2, tab3 = st.tabs(["Skills Analysis", "Job Matching", "Recommendations"])
            
            with tab1:
                st.subheader("Detected Skills")
                if results['skills']:
                    df = pd.DataFrame(results['skills'])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No specific skills detected. Consider adding more technical terms.")
            
            with tab2:
                if job_description:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Matching Keywords")
                        if results['matching_keywords']:
                            for keyword in results['matching_keywords']:
                                st.write(f"✓ {keyword}")
                        else:
                            st.info("No matching keywords found")
                    
                    with col2:
                        st.subheader("Missing Keywords")
                        if results['missing_keywords']:
                            for keyword in results['missing_keywords'][:5]:
                                st.write(f"• {keyword}")
                        else:
                            st.success("Good keyword coverage!")
                else:
                    st.info("Add a job description to see matching analysis")
            
            with tab3:
                st.subheader("Improvement Suggestions")
                if results['recommendations']:
                    for i, rec in enumerate(results['recommendations'], 1):
                        st.write(f"{i}. {rec}")
                else:
                    st.success("Your resume looks good! No major improvements needed.")

if __name__ == "__main__":
    main()