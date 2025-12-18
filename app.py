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

# Modern CSS Theme - Cyan/Blue Fresh Design
st.markdown("""
<style>
    /* Base & Layout */
    .main {
        padding: 0 !important;
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #2a2f4a 100%);
        min-height: 100vh;
    }
    
    .block-container {
        max-width: 100% !important;
        padding: 2.5rem 3rem !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    html {scroll-behavior: smooth;}
    
    /* Glassmorphism Header */
    .main-header {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 0 0 2rem 0;
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: slide 3s ease-in-out infinite;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        color: white;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin-top: 0.5rem;
        color: rgba(255,255,255,0.9);
        position: relative;
        z-index: 1;
    }
    
    /* Cards */
    .content-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .content-card:hover {
        border-color: rgba(14, 165, 233, 0.3);
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.2);
        transform: translateY(-2px);
    }
    
    .content-card h3 {
        color: #0ea5e9;
        font-size: 1.4rem;
        margin: 0 0 1rem 0;
        font-weight: 600;
    }
    
    /* Inputs */
    [data-testid="stFileUploader"] {
        border: 2px dashed rgba(14, 165, 233, 0.5) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        background: rgba(14, 165, 233, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #0ea5e9 !important;
        background: rgba(14, 165, 233, 0.1) !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #0ea5e9 !important;
        font-weight: 600 !important;
    }
    
    .stTextArea textarea {
        background: rgba(14, 165, 233, 0.05) !important;
        border: 1px solid rgba(14, 165, 233, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2) !important;
    }
    
    .stTextArea label {
        color: #0ea5e9 !important;
        font-weight: 600 !important;
    }
    
    /* Button */
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px rgba(14, 165, 233, 0.4) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5) !important;
    }
    
    /* Score Containers */
    .score-container {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15), rgba(6, 182, 212, 0.15));
        border: 1px solid rgba(14, 165, 233, 0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(14, 165, 233, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .score-container h3 {
        color: #0ea5e9;
        margin: 0 0 1rem 0;
        font-size: 1.2rem;
    }
    
    .score-value {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0ea5e9, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: rgba(14, 165, 233, 0.08);
        border: 1px solid rgba(14, 165, 233, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(14, 165, 233, 0.4);
        transform: translateY(-3px);
    }
    
    /* Info Boxes */
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .success-box {
        background: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .warning-box {
        background: rgba(251, 146, 60, 0.1);
        border-left: 4px solid #fb923c;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: rgba(255, 255, 255, 0.9);
        transition: all 0.3s ease;
    }
    
    .warning-box:hover {
        transform: translateX(5px);
    }
    
    /* Charts */
    [data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }
    
    [data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
    }
    
    /* Text Colors */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    p, span, label {
        color: rgba(255, 255, 255, 0.85) !important;
    }
    
    .stMarkdown h3, .stMarkdown h4 {
        color: #0ea5e9 !important;
        font-weight: 600 !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0ea5e9, #06b6d4) !important;
    }
    
    /* Success Message */
    .stSuccess {
        background: rgba(34, 197, 94, 0.15) !important;
        border-left: 4px solid #22c55e !important;
        color: white !important;
    }
    
    .stAlert {
        background: rgba(59, 130, 246, 0.15) !important;
        border-left: 4px solid #3b82f6 !important;
        color: white !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #0ea5e9, #06b6d4);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #06b6d4, #0284c7);
    }
    
    /* Animations */
    @keyframes slide {
        0%, 100% {transform: translateX(-100%);}
        50% {transform: translateX(100%);}
    }
    
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    
    /* Apply fade animation */
    .content-card, .score-container, .metric-card {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Header
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
                color_continuous_scale='Teal'
            )
            fig.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=0, r=0, t=30, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(showgrid=False, color='rgba(255,255,255,0.5)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(14,165,233,0.2)', color='rgba(255,255,255,0.5)')
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
        line=dict(color='#0ea5e9', width=2),
        fillcolor='rgba(14, 165, 233, 0.25)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(14, 165, 233, 0.2)',
                tickcolor='rgba(255,255,255,0.5)'
            ),
            angularaxis=dict(
                gridcolor='rgba(14, 165, 233, 0.2)',
                tickcolor='rgba(255,255,255,0.5)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
