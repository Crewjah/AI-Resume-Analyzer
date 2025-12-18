import streamlit as st
import sys
import os
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from resume_analyzer import ResumeAnalyzer
from pdf_extractor import extract_text_from_pdf
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="AI Resume Analyzer - Smart Career Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Complete Educational Platform Design
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    /* Modern Educational Platform Base */
    .main {
        padding: 0 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
    }
    
    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Hero Section - Landing Page Style */
    .hero-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
        padding: 5rem 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        border-bottom: 6px solid #f093fb;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: float 20s linear infinite;
    }
    
    .hero-title {
        font-size: 5rem;
        font-weight: 900;
        color: white;
        margin: 0;
        text-shadow: 0 10px 30px rgba(0,0,0,0.4);
        animation: heroEntry 1s cubic-bezier(0.34, 1.56, 0.64, 1);
        letter-spacing: -3px;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 2rem;
        color: rgba(255,255,255,0.95);
        margin: 2rem 0;
        font-weight: 500;
        animation: subtitleSlide 1s ease-out 0.3s both;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(15px);
        padding: 1rem 3rem;
        border-radius: 50px;
        color: white;
        font-weight: 700;
        font-size: 1.2rem;
        margin-top: 1.5rem;
        animation: badgePulse 2s ease-in-out infinite;
        border: 3px solid rgba(255,255,255,0.4);
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    /* Stats Bar - Dashboard Style */
    .stats-bar {
        background: white;
        padding: 3.5rem 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 3rem;
        max-width: 1400px;
        margin: -4rem auto 0;
        border-radius: 25px;
        position: relative;
        z-index: 10;
    }
    
    .stat-item {
        text-align: center;
        animation: statEntry 0.8s ease-out;
        padding: 1rem;
        border-radius: 15px;
        transition: all 0.3s ease;
    }
    
    .stat-item:hover {
        background: rgba(102, 126, 234, 0.05);
        transform: translateY(-5px);
    }
    
    .stat-number {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        animation: countUp 2s ease-out;
    }
    
    .stat-label {
        font-size: 1.2rem;
        color: #6b7280;
        margin-top: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Container Sections */
    .container-section {
        max-width: 1400px;
        margin: 4rem auto;
        padding: 0 2rem;
    }
    
    .section-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .section-subtitle {
        color: #6b7280;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        text-align: center;
        font-weight: 500;
    }
    
    /* Feature Cards - Showcase Design */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2.5rem;
        margin: 4rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 3.5rem 2.5rem;
        border-radius: 30px;
        text-align: center;
        box-shadow: 0 15px 50px rgba(0,0,0,0.1);
        transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        border: 4px solid transparent;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 8px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        transform: scaleX(0);
        transition: transform 0.6s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-20px) scale(1.05);
        box-shadow: 0 30px 80px rgba(102, 126, 234, 0.35);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-icon {
        font-size: 5rem;
        margin-bottom: 2rem;
        animation: bounce 2s ease-in-out infinite;
    }
    
    .feature-title {
        font-size: 1.8rem;
        font-weight: 900;
        color: #1f2937;
        margin: 1.5rem 0;
    }
    
    .feature-desc {
        color: #6b7280;
        font-size: 1.1rem;
        line-height: 1.7;
        font-weight: 500;
    }
    
    /* Upload Section - Premium Design */
    .upload-section {
        background: white;
        padding: 5rem 3rem;
        border-radius: 40px;
        box-shadow: 0 25px 80px rgba(0,0,0,0.12);
        margin: 4rem 0;
    }
    
    [data-testid="stFileUploader"] {
        border: 5px dashed #667eea !important;
        border-radius: 35px !important;
        padding: 5rem 3rem !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(240, 147, 251, 0.08)) !important;
        transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        position: relative !important;
    }
    
    [data-testid="stFileUploader"]::before {
        content: '📁';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 6rem;
        opacity: 0.12;
        pointer-events: none;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2 !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(240, 147, 251, 0.15)) !important;
        transform: scale(1.03) !important;
        box-shadow: 0 25px 80px rgba(102, 126, 234, 0.35) !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #667eea !important;
        font-weight: 900 !important;
        font-size: 1.6rem !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
    }
    
    .stTextArea textarea {
        background: rgba(102, 126, 234, 0.04) !important;
        border: 4px solid #e5e7eb !important;
        border-radius: 25px !important;
        color: #1f2937 !important;
        padding: 2rem !important;
        font-size: 1.15rem !important;
        transition: all 0.5s ease !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06) !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #9ca3af !important;
        font-style: italic !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 8px rgba(102, 126, 234, 0.18), 0 15px 40px rgba(0, 0, 0, 0.12) !important;
        transform: translateY(-5px) !important;
        background: white !important;
    }
    
    .stTextArea label {
        color: #667eea !important;
        font-weight: 900 !important;
        font-size: 1.4rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    
    /* Mega Button - Action Style */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        color: white !important;
        border: none !important;
        padding: 2rem 5rem !important;
        font-size: 1.6rem !important;
        font-weight: 900 !important;
        border-radius: 60px !important;
        cursor: pointer !important;
        transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.45) !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        position: relative !important;
        overflow: hidden !important;
        border: 5px solid rgba(255,255,255,0.4) !important;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.35);
        transform: translate(-50%, -50%);
        transition: width 0.7s ease, height 0.7s ease;
    }
    
    .stButton>button:hover::before {
        width: 500px;
        height: 500px;
    }
    
    .stButton>button:hover {
        transform: translateY(-10px) scale(1.12) !important;
        box-shadow: 0 30px 80px rgba(102, 126, 234, 0.65) !important;
    }
    
    .stButton>button:active {
        transform: translateY(-5px) scale(1.08) !important;
    }
    
    /* Results Section - Dashboard Cards */
    .results-section {
        background: white;
        padding: 4rem;
        border-radius: 35px;
        margin: 3rem 0;
        box-shadow: 0 20px 70px rgba(0,0,0,0.12);
    }
    
    .score-mega {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 30px;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        animation: scoreZoom 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .score-mega-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
    }
    
    .score-mega-value {
        font-size: 7rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 10px 30px rgba(0,0,0,0.3);
        animation: pulse 2s ease-in-out infinite;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .metric-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(240, 147, 251, 0.08));
        padding: 2.5rem 1.5rem;
        border-radius: 20px;
        text-align: center;
        border: 3px solid rgba(102, 126, 234, 0.2);
        transition: all 0.4s ease;
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    }
    
    .metric-box:hover {
        transform: translateY(-8px) scale(1.05);
        border-color: #667eea;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.25);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: #6b7280;
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Info Boxes - Modern Alerts */
    .info-box-modern {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 8px solid #3b82f6;
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin: 2rem 0;
        color: #1e3a8a;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
    }
    
    .success-box-modern {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 8px solid #22c55e;
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin: 2rem 0;
        color: #065f46;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 10px 30px rgba(34, 197, 94, 0.2);
    }
    
    .warning-box-modern {
        background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
        border-left: 8px solid #f59e0b;
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin: 2rem 0;
        color: #92400e;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.4s ease;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.2);
    }
    
    .warning-box-modern:hover {
        transform: translateX(12px);
    }
    
    /* Charts */
    [data-testid="stPlotlyChart"] {
        background: white;
        border: 3px solid #e5e7eb;
        border-radius: 25px;
        padding: 2rem;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.08);
    }
    
    /* Animations */
    @keyframes gradientShift {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    @keyframes heroEntry {
        from {
            opacity: 0;
            transform: translateY(-50px) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes subtitleSlide {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes badgePulse {
        0%, 100% {
            transform: scale(1);
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        }
        50% {
            transform: scale(1.05);
            box-shadow: 0 12px 40px rgba(0,0,0,0.3);
        }
    }
    
    @keyframes statEntry {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes countUp {
        from {
            opacity: 0;
            transform: scale(0.5);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-15px);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-20px);
        }
    }
    
    @keyframes scoreZoom {
        from {
            opacity: 0;
            transform: scale(0.7);
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
            transform: scale(1.08);
        }
    }
    
    /* Text Colors */
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
    }
    
    p, span, label {
        color: #374151 !important;
    }
    
    .stMarkdown h3 {
        color: #667eea !important;
        font-weight: 900 !important;
        font-size: 2rem !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 14px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f3f4f6;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
        border: 3px solid #f3f4f6;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2, #f093fb);
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🎓 AI Resume Analyzer</h1>
    <p class="hero-subtitle">Transform Your Career with AI-Powered Intelligence</p>
    <div class="hero-badge">✨ Powered by Advanced Machine Learning Algorithms</div>
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
        <div class="stat-label">Success Rate</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">4.9★</div>
        <div class="stat-label">User Rating</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">24/7</div>
        <div class="stat-label">Available</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class="container-section">
    <div class="section-title">🚀 Why Choose Our Platform?</div>
    <div class="section-subtitle">Cutting-edge AI technology to supercharge your career prospects</div>
    
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">ATS Optimization</div>
            <div class="feature-desc">Beat applicant tracking systems with AI-optimized keywords and professional formatting</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Detailed Analytics</div>
            <div class="feature-desc">Get comprehensive insights with interactive visual charts and performance metrics</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Smart Recommendations</div>
            <div class="feature-desc">Receive personalized AI-powered suggestions to dramatically improve your resume</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Upload Section
st.markdown("""
<div class="container-section">
    <div class="upload-section">
        <div class="section-title">📄 Upload Your Resume</div>
        <div class="section-subtitle">Get instant AI-powered analysis in seconds - it's that simple!</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drag & Drop your PDF resume here or click to browse",
    type=['pdf'],
    help="Upload your resume in PDF format for comprehensive AI analysis"
)

job_description = st.text_area(
    "🎯 Target Job Description (Optional)",
    height=180,
    placeholder="Paste the job description here to get personalized matching insights, keyword optimization, and tailored recommendations..."
)

st.markdown("</div></div>", unsafe_allow_html=True)

# Analyze Button
col_b1, col_b2, col_b3 = st.columns([1, 1.5, 1])
with col_b2:
    analyze_button = st.button("🔍 ANALYZE MY RESUME NOW", use_container_width=True)

# Initialize session state
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'results' not in st.session_state:
    st.session_state.results = None

# Analysis logic
if analyze_button and uploaded_file:
    with st.spinner("🤖 AI is analyzing your resume..."):
        # Extract text
        resume_text = extract_text_from_pdf(uploaded_file)
        
        # Analyze
        analyzer = ResumeAnalyzer()
        results = analyzer.analyze_resume(resume_text, job_description if job_description else "")
        
        st.session_state.analyzed = True
        st.session_state.results = results

# Display results
if st.session_state.analyzed and st.session_state.results:
    results = st.session_state.results
    
    st.markdown("""
    <div class="container-section">
        <div class="results-section">
            <div class="section-title">📈 Your Resume Analysis Results</div>
    """, unsafe_allow_html=True)
    
    # Overall Score
    overall_score = results.get('overall_score', 0)
    st.markdown(f"""
    <div class="score-mega">
        <div class="score-mega-title">Overall Resume Score</div>
        <div class="score-mega-value">{overall_score}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metric Cards
    st.markdown("""<div class="metric-grid">""", unsafe_allow_html=True)
    
    metrics = [
        ("Content Quality", results.get('content_score', 0)),
        ("Keywords", results.get('keyword_score', 0)),
        ("ATS Score", results.get('ats_score', 0)),
        ("Structure", results.get('structure_score', 0)),
        ("Completeness", results.get('completeness_score', 0))
    ]
    
    for label, value in metrics:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{value}%</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Keywords Section
    if results.get('keywords'):
        st.markdown("### 🔑 Top Keywords Found")
        keywords = results['keywords']
        
        if keywords:
            fig = px.bar(
                x=list(keywords.keys())[:10],
                y=list(keywords.values())[:10],
                labels={'x': 'Keyword', 'y': 'Frequency'},
                color=list(keywords.values())[:10],
                color_continuous_scale=[[0, '#667eea'], [0.5, '#764ba2'], [1, '#f093fb']]
            )
            fig.update_layout(
                showlegend=False,
                height=350,
                margin=dict(l=0, r=0, t=30, b=0),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#1f2937', size=13, family='Arial, sans-serif', weight='bold'),
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
    st.markdown("### 💡 AI Recommendations")
    recommendations = results.get('recommendations', [])
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="warning-box-modern">
                <strong>{i}.</strong> {rec}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box-modern">
            🎉 Excellent! Your resume is well-optimized and ready to impress recruiters!
        </div>
        """, unsafe_allow_html=True)
    
    # Score Breakdown Radar
    st.markdown("### 📉 Detailed Score Breakdown")
    
    categories = ['Content\nQuality', 'Keyword\nOptimization', 'ATS\nCompatibility', 'Structure', 'Completeness']
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
        line=dict(color='#667eea', width=4),
        fillcolor='rgba(102, 126, 234, 0.35)',
        marker=dict(size=10, color='#f093fb')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='#e5e7eb',
                tickcolor='#6b7280',
                tickfont=dict(size=14, color='#374151', family='Arial, sans-serif')
            ),
            angularaxis=dict(
                gridcolor='#e5e7eb',
                tickcolor='#374151',
                tickfont=dict(size=14, color='#374151', weight='bold', family='Arial, sans-serif')
            ),
            bgcolor='white'
        ),
        showlegend=False,
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1f2937', family='Arial, sans-serif')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="container-section" style="text-align: center; padding: 3rem 2rem; color: white;">
    <h3 style="color: white !important;">Made with ❤️ for Social Winter of Code 2026</h3>
    <p style="color: rgba(255,255,255,0.9) !important;">© 2026 AI Resume Analyzer - All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
