import streamlit as st
import pandas as pd
import numpy as np
import io
import time
import re
from datetime import datetime

# Try to import optional dependencies
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not available. Some visualizations will be simplified.")

# Import custom modules with error handling
try:
    from resume_analyzer import ResumeAnalyzer
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False
    st.error("❌ Resume analyzer module not found. Using simplified analyzer.")

try:
    from ui_components import (create_animated_metric, create_skill_radar_chart, create_compatibility_gauge, 
                               create_skills_treemap, create_keyword_comparison_chart, create_progress_chart,
                               create_skill_proficiency_chart, create_sentiment_gauge, create_word_cloud_chart)
    UI_COMPONENTS_AVAILABLE = True
except ImportError:
    UI_COMPONENTS_AVAILABLE = False

# Configure page
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        animation: slideInDown 0.8s ease-out;
    }
    
    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        text-align: center;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Card Styles */
    .feature-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        margin: 1rem 0;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    /* Upload Area */
    .upload-area {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        border: 2px dashed rgba(255,255,255,0.5);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
    }
    
    .upload-area:hover {
        background: linear-gradient(135deg, #ff9a9e 0%, #f093fb 100%);
        transform: scale(1.02);
    }
    
    /* Progress Bar */
    .progress-container {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        height: 20px;
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
        animation: shimmer 1.5s infinite;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        animation: bounceIn 0.8s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Animations */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(255, 154, 158, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(255, 154, 158, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(255, 154, 158, 0);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -200% 0;
        }
        100% {
            background-position: 200% 0;
        }
    }
    
    /* Sidebar Styles */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Custom Selectbox */
    .stSelectbox > div > div {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        .feature-card {
            margin: 0.5rem 0;
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_css()
    
    # Header Section
    st.markdown("""
    <div class="main-header">
        <h1 class="header-title">🤖 AI Resume Analyzer</h1>
        <p class="header-subtitle">Intelligent Resume Analysis with Machine Learning & NLP</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = ""
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Analysis Settings")
        
        analysis_type = st.selectbox(
            "Choose Analysis Type",
            ["Complete Analysis", "Skill Analysis Only", "ATS Score Only", "Job Matching"]
        )
        
        st.markdown("### 📊 Analysis Depth")
        depth = st.slider("Analysis Depth", 1, 5, 3)
        
        st.markdown("### 🎯 Industry Focus")
        industry = st.selectbox(
            "Target Industry",
            ["Technology", "Finance", "Healthcare", "Marketing", "Education", "Other"]
        )
        
        st.markdown("---")
        st.markdown("### 📈 Features")
        st.markdown("""
        - 🧠 **AI-Powered Analysis**
        - 📝 **Skill Extraction**
        - 🎯 **ATS Optimization**
        - 📊 **Job Compatibility**
        - 💡 **Improvement Suggestions**
        """)
    
    # Main Content Area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File Upload Section
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Upload Your Resume</h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'docx', 'txt'],
            help="Upload your resume in PDF, DOCX, or TXT format"
        )
        
        # Job Description Input
        st.markdown("""
        <div class="feature-card">
            <h3>💼 Job Description (Optional)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        job_description = st.text_area(
            "Paste the job description here for better matching analysis",
            height=150,
            placeholder="Paste the job description you want to match your resume against..."
        )
    
    with col2:
        # Quick Stats/Preview
        st.markdown("""
        <div class="feature-card">
            <h3>⚡ Quick Stats</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if uploaded_file:
            file_size = len(uploaded_file.getvalue()) / 1024  # KB
            st.metric("File Size", f"{file_size:.1f} KB")
            st.metric("File Type", uploaded_file.type)
            st.metric("Status", "Ready for Analysis", delta="✅")
        else:
            st.info("Upload a resume to see file statistics")
    
    # Analysis Button
    if uploaded_file:
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_center = st.columns([1, 2, 1])[1]
        with col_center:
            if st.button("🚀 Analyze Resume", use_container_width=True):
                analyze_resume(uploaded_file, job_description, analysis_type, depth, industry)
    
    # Display Results
    if st.session_state.analysis_complete:
        display_analysis_results()

def analyze_resume(uploaded_file, job_description, analysis_type, depth, industry):
    """Perform resume analysis with animated progress"""
    
    # Progress animation
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    with progress_placeholder.container():
        st.markdown("""
        <div class="feature-card">
            <h3>🔄 Analysis in Progress...</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Simulate analysis steps with progress
    steps = [
        ("Parsing resume content...", 20),
        ("Extracting skills and keywords...", 40),
        ("Analyzing ATS compatibility...", 60),
        ("Calculating job match score...", 80),
        ("Generating recommendations...", 100)
    ]
    
    progress_bar = st.progress(0)
    
    for step, progress in steps:
        status_placeholder.info(f"🔄 {step}")
        progress_bar.progress(progress)
        time.sleep(0.8)  # Simulate processing time
    
    # Initialize analyzer with fallback
    if ANALYZER_AVAILABLE:
        analyzer = ResumeAnalyzer()
    else:
        # Fallback simple analyzer
        class SimpleAnalyzer:
            def __init__(self):
                self.skills_database = [
                    "Python", "Java", "JavaScript", "React", "Angular", "Vue.js",
                    "Django", "Flask", "Node.js", "Express", "HTML", "CSS", "SQL",
                    "MySQL", "PostgreSQL", "MongoDB", "AWS", "Azure", "Docker", "Git"
                ]
            
            def extract_text_from_file(self, uploaded_file):
                try:
                    if uploaded_file.type == "text/plain":
                        return str(uploaded_file.read(), "utf-8")
                    else:
                        return uploaded_file.read().decode('utf-8', errors='ignore')
                except:
                    return "Error reading file"
            
            def analyze_resume(self, resume_text, job_description="", analysis_type="Complete Analysis", depth=3, industry="Technology"):
                word_count = len(resume_text.split())
                found_skills = []
                text_lower = resume_text.lower()
                
                for skill in self.skills_database:
                    if skill.lower() in text_lower:
                        count = text_lower.count(skill.lower())
                        found_skills.append({
                            'name': skill,
                            'count': count,
                            'confidence': min(100, count * 20 + 60),
                            'category': 'Technical'
                        })
                
                found_skills.sort(key=lambda x: x['confidence'], reverse=True)
                ats_score = min(100, len(found_skills) * 10 + 30)
                match_score = 50 if not job_description else min(100, len(set(job_description.lower().split()) & set(resume_text.lower().split())) * 2)
                
                exp_pattern = r'(\d+)[\+\s]*(?:years?|yrs?)[\s]*(?:of\s*)?(?:experience|exp)'
                exp_match = re.search(exp_pattern, resume_text, re.IGNORECASE)
                experience_years = int(exp_match.group(1)) if exp_match else 0
                
                return {
                    'word_count': word_count,
                    'skills': found_skills,
                    'skill_count': len(found_skills),
                    'top_skills': found_skills[:10],
                    'ats_score': ats_score,
                    'match_score': match_score,
                    'experience_years': experience_years,
                    'sections': ['Experience', 'Education', 'Skills'],
                    'education_level': 'Bachelor',
                    'skill_categories': {'Technical': len(found_skills)},
                    'recommendations': [
                        {'title': 'Add More Skills', 'description': 'Include more technical skills relevant to your field.', 'priority': 'Medium'},
                        {'title': 'Improve ATS Score', 'description': 'Add more industry keywords to improve ATS compatibility.', 'priority': 'High'}
                    ]
                }
        
        analyzer = SimpleAnalyzer()
    
    # Process the uploaded file
    resume_text = analyzer.extract_text_from_file(uploaded_file)
    
    # Perform analysis
    results = analyzer.analyze_resume(
        resume_text, 
        job_description, 
        analysis_type, 
        depth, 
        industry
    )
    
    # Store results in session state
    st.session_state.analysis_results = results
    st.session_state.analysis_complete = True
    
    # Clear progress indicators
    progress_placeholder.empty()
    status_placeholder.empty()
    
    # Success message
    st.success("✅ Analysis Complete! Scroll down to see results.")

def display_analysis_results():
    """Display comprehensive analysis results with beautiful visualizations"""
    
    if 'analysis_results' not in st.session_state:
        return
    
    results = st.session_state.analysis_results
    
    st.markdown("""
    <div class="main-header">
        <h2 class="header-title">📊 Analysis Results</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['ats_score']}</div>
            <div class="metric-label">ATS Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['skill_count']}</div>
            <div class="metric-label">Skills Found</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['match_score']}%</div>
            <div class="metric-label">Job Match</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['experience_years']}</div>
            <div class="metric-label">Years Exp.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Analysis Sections
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🎯 Skills Analysis", "📊 Job Matching", "💡 Recommendations"])
    
    with tab1:
        display_overview_tab(results)
    
    with tab2:
        display_skills_tab(results)
    
    with tab3:
        display_matching_tab(results)
    
    with tab4:
        display_recommendations_tab(results)

def display_overview_tab(results):
    """Display overview analysis"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # ATS Compatibility Gauge
        if UI_COMPONENTS_AVAILABLE and PLOTLY_AVAILABLE:
            fig = create_compatibility_gauge(results['ats_score'], "ATS Compatibility Score")
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Simple progress bar fallback
            st.markdown("### 🎯 ATS Compatibility Score")
            st.progress(results['ats_score'] / 100)
            st.metric("ATS Score", f"{results['ats_score']}/100")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>📋 Resume Summary</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"**Total Words:** {results.get('word_count', 'N/A')}")
        st.write(f"**Sections Found:** {len(results.get('sections', []))}")
        st.write(f"**Education Level:** {results.get('education_level', 'Not specified')}")
        st.write(f"**Industry Match:** {results.get('industry_match', 'N/A')}")

def display_skills_tab(results):
    """Display skills analysis"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Skills Radar Chart
        if results.get('skills'):
            fig = create_skill_radar_chart(results['skills'])
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🛠️ Top Skills</h4>
        </div>
        """, unsafe_allow_html=True)
        
        for skill in results.get('top_skills', [])[:10]:
            st.write(f"• **{skill['name']}** - {skill['confidence']}% match")

def display_matching_tab(results):
    """Display job matching analysis"""
    
    if results.get('job_analysis'):
        col1, col2 = st.columns(2)
        
        with col1:
            # Matching Keywords
            st.markdown("""
            <div class="feature-card">
                <h4>✅ Matching Keywords</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for keyword in results['job_analysis'].get('matching_keywords', [])[:10]:
                st.success(f"✓ {keyword}")
        
        with col2:
            # Missing Keywords
            st.markdown("""
            <div class="feature-card">
                <h4>❌ Missing Keywords</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for keyword in results['job_analysis'].get('missing_keywords', [])[:10]:
                st.error(f"✗ {keyword}")

def display_recommendations_tab(results):
    """Display improvement recommendations"""
    
    st.markdown("""
    <div class="feature-card">
        <h4>💡 Improvement Recommendations</h4>
    </div>
    """, unsafe_allow_html=True)
    
    recommendations = results.get('recommendations', [])
    
    for i, rec in enumerate(recommendations, 1):
        with st.expander(f"📌 Recommendation {i}: {rec.get('title', 'Improvement Suggestion')}"):
            st.write(rec.get('description', ''))
            if rec.get('priority'):
                st.info(f"Priority: {rec['priority']}")

if __name__ == "__main__":
    main()