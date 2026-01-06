import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from backend.resume_analyzer import ResumeAnalyzer
from backend.pdf_extractor import extract_text_from_pdf
from backend.keyword_matcher import calculate_match_score, extract_missing_keywords
import time
import json
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="AI Resume Analyzer - Professional Career Optimizer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS WITH ANIMATIONS & MODERN DESIGN
# ============================================================================
st.markdown("""
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Global Styling */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main > div {
        padding: 2rem 1.5rem;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    #MainMenu, footer, .stDeployButton {
        display: none !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2563EB 0%, #1E40AF 100%);
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] .sidebar-content {
        color: white;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: white !important;
    }
    
    /* Header with Animation */
    .header-container {
        background: linear-gradient(135deg, #2563EB 0%, #0891B2 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(37, 99, 235, 0.3);
        animation: fadeIn 0.8s ease-in;
    }
    
    .header-container h1 {
        font-size: 2.8rem;
        font-weight: 800;
        color: white;
        margin: 0 0 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-container p {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.95);
        margin: 0;
    }
    
    /* Score Cards with Hover Effect */
    .score-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        animation: slideUp 0.5s ease-out;
    }
    
    .score-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.2);
    }
    
    .score-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2563EB, #0891B2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .score-label {
        font-size: 0.9rem;
        color: #6B7280;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Content Box */
    .content-box {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .content-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* Skill Badge */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, #2563EB 0%, #0891B2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);
        transition: transform 0.2s;
    }
    
    .skill-badge:hover {
        transform: scale(1.05);
    }
    
    /* Insight Box */
    .insight-box {
        background: #F9FAFB;
        border-left: 4px solid #2563EB;
        padding: 1rem 1.5rem;
        margin: 0.75rem 0;
        border-radius: 6px;
        animation: fadeIn 0.5s ease-in;
    }
    
    .insight-box strong {
        color: #2563EB;
    }
    
    /* File Uploader Styling */
    [data-testid="stFileUploader"] > div > div {
        background: white;
        border: 3px dashed #2563EB;
        border-radius: 12px;
        padding: 2rem !important;
        transition: all 0.3s;
    }
    
    [data-testid="stFileUploader"] > div > div:hover {
        border-color: #0891B2;
        background: #F0F9FF;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #0891B2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
    }
    
    /* Progress Bar Animation */
    .progress-fill {
        animation: fillBar 2s ease-out;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fillBar {
        from { width: 0; }
        to { width: 100%; }
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #F3F4F6;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563EB 0%, #0891B2 100%);
        color: white;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #2563EB;
    }
    
    /* Icon Styles */
    .icon {
        margin-right: 0.5rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #F9FAFB;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Dataframe */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Toast Messages */
    .stAlert {
        border-radius: 8px;
        animation: fadeIn 0.3s ease-in;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'threshold': 70,
        'industry': 'Technology',
        'show_json': False,
        'weights': {
            'content': 30,
            'keywords': 25,
            'ats': 25,
            'structure': 20
        }
    }

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h2 style='color: white; font-size: 1.5rem; margin: 0;'>
            <i class='fas fa-file-alt'></i> AI Resume Analyzer
        </h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 0.85rem; margin: 0.5rem 0 0 0;'>
            Career Optimizer v2.0
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation Menu
    page = st.radio(
        "Navigation",
        ["📤 Upload & Analyze", "📊 Results Dashboard", "🎯 Job Matching", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Help Section
    with st.expander("📚 Help & Resources"):
        st.markdown("""
        **File Requirements:**
        - Max size: 5 MB
        - Formats: PDF, TXT
        
        **Sample Resume:**
        [Download Sample](javascript:void(0))
        
        **Need Help?**
        Check our [Guide](javascript:void(0))
        """)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: rgba(255,255,255,0.6); font-size: 0.75rem; padding: 1rem 0;'>
        v2.0.0<br>
        Built with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE: UPLOAD & ANALYZE
# ============================================================================
if page == "📤 Upload & Analyze":
    # Header
    st.markdown("""
    <div class="header-container">
        <h1><i class="fas fa-upload icon"></i> Upload Your Resume</h1>
        <p>Get instant AI-powered analysis with actionable insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Single Upload Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Drop your resume files here or click to browse",
            type=['pdf', 'txt'],
            accept_multiple_files=True,
            help="Upload one or more resume files (PDF or TXT, max 5MB each)",
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            
            # File Preview with Remove Options
            st.markdown("### 📁 Selected Files")
            
            files_to_remove = []
            for idx, file in enumerate(uploaded_files):
                col_file, col_info, col_action = st.columns([3, 2, 1])
                
                with col_file:
                    st.markdown(f"**{file.name}**")
                
                with col_info:
                    file_valid = file.size < 5*1024*1024  # 5MB limit
                    size_text = f"{file.size/1024:.1f} KB"
                    if file_valid:
                        st.markdown(f"✅ {size_text}")
                    else:
                        st.markdown(f"❌ {size_text} (Too large)")
                
                with col_action:
                    if st.button("🗑️", key=f"remove_{idx}", help="Remove file"):
                        files_to_remove.append(file)
            
            st.markdown("---")
    
    with col2:
        st.markdown("""
        <div style='background: #F0F9FF; border-radius: 12px; padding: 1.5rem; border: 2px solid #2563EB;'>
            <h3 style='color: #2563EB; margin-top: 0; font-size: 1.1rem;'>
                <i class='fas fa-info-circle'></i> Requirements
            </h3>
            <div style='color: #1F2937; font-size: 0.9rem; line-height: 1.6;'>
                <strong>Formats:</strong> PDF, TXT<br>
                <strong>Max Size:</strong> 5 MB per file<br>
                <strong>Quality:</strong> Clear, readable text<br>
                <strong>Structure:</strong> Standard resume format
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Workflow Steps
        st.markdown("""
        <div style='background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
            <h3 style='color: #1F2937; margin-top: 0; font-size: 1.1rem;'>
                📋 Next Steps
            </h3>
            <div style='color: #6B7280; font-size: 0.85rem; line-height: 1.8;'>
                <strong>1.</strong> Upload your resume(s)<br>
                <strong>2.</strong> Click "Analyze Now"<br>
                <strong>3.</strong> View detailed results<br>
                <strong>4.</strong> Download report
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Analysis Button - Only show if files uploaded
    if uploaded_files:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Count valid files
        valid_files = [f for f in uploaded_files if f.size < 5*1024*1024]
        
        if valid_files:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                analyze_button = st.button(
                    f"🚀 Analyze {len(valid_files)} Resume{'s' if len(valid_files) > 1 else ''} Now",
                    use_container_width=True,
                    type="primary",
                    key="analyze_main"
                )
            
            if analyze_button:
                # Progress tracking
                progress_container = st.container()
                
                with progress_container:
                    st.markdown("### 🔄 Analysis in Progress")
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, file in enumerate(valid_files):
                        status_text.markdown(f"📄 Analyzing **{file.name}**...")
                        
                        # Extract Text
                        if file.type == "application/pdf":
                            resume_text = extract_text_from_pdf(file)
                        else:
                            resume_text = file.read().decode('utf-8')
                        
                        if resume_text and resume_text.strip():
                            # Analyze
                            analyzer = ResumeAnalyzer()
                            analysis = analyzer.analyze(resume_text)
                            
                            if analysis and 'scores' in analysis:
                                st.session_state.analysis_results[file.name] = analysis
                        
                        # Update progress
                        progress_bar.progress((idx + 1) / len(valid_files))
                        time.sleep(0.3)
                    
                    status_text.empty()
                    progress_bar.empty()
                
                # Success with balloons!
                st.balloons()
                
                st.success(f"""
                ✅ **Analysis Complete!**
                
                Successfully analyzed {len(valid_files)} resume{'s' if len(valid_files) > 1 else ''}. 
                Navigate to **Results Dashboard** to view detailed insights.
                """)
                
                # Auto-redirect button
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("📊 View Results →", use_container_width=True, type="primary"):
                        st.session_state.current_page = "📊 Results Dashboard"
                        st.rerun()
        else:
            st.error("❌ No valid files to analyze. Please ensure files are under 5MB.")
    else:
        # No files uploaded - Show instructions
        st.markdown("""
        <div style='background: white; border-radius: 16px; padding: 2.5rem; margin-top: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.08);'>
            <h2 style='color: #1F2937; text-align: center; margin-top: 0;'>
                👆 Get Started
            </h2>
            <p style='color: #6B7280; text-align: center; font-size: 1rem; line-height: 1.8;'>
                Upload your resume above to receive instant, AI-powered analysis including:
            </p>
            <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; margin-top: 2rem;'>
                <div style='text-align: center;'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>📊</div>
                    <strong style='color: #2563EB;'>Detailed Scoring</strong>
                    <p style='color: #6B7280; font-size: 0.85rem; margin: 0.5rem 0 0 0;'>
                        Get scores for content, keywords, ATS compatibility & more
                    </p>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>💼</div>
                    <strong style='color: #2563EB;'>Skills Analysis</strong>
                    <p style='color: #6B7280; font-size: 0.85rem; margin: 0.5rem 0 0 0;'>
                        Identify technical and soft skills automatically
                    </p>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>💡</div>
                    <strong style='color: #2563EB;'>Smart Insights</strong>
                    <p style='color: #6B7280; font-size: 0.85rem; margin: 0.5rem 0 0 0;'>
                        Receive actionable improvement recommendations
                    </p>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🎯</div>
                    <strong style='color: #2563EB;'>Job Matching</strong>
                    <p style='color: #6B7280; font-size: 0.85rem; margin: 0.5rem 0 0 0;'>
                        Compare your resume against job descriptions
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE: RESULTS DASHBOARD
# ============================================================================
elif page == "📊 Results Dashboard":
    st.markdown("""
    <div class="header-container">
        <h1><i class="fas fa-chart-bar icon"></i> Analysis Results</h1>
        <p>Comprehensive resume analysis dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.analysis_results:
        st.warning("⚠️ No analysis results yet. Please upload and analyze resumes first.")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📤 Go to Upload", use_container_width=True, type="primary"):
                st.rerun()
    else:
        # Quick Stats Section (MOVED HERE from sidebar)
        st.markdown("### 📈 Quick Statistics")
        stat_cols = st.columns(4)
        
        with stat_cols[0]:
            st.metric("Total Resumes", len(st.session_state.analysis_results))
        
        with stat_cols[1]:
            avg_score = sum([r['scores']['overall_score'] for r in st.session_state.analysis_results.values()]) / len(st.session_state.analysis_results)
            st.metric("Average Score", f"{avg_score:.1f}%")
        
        with stat_cols[2]:
            max_score = max([r['scores']['overall_score'] for r in st.session_state.analysis_results.values()])
            st.metric("Highest Score", f"{max_score}%")
        
        with stat_cols[3]:
            total_skills = sum([len(r.get('technical_skills', [])) for r in st.session_state.analysis_results.values()])
            st.metric("Total Skills", total_skills)
        
        st.markdown("---")
        
        # Select Resume
        resume_names = list(st.session_state.analysis_results.keys())
        selected_resume = st.selectbox(
            "**📄 Select Resume to View:**",
            resume_names,
            index=0
        )
        
        analysis = st.session_state.analysis_results[selected_resume]
        scores = analysis['scores']
        
        st.markdown("---")
        
        # Score Cards Row
        st.markdown("### 📊 Score Overview")
        cards = st.columns(5)
        
        score_data = [
            ("Overall", scores.get("overall_score", 0), "fa-star"),
            ("Content", scores.get("content_quality", 0), "fa-file-alt"),
            ("Keywords", scores.get("keyword_optimization", 0), "fa-key"),
            ("ATS", scores.get("ats_compatibility", 0), "fa-robot"),
            ("Structure", scores.get("structure_score", 0), "fa-sitemap")
        ]
        
        for col, (label, val, icon) in zip(cards, score_data):
            col.metric(label, f"{val}%", delta=None)
            col.progress(min(val, 100) / 100, text=f"{label} status")
        
        st.markdown("---")
        
        # Tabs for Different Views
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Breakdown Analysis",
            "💼 Skills Detection",
            "💡 Insights & Tips",
            "📄 Summary & Export"
        ])
        
        # TAB 1: Breakdown
        with tab1:
            c1, c2 = st.columns([2, 1])
            
            with c1:
                # Radar Chart
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=[
                        scores.get('content_quality', 0),
                        scores.get('keyword_optimization', 0),
                        scores.get('ats_compatibility', 0),
                        scores.get('structure_score', 0),
                        scores.get('completeness', 0)
                    ],
                    theta=['Content', 'Keywords', 'ATS', 'Structure', 'Completeness'],
                    fill='toself',
                    line=dict(color='#2563EB', width=2),
                    fillcolor='rgba(37, 99, 235, 0.3)'
                ))
                fig.update_layout(
                    margin=dict(l=40, r=40, t=20, b=20),
                    polar=dict(radialaxis=dict(range=[0, 100])),
                    paper_bgcolor='white',
                    height=350
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Bar Chart
                comp_df = pd.DataFrame({
                    'Metric': ['Content', 'Keywords', 'ATS', 'Structure', 'Completeness'],
                    'Score': [
                        scores.get('content_quality', 0),
                        scores.get('keyword_optimization', 0),
                        scores.get('ats_compatibility', 0),
                        scores.get('structure_score', 0),
                        scores.get('completeness', 0)
                    ]
                })
                bar = px.bar(
                    comp_df,
                    x='Score',
                    y='Metric',
                    orientation='h',
                    color='Score',
                    color_continuous_scale=['#DBEAFE', '#2563EB']
                )
                bar.update_layout(margin=dict(l=80, r=20, t=10, b=10), paper_bgcolor='white')
                st.plotly_chart(bar, use_container_width=True)
            
            with c2:
                st.markdown("**Distribution**")
                # Donut Chart
                donut = go.Figure(
                    data=[go.Pie(
                        labels=['Content', 'Keywords', 'ATS', 'Structure', 'Completeness'],
                        values=[
                            scores.get('content_quality', 0),
                            scores.get('keyword_optimization', 0),
                            scores.get('ats_compatibility', 0),
                            scores.get('structure_score', 0),
                            scores.get('completeness', 0)
                        ],
                        hole=0.55,
                        marker=dict(colors=['#2563EB', '#3B82F6', '#60A5FA', '#93C5FD', '#DBEAFE'])
                    )]
                )
                donut.update_layout(
                    showlegend=True,
                    margin=dict(t=20, b=20, l=10, r=10),
                    paper_bgcolor='white'
                )
                st.plotly_chart(donut, use_container_width=True)
        
        # TAB 2: Skills
        with tab2:
            left, right = st.columns(2)
            
            with left:
                st.markdown("#### 💻 Technical Skills")
                tech = analysis.get('technical_skills', [])
                if tech:
                    st.markdown(
                        " ".join([f"<span class='skill-badge'>{s}</span>" for s in tech]),
                        unsafe_allow_html=True
                    )
                else:
                    st.info("No technical skills detected")
            
            with right:
                st.markdown("#### 🤝 Soft Skills")
                soft = analysis.get('soft_skills', [])
                if soft:
                    st.markdown(
                        " ".join([f"<span class='skill-badge'>{s}</span>" for s in soft]),
                        unsafe_allow_html=True
                    )
                else:
                    st.info("No soft skills detected")
        
        # TAB 3: Insights
        with tab3:
            st.markdown("#### 💡 Key Insights")
            
            insights = []
            if scores.get('overall_score', 0) < 70:
                insights.append(("Overall", "Boost content quality and keyword density."))
            if scores.get('content_quality', 0) < 60:
                insights.append(("Content", "Use action verbs and quantify achievements."))
            if scores.get('keyword_optimization', 0) < 70:
                insights.append(("Keywords", "Align skills with the target role."))
            if scores.get('ats_compatibility', 0) < 80:
                insights.append(("ATS", "Use standard headings, avoid tables/graphics."))
            
            if not insights:
                st.success("✅ Great job! No critical issues detected.")
            else:
                for title, text in insights:
                    st.markdown(
                        f"<div class='insight-box'><strong>{title}</strong><br>{text}</div>",
                        unsafe_allow_html=True
                    )
            
            # Recommendations
            if analysis.get('recommendations'):
                st.markdown("#### 📝 Improvement Recommendations")
                for i, rec in enumerate(analysis['recommendations'][:5], 1):
                    with st.expander(f"Tip {i}"):
                        st.write(rec)
        
        # TAB 4: Summary
        with tab4:
            st.markdown("#### 📄 Summary Table")
            summary_df = pd.DataFrame({
                'Metric': [
                    'Overall',
                    'Content',
                    'Keywords',
                    'ATS',
                    'Structure',
                    'Completeness',
                    'Word Count',
                    'Action Verbs'
                ],
                'Value': [
                    scores.get('overall_score', 0),
                    scores.get('content_quality', 0),
                    scores.get('keyword_optimization', 0),
                    scores.get('ats_compatibility', 0),
                    scores.get('structure_score', 0),
                    scores.get('completeness', 0),
                    analysis.get('word_count', 0),
                    analysis.get('action_verbs_count', 0)
                ]
            })
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download Summary (CSV)",
                    data=summary_df.to_csv(index=False),
                    file_name=f"resume_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                if st.checkbox("Show Raw JSON"):
                    st.json(analysis)

# ============================================================================
# PAGE: JOB MATCHING
# ============================================================================
elif page == "🎯 Job Matching":
    st.markdown("""
    <div class="header-container">
        <h1><i class="fas fa-bullseye icon"></i> Job Description Matching</h1>
        <p>Compare your resume against job requirements</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.analysis_results:
        st.warning("⚠️ Please upload and analyze a resume first.")
    else:
        resume_names = list(st.session_state.analysis_results.keys())
        selected_resume = st.selectbox(
            "**Select Resume:**",
            resume_names,
            index=0,
            key="job_match_resume"
        )
        
        st.markdown("---")
        
        # Job Description Input
        job_desc = st.text_area(
            "**Paste Job Description:**",
            height=200,
            placeholder="Paste the complete job description here...",
            help="Copy and paste the full job description to analyze match"
        )
        
        # Match Threshold Slider
        threshold = st.slider(
            "**Match Threshold (%)**",
            min_value=50,
            max_value=100,
            value=70,
            help="Minimum match percentage to highlight"
        )
        
        # Analyze Match Button
        analyze_match = st.button(
            "🔍 Analyze Match",
            use_container_width=True,
            type="primary",
            disabled=not (job_desc and job_desc.strip())
        )
        
        if analyze_match and job_desc and job_desc.strip():
            with st.spinner("Analyzing job match..."):
                # Simulate analysis
                time.sleep(1)
                
                # For demo, use first uploaded file
                if st.session_state.uploaded_files:
                    file = st.session_state.uploaded_files[0]
                    if file.type == "application/pdf":
                        resume_text = extract_text_from_pdf(file)
                    else:
                        resume_text = file.read().decode('utf-8')
                    
                    match_score = calculate_match_score(resume_text, job_desc)
                    missing = extract_missing_keywords(resume_text, job_desc)
                    
                    st.markdown("---")
                    st.markdown("### 📊 Match Results")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Match Score", f"{match_score}%")
                        if match_score >= threshold:
                            st.success("✓ Good Match")
                        else:
                            st.warning("⚠ Below Threshold")
                    
                    with col2:
                        st.metric("Missing Keywords", len(missing))
                    
                    with col3:
                        status = "Strong" if match_score >= 80 else "Moderate" if match_score >= 60 else "Weak"
                        st.metric("Match Status", status)
                    
                    # Missing Keywords
                    if missing:
                        st.markdown("### 🔑 Missing Keywords")
                        st.markdown(
                            " ".join([f"<span class='skill-badge' style='background:#EF4444;'>{kw}</span>" for kw in missing[:15]]),
                            unsafe_allow_html=True
                        )
                    
                    # Gauge Chart
                    fig = go.Figure(go.Indicator(
                            mode="gauge+number+delta",
                            value=match_score,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Match Score"},
                            delta={'reference': threshold},
                            gauge={
                                'axis': {'range': [None, 100]},
                                'bar': {'color': "#2563EB"},
                                'steps': [
                                    {'range': [0, 60], 'color': "#FEE2E2"},
                                    {'range': [60, 80], 'color': "#FEF3C7"},
                                    {'range': [80, 100], 'color': "#D1FAE5"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': threshold
                                }
                            }
                        ))
                    fig.update_layout(paper_bgcolor='white', height=300)
                    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: SETTINGS
# ============================================================================
elif page == "⚙️ Settings":
    st.markdown("""
    <div class="header-container">
        <h1><i class="fas fa-cogs icon"></i> Settings & Preferences</h1>
        <p>Customize your analysis parameters</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎛️ Analysis Weights")
    st.markdown("Adjust the importance of each scoring factor:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        content_weight = st.select_slider(
            "Content Quality Weight",
            options=list(range(0, 51, 5)),
            value=st.session_state.settings['weights']['content']
        )
        
        keywords_weight = st.select_slider(
            "Keywords Weight",
            options=list(range(0, 51, 5)),
            value=st.session_state.settings['weights']['keywords']
        )
    
    with col2:
        ats_weight = st.select_slider(
            "ATS Compatibility Weight",
            options=list(range(0, 51, 5)),
            value=st.session_state.settings['weights']['ats']
        )
        
        structure_weight = st.select_slider(
            "Structure Weight",
            options=list(range(0, 51, 5)),
            value=st.session_state.settings['weights']['structure']
        )
    
    total_weight = content_weight + keywords_weight + ats_weight + structure_weight
    if total_weight != 100:
        st.warning(f"⚠️ Total weight is {total_weight}%. Should be 100%.")
    
    st.markdown("---")
    
    st.markdown("### 🏭 Industry Selection")
    industry = st.selectbox(
        "Target Industry",
        ["Technology", "Healthcare", "Finance", "Education", "Marketing", "Engineering", "Other"],
        index=0
    )
    
    st.markdown("---")
    
    st.markdown("### 🎨 Display Options")
    
    show_json = st.checkbox("Show Raw JSON Data", value=st.session_state.settings['show_json'])
    show_charts = st.checkbox("Show Advanced Charts", value=True)
    show_tips = st.checkbox("Show Improvement Tips", value=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Settings", use_container_width=True, type="primary"):
            st.session_state.settings = {
                'threshold': 70,
                'industry': industry,
                'show_json': show_json,
                'weights': {
                    'content': content_weight,
                    'keywords': keywords_weight,
                    'ats': ats_weight,
                    'structure': structure_weight
                }
            }
            st.success("✅ Settings saved!")
    
    with col2:
        if st.button("🔄 Reset to Default", use_container_width=True):
            st.session_state.settings = {
                'threshold': 70,
                'industry': 'Technology',
                'show_json': False,
                'weights': {
                    'content': 30,
                    'keywords': 25,
                    'ats': 25,
                    'structure': 20
                }
            }
            st.success("✅ Reset to defaults!")
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            st.session_state.uploaded_files = []
            st.session_state.analysis_results = {}
            st.success("✅ All data cleared!")
            st.rerun()
