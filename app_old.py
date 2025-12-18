import streamlit as st
import time
from pathlib import Path
from backend.resume_analyzer import ResumeAnalyzer
from backend.pdf_extractor import extract_text_from_pdf
from backend.keyword_matcher import calculate_match_score
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Educational Platform Theme
st.markdown("""
<style>
    /* Base Layout */
    .main {
        padding: 0 !important;
        background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
        min-height: 100vh;
    }
    
    .block-container {
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding: 2rem 3rem !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    html {scroll-behavior: smooth;}
    
    /* Educational Header */
    .main-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
        padding: 3.5rem 2.5rem;
        border-radius: 24px;
        text-align: center;
        margin: 0 0 2.5rem 0;
        box-shadow: 0 20px 60px rgba(79, 70, 229, 0.25);
        position: relative;
        overflow: hidden;
        animation: headerEntry 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 10%, transparent 60%);
        animation: float 8s ease-in-out infinite;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #f59e0b, #ef4444, #ec4899, #a855f7, #6366f1);
        animation: rainbow 3s linear infinite;
    }
    
    .main-header h1 {
        font-size: 3.2rem;
        font-weight: 800;
        margin: 0;
        color: white;
        position: relative;
        z-index: 1;
        text-shadow: 0 4px 12px rgba(0,0,0,0.2);
        letter-spacing: -0.02em;
        animation: titleSlide 0.6s ease-out;
    }
    
    .main-header p {
        font-size: 1.25rem;
        margin-top: 0.75rem;
        color: rgba(255,255,255,0.95);
        position: relative;
        z-index: 1;
        font-weight: 400;
        animation: subtitleFade 0.8s ease-out 0.2s both;
    }
    
    /* Container Sections */
    .container-section {
        max-width: 1400px;
        margin: 4rem auto;
        padding: 0 2rem;
    }
    
    /* Feature Cards - New Design */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 3rem 2rem;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        border: 3px solid transparent;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 6px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        transform: scaleX(0);
        transition: transform 0.5s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 25px 60px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        animation: bounce 2s ease-in-out infinite;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1f2937;
        margin: 1rem 0;
    }
    
    .feature-desc {
        color: #6b7280;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* Upload Zone - Completely New Design */
    .upload-section {
        background: white;
        padding: 4rem;
        border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        text-align: center;
        margin: 3rem 0;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .section-subtitle {
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
    
    [data-testid="stFileUploader"] {
        border: 4px dashed #667eea !important;
        border-radius: 30px !important;
        padding: 4rem !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(240, 147, 251, 0.05)) !important;
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        position: relative !important;
    }
    
    [data-testid="stFileUploader"]::before {
        content: '📁';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 5rem;
        opacity: 0.1;
        pointer-events: none;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2 !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(240, 147, 251, 0.1)) !important;
        transform: scale(1.02) rotate(1deg) !important;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3) !important;
    }Mega Button - New Design */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1.5rem 4rem !important;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        border-radius: 50px !important;
        cursor: pointer !important;
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        position: relative !important;
        overflow: hidden !important;
        border: 4px solid rgba(255,255,255,0.3) !important;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease;
    }
    
    .stButton>button:hover::before {
        width: 400px;
        height: 400px;
    }
    
    .stButton>button:hover {
        transform: translateY(-8px) scale(1.1) rotate(-2deg) !important;
        box-shadow: 0 25px 70px rgba(102, 126, 234, 0.6) !important;
    }
    
    .stButton>button:active {
        transform: translateY(-4px) scale(1.05
    
    /* Button */
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.875rem 2.5rem !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 24px rgba(79, 70, 229, 0.3), 0 4px 8px rgba(0, 0, 0, 0.1) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 16px 40px rgba(79, 70, 229, 0.4), 0 8px 16px rgba(0, 0, 0, 0.15) !important;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:active {
        transform: translateY(-1px) scale(1.02) !important;
    }
    
    /* Score Containers */
    .score-container {
        background: white;
        border: 3px solid #e5e7eb;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
        transition: all 0.4s ease;
        animation: scoreEntry 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .score-container:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 20px 60px rgba(79, 70, 229, 0.15);
        border-color: #4f46e5;
    }
    
    .score-container h3 {
        color: #4f46e5;
        margin: 0 0 1.5rem 0;
        font-size: 1.4rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .score-value {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #4f46e5, #7c3aed, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
        transition: all 0.4s ease;
        border-left: 5px solid #4f46e5;
        animation: cardSlideIn 0.6s ease-out;
    }
    
    .metric-card:hover {
        border-color: #7c3aed;
        transform: translateY(-5px);
        box-shadow: 0 16px 40px rgba(79, 70, 229, 0.15);
    }
    
    /* Info Boxes - Educational Style */
    .info-box {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 5px solid #3b82f6;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: #1e3a8a;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }
    
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 5px solid #22c55e;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: #065f46;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.15);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
        border-left: 5px solid #f59e0b;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: #92400e;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
    }
    
    .warning-box:hover {
        transform: translateX(8px);
    }
    
    /* Charts */
    [data-testid="stPlotlyChart"] {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
    }
    
    [data-testid="stDataFrame"] {
        background: white !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
    }
    
    /* Text Colors - Dark for Light Background */
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
    }
    
    p, span, label {
        color: #374151 !important;
    }
    
    .stMarkdown h3, .stMarkdown h4 {
        color: #4f46e5 !important;
        font-weight: 700 !important;
    }
    
    /* Progress Bar - Educational Colors */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #ec4899) !important;
    }
    
    /* Success Message - Light Theme */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
        border-left: 5px solid #22c55e !important;
        color: #065f46 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    
    .stAlert {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        border-left: 5px solid #3b82f6 !important;
        color: #1e3a8a !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    
    /* Scrollbar - Educational Theme */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f3f4f6;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #4f46e5, #7c3aed);
        border-radius: 10px;
        border: 2px solid #f3f4f6;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #7c3aed, #ec4899);
    }
    
    /* Educational Animations */
    @keyframes headerEntry {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes cardEntry {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes cardSlideIn {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes scoreEntry {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    @keyframes rainbow {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    @keyframes titleSlide {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes subtitleFade {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    ro Section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🎓 AI Resume Analyzer</h1>
    <p class="hero-subtitle">Transform Your Career with AI-Powered Resume Intelligence</p>
    <div class="hero-badge">✨ Powered by Advanced Machine Learning</div>
</div>
""", unsafe_allow_html=True)

