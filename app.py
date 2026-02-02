"""
AI Resume Analyzer - Professional Resume Analysis Tool
Comprehensive AI-powered analysis with honest feedback
"""

import streamlit as st
from streamlit_option_menu import option_menu
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from resume_analyzer import ResumeAnalyzer
from pdf_extractor import extract_text_from_pdf, extract_text_from_docx
from keyword_matcher import calculate_match_score, extract_missing_keywords, get_keyword_suggestions

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def get_analyzer() -> ResumeAnalyzer:
    return ResumeAnalyzer()

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Dynamic CSS based on theme
if st.session_state.dark_mode:
    # Dark Mode Colors
    theme_css = """
<style>
    /* Dark Mode Colors */
    :root {
        --primary-blue: #3B82F6;
        --primary-blue-dark: #2563EB;
        --primary-blue-light: #60A5FA;
        --success-green: #34D399;
        --success-green-light: #6EE7B7;
        --warning-amber: #FBBF24;
        --error-red: #F87171;
        --text-primary: #F9FAFB;
        --text-secondary: #D1D5DB;
        --bg-light: #1F2937;
        --bg-card: #374151;
        --border-light: #4B5563;
    }
    
    body {
        background-color: #111827 !important;
        color: #F9FAFB !important;
    }
    
    .stApp {
        background-color: #111827 !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1F2937 0%, #111827 100%) !important;
    }
"""
else:
    # Light Mode Colors
    theme_css = """
<style>
    /* Light Mode Colors */
    :root {
        --primary-blue: #2563EB;
        --primary-blue-dark: #1E40AF;
        --primary-blue-light: #3B82F6;
        --success-green: #10B981;
        --success-green-light: #34D399;
        --warning-amber: #F59E0B;
        --error-red: #EF4444;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --bg-light: #F9FAFB;
        --bg-card: #FFFFFF;
        --border-light: #E5E7EB;
    }
    
    body {
        background-color: #F9FAFB !important;
        color: #1F2937 !important;
    }
    
    .stApp {
        background-color: #F9FAFB !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F9FAFB 0%, #F3F4F6 100%) !important;
    }
"""

