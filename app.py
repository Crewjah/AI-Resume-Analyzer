"""
AI Resume Analyzer - Professional Resume Optimization Tool
Version: 2.0.0
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
from pathlib import Path
import io

# Import backend modules
from backend.resume_analyzer import ResumeAnalyzer
from backend.pdf_extractor import extract_text_from_pdf
import backend.keyword_matcher as km

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AI Resume Analyzer 2.0",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
<style>
    /* Color Scheme */
    :root {
        --primary-blue: #2563EB;
        --primary-dark: #1D4ED8;
        --success-green: #10B981;
        --warning-amber: #F59E0B;
        --error-red: #EF4444;
        --bg-light: #F9FAFB;
        --text-primary: #111827;
        --text-secondary: #6B7280;
    }
    
    /* Main App Background */
    .main {
        background-color: #FFFFFF;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #F9FAFB;
    }
    
    /* Active Navigation Item */
    .nav-active {
        background-color: #DBEAFE !important;
        color: #2563EB !important;
        border-left: 4px solid #2563EB;
        font-weight: 600;
    }
    
    /* Score Cards */
    .score-excellent {
        color: #10B981;
        font-weight: 600;
    }
    
    .score-good {
        color: #F59E0B;
        font-weight: 600;
    }
    
    .score-poor {
        color: #EF4444;
        font-weight: 600;
    }
    
    /* Primary Button */
    .stButton > button {
        background-color: #2563EB;
        color: white;
        font-weight: 500;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
        transition: background-color 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #1D4ED8;
    }
    
    /* Success Message */
    .success-box {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #10B981;
        margin: 1rem 0;
    }
    
    /* Error Message */
    .error-box {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #EF4444;
        margin: 1rem 0;
    }
    
    /* Warning Message */
    .warning-box {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #F59E0B;
        margin: 1rem 0;
    }
    
    /* Progress Bar */
    .progress-bar {
        background-color: #E5E7EB;
        border-radius: 8px;
        height: 24px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        background-color: #2563EB;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.875rem;
        font-weight: 500;
        transition: width 0.5s ease;
    }
    
    /* File Upload Zone */
    [data-testid="stFileUploader"] {
        border: 2px dashed #D1D5DB;
        border-radius: 8px;
        padding: 2rem;
        background-color: #F9FAFB;
        transition: border-color 0.3s;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #2563EB;
        background-color: #EFF6FF;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
    
    /* Headers */
    h1 {
        color: #111827;
        font-weight: 700;
    }
    
    h2 {
        color: #1F2937;
        font-weight: 600;
    }
    
    h3 {
        color: #374151;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Upload'
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {}
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'ats_weight': 25,
        'skill_weight': 30,
        'experience_weight': 25,
        'education_weight': 20,
        'target_industry': 'Technology',
        'file_size_limit': 5
    }

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_file(uploaded_file, max_size_mb=5):
    """Validate uploaded file"""
    try:
        if uploaded_file is None:
            return False, "No file selected"
        
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > max_size_mb:
            return False, f"File too large: {file_size_mb:.1f}MB (Max: {max_size_mb}MB)"
        
        allowed_types = ['.pdf', '.docx', '.doc', '.txt']
        file_ext = Path(uploaded_file.name).suffix.lower()
        if file_ext not in allowed_types:
            return False, f"Invalid file type: {file_ext}"
        
        return True, "Valid"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def extract_resume_text(uploaded_file):
    """Extract text from uploaded resume"""
    try:
        file_ext = Path(uploaded_file.name).suffix.lower()
        
        if file_ext == '.pdf':
            text = extract_text_from_pdf(uploaded_file)
        elif file_ext in ['.docx', '.doc']:
            try:
                from docx import Document
                doc = Document(uploaded_file)
                text = '\n'.join([para.text for para in doc.paragraphs])
            except:
                text = uploaded_file.read().decode('utf-8', errors='ignore')
        else:
            text = uploaded_file.read().decode('utf-8', errors='ignore')
        
        if not text or len(text.strip()) < 50:
            return None, "Could not extract sufficient text from file"
        
        return text, None
    except Exception as e:
        return None, f"Text extraction failed: {str(e)}"

def analyze_resume(resume_text):
    """Analyze resume using backend analyzer"""
    try:
        analyzer = ResumeAnalyzer()
        results = analyzer.analyze(resume_text)
        return results, None
    except Exception as e:
        return None, f"Analysis failed: {str(e)}"

def get_score_status(score):
    """Get status text and color based on score"""
    if score >= 85:
        return "Excellent", "score-excellent"
    elif score >= 70:
        return "Good", "score-good"
    elif score >= 50:
        return "Fair", "score-good"
    else:
        return "Needs Improvement", "score-poor"

def create_gauge_chart(score, title):
    """Create gauge chart for score visualization"""
    try:
        color = "#10B981" if score >= 85 else "#F59E0B" if score >= 70 else "#EF4444"
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title, 'font': {'size': 16}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#E5E7EB",
                'steps': [
                    {'range': [0, 50], 'color': '#FEE2E2'},
                    {'range': [50, 70], 'color': '#FEF3C7'},
                    {'range': [70, 85], 'color': '#D1FAE5'},
                    {'range': [85, 100], 'color': '#A7F3D0'}
                ],
                'threshold': {
                    'line': {'color': "#111827", 'width': 2},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))
        
        fig.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor='white',
            font={'family': 'system-ui'}
        )
        return fig
    except Exception as e:
        st.error(f"Chart creation failed: {str(e)}")
        return None

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown("## Navigation")
    
    # Upload & Analyze
    if st.button(
        "Upload & Analyze",
        key="nav_upload",
        use_container_width=True,
        type="primary" if st.session_state.current_page == "Upload" else "secondary"
    ):
        st.session_state.current_page = "Upload"
        st.rerun()
    
    # Results Dashboard
    if st.button(
        "Results Dashboard",
        key="nav_results",
        use_container_width=True,
        type="primary" if st.session_state.current_page == "Results" else "secondary"
    ):
        st.session_state.current_page = "Results"
        st.rerun()
    
    # Job Matching
    if st.button(
        "Job Matching",
        key="nav_job",
        use_container_width=True,
        type="primary" if st.session_state.current_page == "Job Matching" else "secondary"
    ):
        st.session_state.current_page = "Job Matching"
        st.rerun()
    
    # Settings
    if st.button(
        "Settings",
        key="nav_settings",
        use_container_width=True,
        type="primary" if st.session_state.current_page == "Settings" else "secondary"
    ):
        st.session_state.current_page = "Settings"
        st.rerun()
    
    st.divider()
    
    # Quick Stats
    st.markdown("### Quick Stats")
    total_resumes = len(st.session_state.uploaded_files)
    st.metric("Resumes Analyzed", total_resumes)
    st.metric("Version", "2.0.0")

# ============================================================================
# PAGE: UPLOAD & ANALYZE
# ============================================================================

if st.session_state.current_page == "Upload":
    st.title("Upload Resume")
    
    st.markdown("""
    Upload your resume to get instant analysis with actionable insights.
    Supported formats: PDF, DOCX, TXT (Max size: 5MB)
    """)
    
    st.divider()
    
    # File Upload
    uploaded_file = st.file_uploader(
        "Choose a resume file",
        type=['pdf', 'docx', 'doc', 'txt'],
        help="Drag and drop or click to browse",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        # Validate file
        is_valid, validation_msg = validate_file(uploaded_file, max_size_mb=5)
        
        if not is_valid:
            st.markdown(f'<div class="error-box">Error: {validation_msg}</div>', unsafe_allow_html=True)
            st.stop()
        
        # Show file info
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**File:** {uploaded_file.name}")
        with col2:
            st.write(f"**Size:** {uploaded_file.size/1024:.1f} KB")
        with col3:
            if st.button("Remove File"):
                st.rerun()
        
        st.divider()
        
        # Analyze Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_clicked = st.button("ANALYZE NOW", use_container_width=True, type="primary")
        
        if analyze_clicked:
            with st.spinner("Analyzing your resume..."):
                # Extract text
                resume_text, extract_error = extract_resume_text(uploaded_file)
                
                if extract_error:
                    st.markdown(f'<div class="error-box">{extract_error}</div>', unsafe_allow_html=True)
                    st.stop()
                
                # Analyze resume
                analysis_results, analysis_error = analyze_resume(resume_text)
                
                if analysis_error:
                    st.markdown(f'<div class="error-box">{analysis_error}</div>', unsafe_allow_html=True)
                    st.stop()
                
                # Store results
                file_key = f"{uploaded_file.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.uploaded_files[file_key] = {
                    'name': uploaded_file.name,
                    'size': uploaded_file.size,
                    'timestamp': datetime.now().isoformat()
                }
                st.session_state.analysis_results[file_key] = {
                    'text': resume_text,
                    'analysis': analysis_results
                }
            
            # Success message
            st.markdown('<div class="success-box"><strong>Analysis Complete!</strong><br>Your resume has been analyzed successfully.</div>', unsafe_allow_html=True)
            st.balloons()
            
            # Quick Preview
            st.markdown("### Quick Results Preview")
            
            scores = analysis_results.get('scores', {})
            overall = scores.get('overall_score', 0)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Overall", f"{overall}%")
            with col2:
                st.metric("ATS", f"{scores.get('ats_compatibility', 0)}%")
            with col3:
                st.metric("Keywords", f"{scores.get('keyword_optimization', 0)}%")
            with col4:
                st.metric("Content", f"{scores.get('content_quality', 0)}%")
            with col5:
                st.metric("Structure", f"{scores.get('structure_score', 0)}%")
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("View Full Results", use_container_width=True):
                    st.session_state.current_page = "Results"
                    st.rerun()
            with col2:
                if st.button("Match with Job", use_container_width=True):
                    st.session_state.current_page = "Job Matching"
                    st.rerun()
    
    else:
        st.info("Click above to upload your resume")

# ============================================================================
# PAGE: RESULTS DASHBOARD
# ============================================================================

elif st.session_state.current_page == "Results":
    st.title("Analysis Results")
    
    if not st.session_state.analysis_results:
        st.warning("No analysis results available. Please upload and analyze a resume first.")
        if st.button("Go to Upload"):
            st.session_state.current_page = "Upload"
            st.rerun()
        st.stop()
    
    # Select Resume
    file_keys = list(st.session_state.analysis_results.keys())
    selected_key = st.selectbox("Select Resume", file_keys, format_func=lambda x: st.session_state.uploaded_files[x]['name'])
    
    result_data = st.session_state.analysis_results[selected_key]
    analysis = result_data['analysis']
    scores = analysis.get('scores', {})
    
    st.divider()
    
    # Overall Score
    overall_score = scores.get('overall_score', 0)
    status_text, status_class = get_score_status(overall_score)
    
    st.markdown(f"## Overall Score: {overall_score}% - {status_text}")
    
    st.divider()
    
    # Score Breakdown Table
    st.markdown("### Score Breakdown")
    
    score_data = {
        'Category': ['Content Quality', 'Keyword Optimization', 'ATS Compatibility', 'Structure', 'Completeness'],
        'Score': [
            scores.get('content_quality', 0),
            scores.get('keyword_optimization', 0),
            scores.get('ats_compatibility', 0),
            scores.get('structure_score', 0),
            scores.get('completeness', 0)
        ]
    }
    
    score_df = pd.DataFrame(score_data)
    score_df['Status'] = score_df['Score'].apply(lambda x: get_score_status(x)[0])
    
    st.dataframe(score_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Gauge Charts
    st.markdown("### Detailed Scores")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig = create_gauge_chart(scores.get('content_quality', 0), "Content Quality")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_gauge_chart(scores.get('keyword_optimization', 0), "Keywords")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        fig = create_gauge_chart(scores.get('ats_compatibility', 0), "ATS Score")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Skills
    st.markdown("### Detected Skills")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Technical Skills**")
        tech_skills = analysis.get('technical_skills', [])
        if tech_skills:
            for skill in tech_skills[:10]:
                st.write(f"- {skill}")
        else:
            st.info("No technical skills detected")
    
    with col2:
        st.markdown("**Soft Skills**")
        soft_skills = analysis.get('soft_skills', [])
        if soft_skills:
            for skill in soft_skills[:10]:
                st.write(f"- {skill}")
        else:
            st.info("No soft skills detected")
    
    st.divider()
    
    # Recommendations
    st.markdown("### Recommendations")
    
    recommendations = analysis.get('recommendations', [])
    if recommendations:
        for i, rec in enumerate(recommendations[:5], 1):
            with st.expander(f"{i}. {rec.get('title', 'Recommendation')}"):
                st.write(rec.get('description', ''))
    else:
        st.info("No recommendations available")
    
    st.divider()
    
    # Export Options
    st.markdown("### Download Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV Export
        csv_data = score_df.to_csv(index=False)
        st.download_button(
            "Download as CSV",
            csv_data,
            f"resume_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col2:
        # JSON Export
        json_data = json.dumps(analysis, indent=2)
        st.download_button(
            "Download as JSON",
            json_data,
            f"resume_analysis_{datetime.now().strftime('%Y%m%d')}.json",
            "application/json",
            use_container_width=True
        )
    
    with col3:
        if st.button("Analyze Another Resume", use_container_width=True):
            st.session_state.current_page = "Upload"
            st.rerun()

# ============================================================================
# PAGE: JOB MATCHING
# ============================================================================

elif st.session_state.current_page == "Job Matching":
    st.title("Job Matching")
    
    if not st.session_state.analysis_results:
        st.warning("No resume data available. Please upload and analyze a resume first.")
        if st.button("Go to Upload"):
            st.session_state.current_page = "Upload"
            st.rerun()
        st.stop()
    
    # Select Resume
    file_keys = list(st.session_state.analysis_results.keys())
    selected_key = st.selectbox("Select Resume to Match", file_keys, format_func=lambda x: st.session_state.uploaded_files[x]['name'])
    
    result_data = st.session_state.analysis_results[selected_key]
    resume_text = result_data['text']
    
    st.divider()
    
    # Job Description Input
    st.markdown("### Paste Job Description")
    
    job_description = st.text_area(
        "Job description",
        height=200,
        placeholder="Paste the job description here...",
        label_visibility="collapsed"
    )
    
    if job_description:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            match_clicked = st.button("MATCH NOW", use_container_width=True, type="primary")
        
        if match_clicked:
            with st.spinner("Calculating match score..."):
                try:
                    # Calculate match
                    match_score = km.calculate_match_score(resume_text, job_description)
                    missing_keywords = km.find_missing_keywords(resume_text, job_description)
                    
                    st.divider()
                    st.markdown("### Match Results")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Match Score", f"{match_score}%")
                    
                    with col2:
                        matched = max(0, 100 - len(missing_keywords[:20]))
                        st.metric("Keywords Matched", f"{matched}%")
                    
                    with col3:
                        st.metric("Missing Keywords", len(missing_keywords[:20]))
                    
                    st.divider()
                    
                    # Recommendation
                    if match_score >= 80:
                        st.markdown('<div class="success-box"><strong>Great Match!</strong><br>Your resume aligns well with this job description.</div>', unsafe_allow_html=True)
                    elif match_score >= 60:
                        st.markdown('<div class="warning-box"><strong>Good Match</strong><br>Some improvements could strengthen your application.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-box"><strong>Needs Improvement</strong><br>Consider addressing the gaps shown below.</div>', unsafe_allow_html=True)
                    
                    st.divider()
                    
                    # Missing Keywords
                    if missing_keywords:
                        st.markdown("### Missing Keywords")
                        st.write("Consider adding these keywords from the job description:")
                        
                        cols = st.columns(3)
                        for idx, keyword in enumerate(missing_keywords[:15]):
                            with cols[idx % 3]:
                                st.write(f"- {keyword}")
                    
                except Exception as e:
                    st.markdown(f'<div class="error-box">Match calculation failed: {str(e)}</div>', unsafe_allow_html=True)
    else:
        st.info("Paste a job description above to analyze the match")

# ============================================================================
# PAGE: SETTINGS
# ============================================================================

elif st.session_state.current_page == "Settings":
    st.title("Settings")
    
    st.markdown("### Analysis Weights")
    st.write("Adjust the importance of each scoring factor (must sum to 100)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ats_weight = st.slider("ATS Compatibility Weight", 0, 50, st.session_state.settings['ats_weight'])
        skill_weight = st.slider("Skill Match Weight", 0, 50, st.session_state.settings['skill_weight'])
    
    with col2:
        exp_weight = st.slider("Experience Weight", 0, 50, st.session_state.settings['experience_weight'])
        edu_weight = st.slider("Education Weight", 0, 50, st.session_state.settings['education_weight'])
    
    total_weight = ats_weight + skill_weight + exp_weight + edu_weight
    
    if total_weight == 100:
        st.success(f"Total Weight: {total_weight}%")
    else:
        st.warning(f"Total Weight: {total_weight}% (should be 100%)")
    
    st.divider()
    
    st.markdown("### Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_industry = st.selectbox(
            "Target Industry",
            ["Technology", "Finance", "Healthcare", "Sales", "Marketing", "Engineering", "Other"]
        )
    
    with col2:
        file_size_limit = st.selectbox("Maximum File Size (MB)", [5, 10, 25])
    
    st.divider()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("SAVE SETTINGS", use_container_width=True, type="primary"):
            st.session_state.settings = {
                'ats_weight': ats_weight,
                'skill_weight': skill_weight,
                'experience_weight': exp_weight,
                'education_weight': edu_weight,
                'target_industry': target_industry,
                'file_size_limit': file_size_limit
            }
            st.markdown('<div class="success-box">Settings saved successfully!</div>', unsafe_allow_html=True)
            st.balloons()

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 20px;">
    <p><strong>AI Resume Analyzer 2.0.0</strong></p>
    <p>Built with Python, Streamlit, SpaCy, and Scikit-learn</p>
</div>
""", unsafe_allow_html=True)
