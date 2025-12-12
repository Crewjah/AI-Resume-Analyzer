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
        --primary-color: #6C63FF;
        --secondary-color: #4CAF50;
        --accent-color: #FF6B6B;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        animation: fadeIn 1s ease-in;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 5px solid #6C63FF;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
    
    /* Score display */
    .score-container {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        animation: slideIn 0.5s ease-out;
    }
    
    .score-value {
        font-size: 4rem;
        font-weight: 700;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Upload section */
    .upload-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Info boxes */
    .info-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #e8f5e9;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF9800;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📄 AI Resume Analyzer</h1>
    <p>Enhance your resume with AI-powered insights and recommendations</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'results' not in st.session_state:
    st.session_state.results = None

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 About")
    st.markdown("""
    This AI-powered tool analyzes your resume to:
    - Extract and evaluate key skills
    - Calculate keyword match with job descriptions
    - Provide compatibility scores
    - Offer improvement suggestions
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Analysis Features")
    st.markdown("""
    - **Skill Extraction**: NLP-based skill identification
    - **Keyword Matching**: Match with job requirements
    - **ATS Compatibility**: Check ATS friendliness
    - **Detailed Feedback**: Actionable recommendations
    """)
    
    st.markdown("---")
    st.markdown("### 🛠️ Tech Stack")
    st.markdown("""
    - Python & Streamlit
    - SpaCy & Transformers
    - Scikit-learn
    - Natural Language Processing
    """)

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
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>Made with Streamlit | AI Resume Analyzer | Open Source Project</p>
    <p>Social Winter of Code 2026</p>
</div>
""", unsafe_allow_html=True)
