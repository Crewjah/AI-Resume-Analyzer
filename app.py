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
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --card-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header styling with enhanced animation */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.3);
        animation: slideDown 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
        letter-spacing: -1px;
    }
    
    .main-header p {
        font-size: 1.3rem;
        margin-top: 0.8rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
        font-weight: 300;
    }
    
    /* Enhanced card styling */
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
        margin: 1.5rem 0;
        border-left: 5px solid transparent;
        border-image: linear-gradient(135deg, #667eea, #764ba2) 1;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.05), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.15);
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    /* Score display with pulse animation */
    .score-container {
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        animation: fadeInScale 0.6s ease-out;
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .score-container::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        transform: translate(-50%, -50%);
        animation: ripple 2s infinite;
    }
    
    .score-value {
        font-size: 5rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 3px 3px 10px rgba(0, 0, 0, 0.3);
        animation: countUp 1s ease-out;
        position: relative;
        z-index: 1;
    }
    
    /* Enhanced animations */
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
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
    
    @keyframes ripple {
        0% {
            width: 0;
            height: 0;
            opacity: 0.5;
        }
        100% {
            width: 400px;
            height: 400px;
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
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    /* Upload section with gradient border */
    .upload-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
    }
    
    .upload-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
    }
    
    /* Enhanced button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.9rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* Progress bar enhancement */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        animation: pulse 2s infinite;
    }
    
    /* Sidebar enhancement */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Info boxes with modern design */
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
        animation: fadeInScale 0.5s ease-out;
    }
    
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
        animation: fadeInScale 0.5s ease-out;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #FF9800;
        margin: 1rem 0;
        animation: fadeInScale 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .warning-box:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 20px rgba(255, 152, 0, 0.2);
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        background: linear-gradient(135deg, #fafbff 0%, #f0f2ff 100%);
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #f0f2ff 0%, #e8ebff 100%);
        transform: scale(1.01);
    }
    
    /* Text area enhancement */
    .stTextArea textarea {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
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
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📤 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload your resume in PDF format for analysis"
    )

with col2:
    st.markdown("### 💼 Job Description (Optional)")
    job_description = st.text_area(
        "Paste job description here",
        height=150,
        placeholder="Enter the job description to calculate match score..."
    )

if uploaded_file is not None:
    # Process button
    if st.button("🚀 Analyze Resume", type="primary"):
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
st.markdown("""
<div style="text-align: center; padding: 3rem 0 2rem 0;">
    <div style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 0.5rem 2rem; border-radius: 50px; margin-bottom: 1rem;">
        <span style="color: white; font-weight: 600; font-size: 1rem;">AI Resume Analyzer</span>
    </div>
    <p style="color: #666; font-size: 0.9rem; margin: 1rem 0;">
        Empowering careers with AI-driven insights
    </p>
    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1.5rem; flex-wrap: wrap;">
        <a href="https://github.com/Crewjah/AI-Resume-Analyzer" target="_blank" 
           style="color: #667eea; text-decoration: none; font-weight: 500; transition: all 0.3s;">
            GitHub
        </a>
        <span style="color: #667eea; font-weight: 500;">•</span>
        <span style="color: #888;">SWOC 2026</span>
        <span style="color: #667eea; font-weight: 500;">•</span>
        <span style="color: #888;">Open Source</span>
    </div>
</div>
""", unsafe_allow_html=True)