st.markdown(theme_css + """
    /* ========================================
       PROFESSIONAL DESIGN SYSTEM
       ======================================== */
    
    /* TYPOGRAPHY */
    h1 { font-size: 3rem; font-weight: 800; color: #1F2937; letter-spacing: -0.5px; margin: 0 0 1rem 0; }
    h2 { font-size: 2.25rem; font-weight: 700; color: #1F2937; margin: 2rem 0 1rem 0; }
    h3 { font-size: 1.5rem; font-weight: 600; color: #1F2937; margin: 1.5rem 0 0.75rem 0; }
    h4 { font-size: 1.25rem; font-weight: 600; color: #6B7280; margin: 1rem 0 0.5rem 0; }
    
    p { font-size: 1rem; font-weight: 400; color: #6B7280; line-height: 1.6; margin: 0.5rem 0; }
    
    small { font-size: 0.875rem; font-weight: 400; color: #9CA3AF; }
    
    /* SPACING SCALE (8px base) */
    .spacing-xs { margin: 4px; }
    .spacing-sm { margin: 8px; }
    .spacing-md { margin: 16px; }
    .spacing-lg { margin: 24px; }
    .spacing-xl { margin: 32px; }
    .spacing-2xl { margin: 48px; }
    .spacing-3xl { margin: 64px; }
    
    /* HERO HEADER */
    .header-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        color: white;
        padding: 4rem 2rem;
        margin-bottom: 3rem;
        text-align: center;
        box-shadow: 0 10px 15px rgba(37, 99, 235, 0.15);
        border-radius: 12px;
        animation: fadeIn 0.5s ease;
    }
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        padding: 0;
        color: #FFFFFF;
        letter-spacing: -0.5px;
        text-transform: none;
    }
    .header-subtitle {
        font-size: 1.25rem;
        opacity: 0.95;
        margin: 0.75rem 0 0 0;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
    }
    
    /* FEATURE CARDS */
    .feature-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        padding: 2rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 2px solid #E5E7EB;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 25px rgba(37, 99, 235, 0.15);
        border-color: #2563EB;
    }
    .feature-card h3 {
        color: #2563EB !important;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 1rem 0 0.5rem 0;
    }
    .feature-card p {
        color: #6B7280 !important;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0;
    }
    
    /* STATUS BOXES */
    .info-box {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #2563EB;
        margin: 1.5rem 0;
        color: #1F2937;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #F0FDF4 0%, #DBEAFE 100%);
        border-left-color: #10B981;
        box-shadow: 0 2px 6px rgba(16, 185, 129, 0.1);
    }
    .warning-box {
        background: linear-gradient(135deg, #FEF9E7 0%, #FEF08A 100%);
        border-left-color: #F59E0B;
        box-shadow: 0 2px 6px rgba(245, 158, 11, 0.1);
    }
    .error-box {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-left-color: #EF4444;
        box-shadow: 0 2px 6px rgba(239, 68, 68, 0.1);
    }
    
    /* STATISTICS CARDS */
    .stat-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
        padding: 2rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    }
    .stat-number {
        font-size: 2.25rem;
        font-weight: 800;
        color: #2563EB !important;
        margin: 0.75rem 0;
    }
    .stat-label {
        font-size: 0.875rem;
        color: #6B7280 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.75px;
    }
    
    /* STEP BOXES */
    .step-box {
        background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #2563EB;
        text-align: left;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .step-box:hover {
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
    }
    .step-number {
        display: inline-block;
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        color: white;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        line-height: 44px;
        text-align: center;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
    }
    .step-title {
        font-weight: 700;
        color: #1F2937 !important;
        font-size: 1.125rem;
        margin: 0.75rem 0;
    }
    .step-description {
        font-size: 0.9rem;
        color: #6B7280 !important;
        margin: 0.5rem 0 0 0;
        line-height: 1.6;
    }
    
    /* BUTTONS */
    .stButton > button {
        background-color: #2563EB !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2) !important;
        font-size: 1rem !important;
    }
    .stButton > button:hover {
        background-color: #1E40AF !important;
        box-shadow: 0 8px 12px rgba(37, 99, 235, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    .stButton > button:active {
        background-color: #1D4ED8 !important;
        transform: translateY(0) !important;
    }
    
    /* FILE UPLOADER */
    .stFileUploader label {
        color: #1F2937 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    .stFileUploader > div > div {
        border: 3px dashed #2563EB !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%) !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    .stFileUploader > div > div:hover {
        border-color: #1E40AF !important;
        background: linear-gradient(135deg, #E0F2FE 0%, #D0E7FC 100%) !important;
    }
    
    /* INPUTS */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 2px solid #E5E7EB !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] button {
        color: #6B7280 !important;
        font-weight: 500 !important;
        border-bottom: 3px solid transparent !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #2563EB !important;
        border-bottom: 3px solid #2563EB !important;
        font-weight: 700 !important;
    }
    
    /* METRICS */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%) !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
    }
    [data-testid="metric-container"] > div > div > div:first-child {
        color: #6B7280 !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.75px !important;
    }
    [data-testid="metric-container"] > div > div > div:last-child {
        color: #2563EB !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    
    /* SECTION HEADING */
    .section-heading {
        font-size: 2rem;
        font-weight: 800;
        color: #1F2937;
        margin: 3rem 0 2rem 0;
        padding-bottom: 1rem;
        border-bottom: 3px solid #2563EB;
    }
    
    /* FOOTER */
    .footer-container {
        text-align: center;
        color: #6B7280;
        font-size: 0.875rem;
        padding: 3rem 2rem;
        border-top: 2px solid #E5E7EB;
        margin-top: 4rem;
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .footer-links a {
        color: #2563EB;
        text-decoration: none;
        margin: 0 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .footer-links a:hover {
        color: #1E40AF;
        text-decoration: underline;
    }
    
    /* ANIMATIONS */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .stMetric { animation: slideUp 0.5s ease-out; }
    
    /* RESPONSIVE */
    @media (max-width: 768px) {
        .header-title { font-size: 2rem; }
        .section-heading { font-size: 1.5rem; }
        h2 { font-size: 1.75rem; }
        .stat-number { font-size: 1.75rem; }
        .step-number { width: 36px; height: 36px; line-height: 36px; }
    }
    
    /* UTILITIES */
    .divider { border-top: 2px solid #E5E7EB; margin: 2rem 0; }
    .highlight { background: linear-gradient(120deg, #FEF08A, #FBBF24); padding: 0.25rem 0.5rem; border-radius: 4px; }

    
    /* Metric Cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%) !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 0.75rem !important;
        padding: 1.5rem !important;
    }
    [data-testid="metric-container"] > div > div > div:first-child {
        color: #6B7280 !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    [data-testid="metric-container"] > div > div > div:last-child {
        color: #2563EB !important;
    
    # Theme Toggle
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️", help="Toggle theme"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.markdown("---")
    
    selected_page = option_menu(
        menu_title=None,
        options=["Home", "Upload Resume", "Analysis", "Job Matching", "ATS Check", "About"],
        icons=["house", "upload", "bar-chart", "target", "checkbox", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#F8FAFC" if not st.session_state.dark_mode else "#1F2937"},
            "icon": {"color": "#2563EB" if not st.session_state.dark_mode else "#3B82F6", "font-size": "20px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "color": "#1F2937" if not st.session_state.dark_mode else "#F9FAFB
        background: linear-gradient(135deg, #FEF9E7 0%, #FEF08A 100%) !important;
        border: 1px solid #F59E0B !important;
        border-left: 4px solid #F59E0B !important;
        color: #1F2937 !important;
    }
    .stError {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%) !important;
        border: 1px solid #EF4444 !important;
        border-left: 4px solid #EF4444 !important;
        color: #1F2937 !important;
    }
    .stInfo {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%) !important;
        border: 1px solid #2563EB !important;
        border-left: 4px solid #2563EB !important;
        color: #1F2937 !important;
    }
    
    /* Expander */
    .streamlit-expander {
        border: 1px solid #E5E7EB !important;
        border-radius: 0.5rem !important;
    }
    .streamlit-expanderContent {
        padding: 1rem !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F9FAFB 0%, #F3F4F6 100%) !important;
    }
    

</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### AI Resume Analyzer")
    st.markdown("---")
    
    selected_page = option_menu(
        menu_title=None,
        options=["Home", "Upload Resume", "Analysis", "Job Matching", "ATS Check", "About"],
        icons=["house", "upload", "bar-chart", "target", "checkbox", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#F8FAFC"},
            "icon": {"color": "#2563EB", "font-size": "20px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#2563EB", "color": "white"},
        }
    )
    
    st.markdown("---")
    if st.session_state.analysis_results:
        sidebar_scores = st.session_state.analysis_results.get('scores', {})
        st.metric("Overall Score", f"{sidebar_scores.get('overall_score', 0):.0f}%")


def show_home_page():
    """Home page"""
    st.markdown('<div class="header-container"><h1 class="header-title">Transform Your Resume</h1><p class="header-subtitle">Professional AI-powered analysis with honest feedback</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Upload Resume", use_container_width=True):
            st.session_state.page = 'upload'
            st.rerun()
    with col2:
        if st.button("See Analysis", use_container_width=True):
            if st.session_state.analysis_results:
                st.session_state.page = 'analysis'
                st.rerun()
    with col3:
        if st.button("Learn More", use_container_width=True):
            st.session_state.page = 'about'
            st.rerun()
    
    st.markdown("---")
    st.markdown("<h2 class='section-heading' style='color: #2563EB !important;'>✨ Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown('<div class="feature-card"><div style="font-size: 3rem; margin-bottom: 1rem;">📊</div><h3 style="color: #2563EB !important; margin: 0.5rem 0;">Content Quality</h3><p style="color: #6B7280 !important;">Analyze word count, action verbs, and impact of achievements</p></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card"><div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div><h3 style="color: #2563EB !important; margin: 0.5rem 0;">Skills Detection</h3><p style="color: #6B7280 !important;">Extract technical and soft skills automatically</p></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="feature-card"><div style="font-size: 3rem; margin-bottom: 1rem;">✅</div><h3 style="color: #2563EB !important; margin: 0.5rem 0;">ATS Compatible</h3><p style="color: #6B7280 !important;">Ensure your resume passes Applicant Tracking Systems</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown('<div class="feature-card"><div style="font-size: 3rem; margin-bottom: 1rem;">📐</div><h3 style="color: #2563EB !important; margin: 0.5rem 0;">Structure Review</h3><p style="color: #6B7280 !important;">Check organization and document structure</p></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card"><div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div><h3 style="color: #2563EB !important; margin: 0.5rem 0;">Job Matching</h3><p style="color: #6B7280 !important;">Compare against job descriptions</p></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="feature-card"><div style="font-size: 3rem; margin-bottom: 1rem;">📈</div><h3 style="color: #2563EB !important; margin: 0.5rem 0;">Detailed Reports</h3><p style="color: #6B7280 !important;">Get comprehensive analysis with actionable insights</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h2 class='section-heading' style='color: #2563EB !important;'>🚀 How It Works</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown("""
        <div class="step-box">
            <div class="step-number">1</div>
            <div style="font-size: 2.5rem; margin: 1rem 0;">📤</div>
            <div class="step-title">Upload</div>
            <div class="step-description">Choose your resume in PDF, DOCX, or TXT format</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="step-box">
            <div class="step-number">2</div>
            <div style="font-size: 2.5rem; margin: 1rem 0;">🤖</div>
            <div class="step-title">Analyze</div>
            <div class="step-description">We analyze across 5 core dimensions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="step-box">
            <div class="step-number">3</div>
            <div style="font-size: 2.5rem; margin: 1rem 0;">📋</div>
            <div class="step-title">Review</div>
            <div class="step-description">Get detailed scores and recommendations</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="step-box">
            <div class="step-number">4</div>
            <div style="font-size: 2.5rem; margin: 1rem 0;">⬆️</div>
            <div class="step-title">Improve</div>
            <div class="step-description">Implement changes and re-upload</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h2 class='section-heading' style='color: #2563EB !important;'>📈 Key Highlights</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Processing Mode</div>
            <div class="stat-number">Local</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Scoring Model</div>
            <div class="stat-number">Transparent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Analysis Time</div>
            <div class="stat-number">File Dependent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Cost</div>
            <div class="stat-number">Free</div>
        </div>
        """, unsafe_allow_html=True)


def show_upload_page():
    """Upload page"""
    st.markdown("<h2 style='color: #1F2937;'>📤 Upload Your Resume</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h3 style='color: #1F2937;'>Submit Your Resume</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #6B7280;'>Our AI will analyze your resume for:</p>", unsafe_allow_html=True)
        st.markdown("<div style='color: #6B7280;'><li>Content quality and impact</li><li>Keyword optimization</li><li>ATS compatibility</li><li>Skills detection</li><li>Structure review</li></div>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose resume", type=["pdf", "docx", "txt"])
        
        if uploaded_file:
            st.success(f"File selected: {uploaded_file.name}")
            st.info(f"Size: {uploaded_file.size / 1024:.1f} KB")

            if st.button("Analyze Resume", use_container_width=True):
                with st.spinner("Analyzing..."):
                    try:
                        if uploaded_file.type == "application/pdf":
                            resume_text = extract_text_from_pdf(uploaded_file)
                        elif "wordprocessingml" in uploaded_file.type:
                            resume_text = extract_text_from_docx(uploaded_file)
                        else:
                            resume_text = uploaded_file.getvalue().decode("utf-8", errors="ignore")

                        if resume_text.startswith("Error"):
                            st.error(resume_text)
                            return

                        analyzer = get_analyzer()
                        results = analyzer.analyze(resume_text)

                        st.session_state.resume_data = {
                            'text': resume_text,
                            'filename': uploaded_file.name,
                            'file_type': uploaded_file.type
                        }
                        st.session_state.analysis_results = results

                        st.success("Analysis complete!")
                        st.session_state.page = 'analysis'
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("<h3 style='color: #1F2937;'>Formats Supported</h3>", unsafe_allow_html=True)
        st.markdown("<div style='color: #6B7280;'><li>PDF (.pdf)</li><li>Word (.docx)</li><li>Text (.txt)</li></div>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='color: #1F2937;'>Requirements</h3>", unsafe_allow_html=True)
        st.markdown("<div style='color: #6B7280;'><li>Max: 10 MB</li><li>Readable text</li><li>Clear formatting</li></div>", unsafe_allow_html=True)


def show_analysis_page():
    """Analysis page"""
    st.markdown("<h2 style='color: #1F2937;'>📊 Analysis Results</h2>", unsafe_allow_html=True)
    
    if not st.session_state.analysis_results:
        st.warning("Upload a resume first")
        if st.button("Upload Resume"):
            st.session_state.page = 'upload'
            st.rerun()
        return
    
    results = st.session_state.analysis_results
    scores = results.get('scores', {})

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Score", f"{scores.get('overall_score', 0):.0f}%")
    with col2:
        st.metric("Content Quality", f"{scores.get('content_quality', 0):.0f}%")
    with col3:
        st.metric("Keyword Optimization", f"{scores.get('keyword_optimization', 0):.0f}%")
    with col4:
        st.metric("ATS Score", f"{scores.get('ats_compatibility', 0):.0f}%")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Content", "Skills", "Recommendations", "Details"])
    
    with tab1:
        st.markdown("<h3 style='color: #1F2937;'>Content Analysis</h3>", unsafe_allow_html=True)
        st.markdown(f"<div style='color: #6B7280;'><strong>Word Count:</strong> {results.get('word_count', 0)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color: #6B7280;'><strong>Action Verbs:</strong> {results.get('action_verbs_count', 0)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color: #6B7280;'><strong>Sections Found:</strong> {len(results.get('sections_detected', []))}</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<h3 style='color: #1F2937;'>Detected Skills</h3>", unsafe_allow_html=True)
        skills = {
            'technical': results.get('technical_skills', []),
            'soft': results.get('soft_skills', [])
        }
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4 style='color: #1F2937;'>Technical</h4>", unsafe_allow_html=True)
            tech_list = "".join([f"<li>{skill}</li>" for skill in skills.get('technical', [])[:10]])
            st.markdown(f"<div style='color: #6B7280;'><ul>{tech_list}</ul></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h4 style='color: #1F2937;'>Soft</h4>", unsafe_allow_html=True)
            soft_list = "".join([f"<li>{skill}</li>" for skill in skills.get('soft', [])[:10]])
            st.markdown(f"<div style='color: #6B7280;'><ul>{soft_list}</ul></div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<h3 style='color: #1F2937;'>Recommendations</h3>", unsafe_allow_html=True)
        recs_html = "".join([f"<li>{rec}</li>" for rec in results.get('recommendations', [])[:5]])
        st.markdown(f"<div style='color: #6B7280;'><ol>{recs_html}</ol></div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("<h3 style='color: #1F2937;'>Technical Details</h3>", unsafe_allow_html=True)
        st.json({
            "overall_score": f"{scores.get('overall_score', 0):.1f}%",
            "content_quality": f"{scores.get('content_quality', 0):.1f}%",
            "keyword_optimization": f"{scores.get('keyword_optimization', 0):.1f}%",
            "ats_compatibility": f"{scores.get('ats_compatibility', 0):.1f}%",
            "structure_score": f"{scores.get('structure_score', 0):.1f}%",
            "completeness": f"{scores.get('completeness', 0):.1f}%"
        })


def show_job_matching_page():
    """Job matching page"""
    st.markdown("<h2 style='color: #1F2937;'>🎯 Job Description Matching</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color: #6B7280; margin-bottom: 1rem;'>Paste a job description to see how well your resume matches:</div>", unsafe_allow_html=True)
    
    if not st.session_state.resume_data:
        st.warning("Upload a resume first")
        if st.button("Upload Resume"):
            st.session_state.page = 'upload'
            st.rerun()
        return
    
    job_description = st.text_area("Paste Job Description", height=200)
    
    if st.button("Analyze Match"):
        if job_description:
            resume_text = st.session_state.resume_data.get('text', '')
            with st.spinner("Analyzing job match..."):
                match_score = calculate_match_score(resume_text, job_description)
                missing_keywords = extract_missing_keywords(resume_text, job_description)
                suggestions = get_keyword_suggestions(job_description)

            st.metric("Match Score", f"{match_score}%")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Missing Keywords (Top 10)**")
                if missing_keywords:
                    st.markdown("<ul>" + "".join([f"<li>{k}</li>" for k in missing_keywords]) + "</ul>", unsafe_allow_html=True)
                else:
                    st.success("No critical keywords missing.")

            with col2:
                st.markdown("**Suggested Keywords**")
                st.markdown("**Technical:** " + ", ".join(suggestions.get('technical_skills', [])) if suggestions.get('technical_skills') else "**Technical:** None detected")
                st.markdown("**Soft Skills:** " + ", ".join(suggestions.get('soft_skills', [])) if suggestions.get('soft_skills') else "**Soft Skills:** None detected")
                st.markdown("**Action Verbs:** " + ", ".join(suggestions.get('action_verbs', [])) if suggestions.get('action_verbs') else "**Action Verbs:** None detected")
        else:
            st.warning("Please enter a job description")


def show_ats_check_page():
    """ATS check page"""
    st.markdown("<h2 style='color: #1F2937;'>✓ ATS Compatibility Check</h2>", unsafe_allow_html=True)
    
    if not st.session_state.analysis_results:
        st.warning("Upload a resume first")
        if st.button("Upload Resume"):
            st.session_state.page = 'upload'
            st.rerun()
        return
    
    results = st.session_state.analysis_results
    scores = results.get('scores', {})
    contact_info = results.get('contact_info', {})
    sections = set(results.get('sections_detected', []))

    st.metric("ATS Compatibility", f"{scores.get('ats_compatibility', 0):.0f}%")

    required_sections = {"Experience", "Education", "Skills", "Summary"}
    missing_sections = sorted(list(required_sections - sections))

    missing_contact = []
    if not contact_info.get('has_email'):
        missing_contact.append("Email")
    if not contact_info.get('has_phone'):
        missing_contact.append("Phone")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='color: #10B981;'>✓ Good Practices</h3>", unsafe_allow_html=True)
        good_items = [
            "Clear section headers",
            "Readable text and spacing",
            "Standard bullet points",
            "Consistent date formatting"
        ]
        st.markdown("<div style='color: #6B7280;'><ul>" + "".join([f"<li>{i}</li>" for i in good_items]) + "</ul></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='color: #EF4444;'>✗ Missing or Risk Areas</h3>", unsafe_allow_html=True)
        risk_items = []
        if missing_sections:
            risk_items.append("Missing sections: " + ", ".join(missing_sections))
        if missing_contact:
            risk_items.append("Missing contact: " + ", ".join(missing_contact))
        if not risk_items:
            risk_items.append("No major ATS risks detected.")
        st.markdown("<div style='color: #6B7280;'><ul>" + "".join([f"<li>{i}</li>" for i in risk_items]) + "</ul></div>", unsafe_allow_html=True)


def show_about_page():
    """About page"""
    st.markdown("<h2 style='color: #1F2937;'>ℹ️ About AI Resume Analyzer</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <h3 style='color: #1F2937;'>What is AI Resume Analyzer?</h3>
    <div style='color: #6B7280; line-height: 1.6;'>AI Resume Analyzer is a professional resume analysis tool that provides honest, actionable feedback to help you improve your resume and land your dream job.</div>
    
    <h3 style='color: #1F2937; margin-top: 2rem;'>Features</h3>
    <div style='color: #6B7280;'><ul>
    <li>Content Quality Analysis</li>
    <li>Skill Detection</li>
    <li>ATS Compatibility Check</li>
    <li>Job Matching</li>
    <li>Structure Review</li>
    <li>Actionable Recommendations</li>
    </ul></div>
    
    <h3 style='color: #1F2937; margin-top: 2rem;'>How It Works</h3>
    <div style='color: #6B7280;'><ol>
    <li>Upload your resume (PDF, DOCX, or TXT)</li>
    <li>The analyzer evaluates content, keywords, ATS, structure, and completeness</li>
    <li>You get instant, honest feedback</li>
    <li>Implement recommendations</li>
    <li>Re-upload to see improvements</li>
    </ol></div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Upload Resume", use_container_width=True):
            st.session_state.page = 'upload'
            st.rerun()
    
    with col2:
        if st.button("View Features", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()


# Main routing
if selected_page == "Home":
    show_home_page()
elif selected_page == "Upload Resume":
    show_upload_page()
elif selected_page == "Analysis":
    show_analysis_page()
elif selected_page == "Job Matching":
    show_job_matching_page()
elif selected_page == "ATS Check":
    show_ats_check_page()
elif selected_page == "About":
    show_about_page()

# Footer
st.markdown("---")
st.markdown("""
<div class="footer-container">
    <p style="margin: 0.5rem 0; font-weight: 600; color: #1F2937;">© 2026 AI Resume Analyzer</p>
    <p style="margin: 0.5rem 0; color: #6B7280;">Professional resume analysis powered by NLP and rules</p>
    <div class="footer-links" style="margin-top: 1rem;">
        <a href="#">Privacy Policy</a> |
        <a href="#">Terms of Service</a> |
        <a href="#">Contact Support</a> |
        <a href="https://github.com/Crewjah/AI-Resume-Analyzer" target="_blank">GitHub</a>
    </div>
    <p style="margin: 1rem 0 0 0; font-size: 0.8rem; color: #9CA3AF;">Built with dedication to help you succeed</p>
</div>
""", unsafe_allow_html=True)
