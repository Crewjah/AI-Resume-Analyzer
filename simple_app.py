import streamlit as st
import pandas as pd
import numpy as np
import re
import io
import time
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified CSS for basic styling
def load_css():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .feature-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)

# Simple Resume Analyzer Class
class SimpleResumeAnalyzer:
    def __init__(self):
        self.skills_database = [
            "Python", "Java", "JavaScript", "React", "Angular", "Vue.js",
            "Django", "Flask", "Node.js", "Express", "HTML", "CSS",
            "SQL", "MySQL", "PostgreSQL", "MongoDB", "AWS", "Azure",
            "Docker", "Kubernetes", "Git", "GitHub", "Linux", "Windows"
        ]
    
    def extract_text_from_file(self, uploaded_file):
        """Extract text from uploaded file"""
        try:
            if uploaded_file.type == "text/plain":
                return str(uploaded_file.read(), "utf-8")
            else:
                return uploaded_file.read().decode('utf-8', errors='ignore')
        except:
            return "Error reading file"
    
    def analyze_resume(self, resume_text, job_description=""):
        """Simple resume analysis"""
        
        # Basic metrics
        word_count = len(resume_text.split())
        char_count = len(resume_text)
        
        # Find skills
        found_skills = []
        text_lower = resume_text.lower()
        
        for skill in self.skills_database:
            if skill.lower() in text_lower:
                count = text_lower.count(skill.lower())
                found_skills.append({
                    'name': skill,
                    'count': count,
                    'confidence': min(100, count * 20 + 60)
                })
        
        # Sort by confidence
        found_skills.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Calculate ATS score
        ats_score = min(100, len(found_skills) * 10 + 30)
        
        # Calculate job match if description provided
        match_score = 50  # Default
        if job_description:
            job_words = set(job_description.lower().split())
            resume_words = set(resume_text.lower().split())
            common_words = job_words.intersection(resume_words)
            match_score = min(100, len(common_words) * 2)
        
        # Extract experience years
        exp_pattern = r'(\d+)[\+\s]*(?:years?|yrs?)[\s]*(?:of\s*)?(?:experience|exp)'
        exp_match = re.search(exp_pattern, resume_text, re.IGNORECASE)
        experience_years = int(exp_match.group(1)) if exp_match else 0
        
        return {
            'word_count': word_count,
            'char_count': char_count,
            'skills': found_skills,
            'skill_count': len(found_skills),
            'top_skills': found_skills[:10],
            'ats_score': ats_score,
            'match_score': match_score,
            'experience_years': experience_years,
            'recommendations': self._generate_recommendations(ats_score, len(found_skills), match_score)
        }
    
    def _generate_recommendations(self, ats_score, skill_count, match_score):
        """Generate simple recommendations"""
        recommendations = []
        
        if ats_score < 70:
            recommendations.append({
                'title': 'Improve ATS Compatibility',
                'description': 'Add more relevant keywords and technical skills to improve ATS scanning.',
                'priority': 'High'
            })
        
        if skill_count < 8:
            recommendations.append({
                'title': 'Add More Skills',
                'description': 'Include more technical and soft skills relevant to your target role.',
                'priority': 'Medium'
            })
        
        if match_score < 60:
            recommendations.append({
                'title': 'Better Job Alignment',
                'description': 'Incorporate more keywords from the job description into your resume.',
                'priority': 'High'
            })
        
        return recommendations

def main():
    load_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Resume Analyzer</h1>
        <p>Intelligent Resume Analysis with Machine Learning & NLP</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize analyzer
    analyzer = SimpleResumeAnalyzer()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Settings")
        analysis_type = st.selectbox("Analysis Type", ["Complete Analysis", "Skills Only", "ATS Score Only"])
        industry = st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Marketing"])
        
        st.markdown("### 📊 Features")
        st.markdown("""
        - 🧠 **AI Analysis**
        - 📝 **Skill Detection**
        - 🎯 **ATS Scoring**
        - 📊 **Job Matching**
        - 💡 **Recommendations**
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Upload Your Resume</h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=['txt', 'pdf', 'docx'],
            help="Upload your resume in TXT, PDF, or DOCX format"
        )
        
        st.markdown("""
        <div class="feature-card">
            <h3>💼 Job Description (Optional)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        job_description = st.text_area(
            "Paste job description for matching analysis",
            height=150,
            placeholder="Paste the job description here..."
        )
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>⚡ Status</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if uploaded_file:
            st.success("✅ File uploaded successfully!")
            st.info(f"📁 File: {uploaded_file.name}")
        else:
            st.warning("⏳ Waiting for file upload...")
    
    # Analysis button and results
    if uploaded_file:
        if st.button("🚀 Analyze Resume", use_container_width=True):
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate analysis steps
            steps = [
                ("Extracting text...", 25),
                ("Analyzing skills...", 50),
                ("Calculating scores...", 75),
                ("Generating recommendations...", 100)
            ]
            
            for step, progress in steps:
                status_text.info(f"🔄 {step}")
                progress_bar.progress(progress)
                time.sleep(0.5)
            
            # Extract and analyze
            resume_text = analyzer.extract_text_from_file(uploaded_file)
            results = analyzer.analyze_resume(resume_text, job_description)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            st.success("✅ Analysis Complete!")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h2>{results['ats_score']}</h2>
                    <p>ATS Score</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h2>{results['skill_count']}</h2>
                    <p>Skills Found</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h2>{results['match_score']}%</h2>
                    <p>Job Match</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h2>{results['experience_years']}</h2>
                    <p>Years Exp.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Detailed results in tabs
            tab1, tab2, tab3 = st.tabs(["📈 Overview", "🎯 Skills", "💡 Recommendations"])
            
            with tab1:
                st.markdown("### 📊 Resume Statistics")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Word Count", results['word_count'])
                    st.metric("Character Count", results['char_count'])
                
                with col2:
                    st.metric("Skills Detected", results['skill_count'])
                    st.metric("Experience Years", results['experience_years'])
            
            with tab2:
                st.markdown("### 🛠️ Detected Skills")
                
                if results['top_skills']:
                    for skill in results['top_skills']:
                        confidence_color = "🟢" if skill['confidence'] > 80 else "🟡" if skill['confidence'] > 60 else "🔴"
                        st.write(f"{confidence_color} **{skill['name']}** - {skill['confidence']}% confidence")
                else:
                    st.info("No skills detected. Try uploading a different resume or adding more technical terms.")
            
            with tab3:
                st.markdown("### 💡 Improvement Recommendations")
                
                for i, rec in enumerate(results['recommendations'], 1):
                    priority_icon = {"High": "🔴", "Medium": "🟡", "Low": "🔵"}.get(rec['priority'], "⚪")
                    
                    with st.expander(f"{priority_icon} {rec['title']}", expanded=(rec['priority'] == 'High')):
                        st.write(rec['description'])
                        st.info(f"Priority: {rec['priority']}")

if __name__ == "__main__":
    main()