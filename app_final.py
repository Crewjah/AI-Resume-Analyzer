import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from resume_analyzer import ResumeAnalyzer
from pdf_extractor import extract_text_from_pdf
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern Professional Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    .main {
        background: linear-gradient(to bottom, #0f172a 0%, #1e293b 100%);
        padding: 0 !important;
    }
    
    .block-container {
        max-width: 1400px !important;
        padding: 0 !important;
        margin: 0 auto !important;
    }
    
    /* Hero */
    .hero {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 50%, #14b8a6 100%);
        padding: 4rem 3rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero::before {
        content: '';
        position: absolute;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 40px 40px;
        top: -50%;
        left: -50%;
        animation: drift 30s linear infinite;
    }
    
    @keyframes drift {
        from {transform: rotate(0deg);}
        to {transform: rotate(360deg);}
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
    }
    
    .hero h1 {
        font-size: 4rem;
        font-weight: 900;
        color: white;
        margin: 0 0 1.5rem 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        letter-spacing: -1px;
    }
    
    .hero p {
        font-size: 1.5rem;
        color: rgba(255,255,255,0.95);
        margin: 0;
        font-weight: 500;
    }
    
    /* Main Content */
    .content-wrapper {
        padding: 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Modern Card */
    .modern-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .modern-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(14, 165, 233, 0.3);
        border-color: rgba(14, 165, 233, 0.3);
    }
    
    .card-header {
        font-size: 1.75rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .card-desc {
        font-size: 1.05rem;
        color: rgba(255,255,255,0.7);
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Upload Zone */
    [data-testid="stFileUploader"] {
        border: 3px dashed rgba(14, 165, 233, 0.5) !important;
        border-radius: 16px !important;
        padding: 4rem 2rem !important;
        background: rgba(14, 165, 233, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #0ea5e9 !important;
        background: rgba(14, 165, 233, 0.1) !important;
        transform: scale(1.02) !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important;
    }
    
    /* Text Area */
    .stTextArea label {
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 2px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 1.25rem !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #0ea5e9 !important;
        background: rgba(15, 23, 42, 0.8) !important;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.2) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: rgba(255,255,255,0.4) !important;
    }
    
    /* Button */
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1.25rem 3rem !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 24px rgba(14, 165, 233, 0.4) !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 32px rgba(14, 165, 233, 0.5) !important;
    }
    
    /* Results Section */
    .score-display {
        background: linear-gradient(135deg, #0ea5e9 0%, #14b8a6 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 12px 40px rgba(14, 165, 233, 0.4);
    }
    
    .score-title {
        font-size: 1.5rem;
        color: rgba(255,255,255,0.9);
        margin-bottom: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .score-value {
        font-size: 6rem;
        font-weight: 900;
        color: white;
        margin: 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    /* Metrics */
    .metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric {
        background: rgba(30, 41, 59, 0.6);
        border: 2px solid rgba(14, 165, 233, 0.3);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric:hover {
        border-color: #0ea5e9;
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(14, 165, 233, 0.3);
    }
    
    .metric-val {
        font-size: 3rem;
        font-weight: 900;
        color: #0ea5e9;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: rgba(255,255,255,0.7);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Alert Box */
    .alert-box {
        background: rgba(6, 182, 212, 0.1);
        border-left: 4px solid #06b6d4;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: rgba(255,255,255,0.9);
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    .success-box {
        background: rgba(20, 184, 166, 0.1);
        border-left: 4px solid #14b8a6;
    }
    
    .warning-box {
        background: rgba(251, 146, 60, 0.1);
        border-left: 4px solid #fb923c;
    }
    
    /* Charts */
    [data-testid="stPlotlyChart"] {
        background: rgba(30, 41, 59, 0.4);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Typography */
    h1, h2, h3 {
        color: white !important;
    }
    
    p {
        color: rgba(255,255,255,0.8) !important;
    }
    
    .stMarkdown h3 {
        color: #0ea5e9 !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        margin: 2rem 0 1rem 0 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #0ea5e9 !important;
    }
    
    /* Progress */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0ea5e9, #06b6d4, #14b8a6) !important;
    }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1>🚀 AI Resume Analyzer</h1>
        <p>Transform your resume with AI-powered insights and recommendations</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Content
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Upload Card
st.markdown("""
<div class="modern-card">
    <div class="card-header">📄 Upload Your Resume</div>
    <div class="card-desc">Upload your resume in PDF format to get started with AI analysis</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop your PDF here or click to browse",
    type=['pdf'],
    label_visibility="collapsed"
)

# Job Description Card
st.markdown("""
<div class="modern-card">
    <div class="card-header">🎯 Job Description (Optional)</div>
    <div class="card-desc">Add the job description to get personalized matching insights</div>
</div>
""", unsafe_allow_html=True)

job_description = st.text_area(
    "Paste job description here",
    height=160,
    placeholder="Paste the target job description here for tailored recommendations and keyword matching...",
    label_visibility="collapsed"
)

# Analyze Button
st.markdown("""
<div class="modern-card">
    <div class="card-header">🔍 Ready to Analyze</div>
    <div class="card-desc">Click below to start your comprehensive resume analysis</div>
</div>
""", unsafe_allow_html=True)

analyze_button = st.button("Analyze My Resume")

# Session state
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'results' not in st.session_state:
    st.session_state.results = None

# Analysis
if analyze_button and uploaded_file:
    with st.spinner("🤖 AI is analyzing your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        analyzer = ResumeAnalyzer()
        results = analyzer.analyze_resume(resume_text, job_description if job_description else "")
        st.session_state.analyzed = True
        st.session_state.results = results

# Results
if st.session_state.analyzed and st.session_state.results:
    results = st.session_state.results
    
    # Score
    overall_score = results.get('overall_score', 0)
    st.markdown(f"""
    <div class="score-display">
        <div class="score-title">Your Overall Score</div>
        <div class="score-value">{overall_score}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    st.markdown("""
    <div class="modern-card">
        <div class="card-header">📊 Score Breakdown</div>
        <div class="metrics">
    """, unsafe_allow_html=True)
    
    metrics = [
        ("Content", results.get('content_score', 0)),
        ("Keywords", results.get('keyword_score', 0)),
        ("ATS", results.get('ats_score', 0)),
        ("Structure", results.get('structure_score', 0)),
        ("Completeness", results.get('completeness_score', 0))
    ]
    
    for name, value in metrics:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-val">{value}%</div>
            <div class="metric-label">{name}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Keywords Chart
    if results.get('keywords'):
        st.markdown("### 🔑 Top Keywords Found")
        keywords = results['keywords']
        
        if keywords:
            fig = px.bar(
                x=list(keywords.keys())[:10],
                y=list(keywords.values())[:10],
                labels={'x': 'Keyword', 'y': 'Frequency'},
                color=list(keywords.values())[:10],
                color_continuous_scale=['#0ea5e9', '#06b6d4', '#14b8a6']
            )
            fig.update_layout(
                showlegend=False,
                height=350,
                margin=dict(l=0, r=0, t=20, b=0),
                plot_bgcolor='rgba(30, 41, 59, 0.4)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                xaxis=dict(showgrid=False, color='rgba(255,255,255,0.7)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='rgba(255,255,255,0.7)')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.markdown("### 💡 AI Recommendations")
    recommendations = results.get('recommendations', [])
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="warning-box alert-box">
                <strong>{i}.</strong> {rec}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box alert-box">
            ✓ Excellent! Your resume is well-optimized and ready for applications.
        </div>
        """, unsafe_allow_html=True)
    
    # Radar Chart
    st.markdown("### 📈 Visual Score Analysis")
    
    categories = ['Content', 'Keywords', 'ATS', 'Structure', 'Complete']
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
        line=dict(color='#0ea5e9', width=3),
        fillcolor='rgba(14, 165, 233, 0.3)',
        marker=dict(size=8, color='#14b8a6')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255,255,255,0.2)',
                tickcolor='rgba(255,255,255,0.5)'
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.2)',
                tickcolor='rgba(255,255,255,0.7)'
            ),
            bgcolor='rgba(30, 41, 59, 0.4)'
        ),
        showlegend=False,
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=13)
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 3rem; color: rgba(255,255,255,0.6);">
    <p>Made with ❤️ for Social Winter of Code 2026</p>
</div>
""", unsafe_allow_html=True)