# Stats Bar
st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-number">10K+</div>
        <div class="stat-label">Resumes Analyzed</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">95%</div>
  Upload Section
st.markdown("""
<div class="container-section">
    <div class="upload-section">
        <div class="section-title">📄 Upload Your Resume</div>
        <div class="section-subtitle">Get instant AI-powered analysis in seconds</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
        "Drag & Drop your PDF resume herue)

# Features Section
st.markdown("""
<div class="container-section">
    <div class="section-title" style="text-align:center;">🚀 Why Choose Us?</div>
    <div class="section-subtitle" style="text-align:center;">Cutting-edge AI technology to boost your career prospects</div>
    
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">ATS Optimization</div>
            <div class="feature-desc">Beat applicant tracking systems with optimized keywords and formatting</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Detailed Analytics</div>
            <div class="feature-desc">Get comprehensive insights with visual charts and metrics</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Smart Recommendations</div>
            <div class="feature-desc">Receive personalized suggestions to improve your resume</div>
        </div>
    </div
st.markdown("""
<div class="main-header">
    <h1>AI Resume Analyzer</h1>
    <p>Enhance Your Career with Intelligent Resume Analysis</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'results' not in st.session_state:
    st.session_state.results = None

# Sidebar (minimal)
with st.sidebar:
    pass

# Main content
st.markdown("""
<div class="content-card">
    <h3>Upload Your Resume</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload your resume in PDF format for analysis"
    )

with col2:
    st.markdown("""
    <div class="content-card" style="margin-top: 0;">
        <h3 style="margin-top: 0;">Job Description (Optional)</h3>
    </div>
    """, unsafe_allow_html=True)
    job_description = st.text_area(
        "Paste job description here",
        height=200,
        placeholder="Enter the job description to calculate match score..."
    )

if uploaded_file is not None:
    # Process button
    if st.button("🚀 Analyze Resume", key="analyze_btn", help="Click to analyze your resume"):
        with st.spinner("Analyzing your resume..."):
            # Progress bar
            progress_bar = st.progress(0)
            
            # Extract text from PDF
            progress_bar.progress(20)
            time.sleep(0.3)
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # Initialize analyzer
            progress_bar.progress(40)
            analyzer = ResumeAnalyzer()
            
            # Analyze resume
            progress_bar.progress(60)
            time.sleep(0.3)
            analysis_results = analyzer.analyze(resume_text)
            
            # Calculate job match if description provided
            if job_description:
                progress_bar.progress(80)
                match_score = calculate_match_score(resume_text, job_description)
                analysis_results['match_score'] = match_score
            
            progress_bar.progress(100)
            time.sleep(0.2)
            st.session_state.results = analysis_results
            st.session_state.analyzed = True
            
        st.success("✅ Analysis complete!")

# Display results
if st.session_state.analyzed and st.session_state.results:
    results = st.session_state.results
    
    st.markdown("---")
    st.markdown("## 📈 Analysis Results")
    
    # Overall score
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="score-container">
            <h3>Overall Score</h3>
            <div class="score-value">{results.get('overall_score', 0)}/100</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if 'match_score' in results:
            st.markdown(f"""
            <div class="score-container">
                <h3>Job Match</h3>
                <div class="score-value">{results['match_score']}/100</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Add job description for match score")
    
    with col3:
        ats_score = results.get('ats_score', 0)
        st.markdown(f"""
        <div class="score-container">
            <h3>ATS Score</h3>
            <div class="score-value">{ats_score}/100</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed metrics
    st.markdown("### 📊 Detailed Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Skills found
        st.markdown("#### 🎯 Skills Identified")
        skills = results.get('skills', [])
        if skills:
            skills_df = {
                'Skill': skills[:10],
                'Category': ['Technical' if i % 2 == 0 else 'Soft' for i in range(len(skills[:10]))]
            }
            st.dataframe(skills_df, use_container_width=True)
        else:
            st.warning("No skills identified. Consider adding more specific skills.")
    
    with col2:
        # Keyword density chart
        st.markdown("#### 📌 Top Keywords")
        keywords = results.get('keywords', {})
        if keywords:
            fig = px.bar(
                x=list(keywords.keys())[:10],
                y=list(keywords.values())[:10],
                labels={'x': 'Keyword', 'y': 'Frequency'},
                color=list(keywords.values())[:10],
                color_continuous_scale=[[0, '#4f46e5'], [0.5, '#7c3aed'], [1, '#ec4899']]
            )
            fig.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=0, r=0, t=30, b=0),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#1f2937', size=12, family='Arial, sans-serif'),
                xaxis=dict(
                    showgrid=False, 
                    color='#6b7280',
                    tickangle=-45
                ),
                yaxis=dict(
                    showgrid=True, 
                    gridcolor='#e5e7eb', 
                    color='#6b7280'
                )
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    recommendations = results.get('recommendations', [])
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="warning-box">
                <strong>{i}.</strong> {rec}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
            Great job! Your resume looks well-optimized.
        </div>
        """, unsafe_allow_html=True)
    
    # Score breakdown chart
    st.markdown("### 📉 Score Breakdown")
    
    categories = ['Content Quality', 'Keyword Optimization', 'ATS Compatibility', 'Structure', 'Completeness']
    scores = [
        results.get('content_score', 75),
        results.get('keyword_score', 80),
        results.get('ats_score', 70),
        results.get('structure_score', 85),
        results.get('completeness_score', 90)
    ]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        line=dict(color='#4f46e5', width=3),
        fillcolor='rgba(79, 70, 229, 0.3)',
        marker=dict(size=8, color='#ec4899')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='#e5e7eb',
                tickcolor='#6b7280',
                tickfont=dict(size=12, color='#374151')
            ),
            angularaxis=dict(
                gridcolor='#e5e7eb',
                tickcolor='#374151',
                tickfont=dict(size=12, color='#374151', weight='bold')
            ),
            bgcolor='white'
        ),
        showlegend=False,
        height=450,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1f2937', family='Arial, sans-serif')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
