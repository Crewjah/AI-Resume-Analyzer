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

# Hide sidebar completely
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Remove padding and make fullscreen */
    .main {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .block-container {
        max-width: 100% !important;
        padding: 2rem !important;
        padding-top: 1rem !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Header styling with enhanced animation */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%, #f093fb 100%);
        padding: 4rem 3rem;
        border-radius: 30px;
        text-align: center;
        color: white;
        margin: 0 0 3rem 0;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        animation: slideDown 0.9s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        animation: rotate 25s linear infinite;
        z-index: 0;
    }
    
    .main-header h1 {
        font-size: 4rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
        letter-spacing: -1px;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .main-header p {
        font-size: 1.4rem;
        margin-top: 1rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
        font-weight: 300;
        letter-spacing: 0.5px;
        animation: fadeInUp 0.8s ease-out 0.2s backwards;
    }
    
    /* Content sections */
    .content-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        padding: 2.5rem;
        border-radius: 25px;
        margin: 1.5rem 0;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(20px);
        animation: fadeInScale 0.7s ease-out;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .content-card:hover {
        box-shadow: 0 25px 70px rgba(102, 126, 234, 0.25), inset 0 1px 0 rgba(255,255,255,0.1);
        transform: translateY(-5px);
        border: 1px solid rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.06) 100%);
    }
    
    .content-card h3 {
        color: #ffffff;
        font-size: 1.8rem;
        margin: 0 0 1.5rem 0;
        font-weight: 700;
        animation: slideInLeft 0.6s ease-out;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Upload and input styling */
    [data-testid="stFileUploader"] {
        border: 3px dashed #667eea !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%) !important;
        transition: all 0.3s ease !important;
        box-shadow: inset 0 0 30px rgba(102, 126, 234, 0.1) !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2 !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%) !important;
        transform: scale(1.02) !important;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3), inset 0 0 30px rgba(102, 126, 234, 0.15) !important;
    }
    
    .stTextArea textarea {
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%) !important;
        color: white !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%) !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2), 0 0 20px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1.2rem 3rem !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 35px rgba(102, 126, 234, 0.4) !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
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
        background: rgba(255, 255, 255, 0.2);
        transition: left 0.5s ease;
        z-index: -1;
    }
    
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.6);
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:active {
        transform: translateY(-2px) scale(0.98);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        animation: pulse 2s infinite;
    }
    
    /* Metric card styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.15) 0%, rgba(0, 242, 254, 0.15) 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(79, 172, 254, 0.2), inset 0 1px 0 rgba(255,255,255,0.1);
        margin: 1.5rem 0;
        border: 1px solid rgba(79, 172, 254, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: fadeInScale 0.6s ease-out;
        backdrop-filter: blur(10px);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
        transition: left 0.6s;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 60px rgba(79, 172, 254, 0.4), inset 0 1px 0 rgba(255,255,255,0.1);
        border-color: rgba(0, 242, 254, 0.6);
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.25) 0%, rgba(0, 242, 254, 0.25) 100%);
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    /* Score container */
    .score-container {
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 25px;
        color: white;
        animation: fadeInScale 0.7s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .score-container::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        transform: translate(-50%, -50%);
        animation: ripple 2s infinite;
    }
    
    .score-value {
        font-size: 5.5rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 4px 4px 12px rgba(0, 0, 0, 0.3);
        animation: countUp 1.2s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        z-index: 1;
        letter-spacing: -2px;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 18px;
        border-left: 6px solid #2196F3;
        margin: 1.2rem 0;
        animation: slideInLeft 0.6s ease-out;
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.15);
    }
    
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1.5rem;
        border-radius: 18px;
        border-left: 6px solid #4CAF50;
        margin: 1.2rem 0;
        animation: slideInLeft 0.6s ease-out;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.15);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1.5rem;
        border-radius: 18px;
        border-left: 6px solid #FF9800;
        margin: 1.2rem 0;
        animation: slideInLeft 0.6s ease-out;
        box-shadow: 0 8px 25px rgba(255, 152, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    .warning-box:hover {
        transform: translateX(8px);
        box-shadow: 0 12px 35px rgba(255, 152, 0, 0.25);
    }
    
    /* Animation keyframes */
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-60px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-40px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeInDown {
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
    
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.92);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes countUp {
        from {
            opacity: 0;
            transform: scale(0.5) rotateY(180deg);
        }
        to {
            opacity: 1;
            transform: scale(1) rotateY(0deg);
        }
    }
    
    @keyframes ripple {
        0% {
            width: 0;
            height: 0;
            opacity: 0.5;
        }
        100% {
            width: 500px;
            height: 500px;
            opacity: 0;
        }
    }
    
    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scaleY(1);
        }
        50% {
            transform: scaleY(1.1);
        }
    }
    
    /* Plotly chart styling */
    [data-testid="stPlotlyChart"] {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
    }
    
    /* Column layout */
    [data-testid="column"] {
        animation: fadeInScale 0.7s ease-out;
    }
    
    /* Background gradient for main page */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }
    
    body {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
    }
    
    /* Enhanced dark theme colors for text */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    p, span, label {
        color: rgba(255, 255, 255, 0.85) !important;
    }
    
    /* Expander styling */
    [data-testid="stExpander"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 15px !important;
    }
    
    /* Success messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.2) 0%, rgba(0, 242, 254, 0.2) 100%) !important;
        border-left: 4px solid #4facfe !important;
        border-radius: 15px !important;
        padding: 1.2rem !important;
        color: white !important;
    }
    
    .stAlert {
        border-radius: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>AI Resume Analyzer</h1>
    <p>Transform Your Resume with AI-Powered Intelligence</p>
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
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=0, r=0, t=30, b=0)
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
        line=dict(color='#667eea', width=3),
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
