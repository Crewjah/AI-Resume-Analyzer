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
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean Educational Design - Like Khan Academy / Coursera
st.markdown("""
<style>
    /* Clean Base */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    .main {
        background: #f9fafb;
        padding: 0 !important;
    }
    
    .block-container {
        max-width: 1200px !important;
        padding: 2rem !important;
        margin: 0 auto !important;
    }
    
    /* Top Navigation Bar */
    .top-nav {
        background: white;
        padding: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 3rem;
    }
    
    .nav-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .logo {
        font-size: 1.5rem;
        font-weight: 800;
        color: #2563eb;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .nav-badge {
        background: #dbeafe;
        color: #1e40af;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
    }
    
    /* Page Header */
    .page-header {
        text-align: center;
        padding: 3rem 0;
        margin-bottom: 3rem;
    }
    
    .page-title {
        font-size: 3rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .page-description {
        font-size: 1.25rem;
        color: #6b7280;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Clean Cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid #e5e7eb;
        transition: all 0.2s ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-subtitle {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    
    /* Steps */
    .steps {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .step {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2563eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .step-number {
        background: #2563eb;
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    
    .step-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.5rem;
    }
    
    .step-desc {
        font-size: 0.95rem;
        color: #6b7280;
        line-height: 1.5;
    }
    
    /* File Upload */
    [data-testid="stFileUploader"] {
        border: 2px dashed #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 3rem 2rem !important;
        background: #f8fafc !important;
        text-align: center !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #2563eb !important;
        background: #eff6ff !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #111827 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Text Area */
    .stTextArea textarea {
        border: 2px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        background: white !important;
        color: #111827 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    .stTextArea label {
        color: #111827 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Button */
    .stButton>button {
        background: #2563eb !important;
        color: white !important;
        border: none !important;
        padding: 0.875rem 2rem !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    
    .stButton>button:hover {
        background: #1d4ed8 !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    
    /* Results */
    .result-header {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .result-score {
        font-size: 4rem;
        font-weight: 900;
        margin: 1rem 0;
    }
    
    .result-label {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2563eb;
    }
    
    .metric-name {
        font-size: 0.95rem;
        color: #6b7280;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Alert Boxes */
    .alert {
        padding: 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    
    .alert-info {
        background: #eff6ff;
        border-color: #2563eb;
        color: #1e40af;
    }
    
    .alert-success {
        background: #f0fdf4;
        border-color: #16a34a;
        color: #166534;
    }
    
    .alert-warning {
        background: #fffbeb;
        border-color: #f59e0b;
        color: #92400e;
    }
    
    /* Charts */
    [data-testid="stPlotlyChart"] {
        background: white;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Typography */
    h1, h2, h3 {
        color: #111827 !important;
        font-weight: 700 !important;
    }
    
    p {
        color: #4b5563 !important;
        line-height: 1.6 !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: #2563eb !important;
    }
</style>
""", unsafe_allow_html=True)

# Navigation
st.markdown("""
<div class="top-nav">
    <div class="nav-content">
        <div class="logo">
            📝 AI Resume Analyzer
        </div>
        <div class="nav-badge">FREE TOOL</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Page Header
st.markdown("""
<div class="page-header">
    <h1 class="page-title">Improve Your Resume with AI</h1>
    <p class="page-description">Get instant feedback and actionable recommendations to make your resume stand out to recruiters</p>
</div>
""", unsafe_allow_html=True)

# How it works
st.markdown("""
<div class="card">
    <div class="card-title">📚 How It Works</div>
    <div class="card-subtitle">Simple 3-step process to analyze your resume</div>
    
    <div class="steps">
        <div class="step">
            <div class="step-number">1</div>
            <div class="step-title">Upload Resume</div>
            <div class="step-desc">Upload your resume in PDF format</div>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <div class="step-title">Add Job Details</div>
            <div class="step-desc">Optionally paste the job description</div>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <div class="step-title">Get Analysis</div>
            <div class="step-desc">Receive detailed insights and tips</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Upload Section
st.markdown("""
<div class="card">
    <div class="card-title">📄 Step 1: Upload Your Resume</div>
    <div class="card-subtitle">We support PDF files only</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose your resume (PDF)",
    type=['pdf'],
    help="Upload your resume in PDF format"
)

st.markdown("""
<div class="card">
    <div class="card-title">🎯 Step 2: Job Description (Optional)</div>
    <div class="card-subtitle">Paste the job description to get tailored recommendations</div>
</div>
""", unsafe_allow_html=True)

job_description = st.text_area(
    "Job Description",
    height=150,
    placeholder="Paste the job description here for better matching..."
)

# Analyze Button
st.markdown("""
<div class="card">
    <div class="card-title">🔍 Step 3: Analyze</div>
    <div class="card-subtitle">Click the button below to start the analysis</div>
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
    with st.spinner("Analyzing your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        analyzer = ResumeAnalyzer()
        results = analyzer.analyze_resume(resume_text, job_description if job_description else "")
        st.session_state.analyzed = True
        st.session_state.results = results

# Display Results
if st.session_state.analyzed and st.session_state.results:
    results = st.session_state.results
    
    # Overall Score
    overall_score = results.get('overall_score', 0)
    st.markdown(f"""
    <div class="result-header">
        <div class="result-label">Your Resume Score</div>
        <div class="result-score">{overall_score}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    st.markdown("""
    <div class="card">
        <div class="card-title">📊 Detailed Breakdown</div>
        <div class="metrics-grid">
    """, unsafe_allow_html=True)
    
    metrics = [
        ("Content", results.get('content_score', 0)),
        ("Keywords", results.get('keyword_score', 0)),
        ("ATS", results.get('ats_score', 0)),
        ("Structure", results.get('structure_score', 0)),
        ("Complete", results.get('completeness_score', 0))
    ]
    
    for name, value in metrics:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{value}%</div>
            <div class="metric-name">{name}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Keywords
    if results.get('keywords'):
        st.markdown("""
        <div class="card">
            <div class="card-title">🔑 Top Keywords</div>
        </div>
        """, unsafe_allow_html=True)
        
        keywords = results['keywords']
        if keywords:
            fig = px.bar(
                x=list(keywords.keys())[:10],
                y=list(keywords.values())[:10],
                labels={'x': 'Keyword', 'y': 'Count'},
                color_discrete_sequence=['#2563eb']
            )
            fig.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=0, r=0, t=20, b=0),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#111827', size=12)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.markdown("""
    <div class="card">
        <div class="card-title">💡 Recommendations</div>
    </div>
    """, unsafe_allow_html=True)
    
    recommendations = results.get('recommendations', [])
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="alert alert-warning">
                <strong>{i}.</strong> {rec}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert alert-success">
            ✓ Great job! Your resume looks well-optimized.
        </div>
        """, unsafe_allow_html=True)
    
    # Radar Chart
    st.markdown("""
    <div class="card">
        <div class="card-title">📈 Score Breakdown</div>
    </div>
    """, unsafe_allow_html=True)
    
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
        line=dict(color='#2563eb', width=2),
        fillcolor='rgba(37, 99, 235, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
            bgcolor='white'
        ),
        showlegend=False,
        height=400,
        paper_bgcolor='white',
        font=dict(color='#111827')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 3rem 0; color: #6b7280;">
    <p>Made for Social Winter of Code 2026</p>
</div>
""", unsafe_allow_html=True)
