"""
UI styling and components for the resume analyzer
"""
import streamlit as st

def load_css():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .info-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .info-card h3 {
        margin-top: 0;
        color: #1e293b;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        color: #64748b;
        font-size: 0.9rem;
    }
    
    /* Score colors */
    .score-excellent { color: #059669; }
    .score-good { color: #0891b2; }
    .score-fair { color: #d97706; }
    .score-poor { color: #dc2626; }
    
    /* Feature list styling */
    .feature-list {
        list-style: none;
        padding: 0;
    }
    
    .feature-list li {
        padding: 0.5rem 0;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .feature-list li:last-child {
        border-bottom: none;
    }
    
    /* Upload area styling */
    .upload-info {
        background: #f1f5f9;
        padding: 1rem;
        border-radius: 8px;
        border: 2px dashed #cbd5e1;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Success/Info/Warning styling */
    .success-box {
        background: #dcfce7;
        border: 1px solid #bbf7d0;
        padding: 1rem;
        border-radius: 8px;
        color: #166534;
    }
    
    .info-box {
        background: #dbeafe;
        border: 1px solid #bfdbfe;
        padding: 1rem;
        border-radius: 8px;
        color: #1e40af;
    }
    
    .warning-box {
        background: #fef3c7;
        border: 1px solid #fde68a;
        padding: 1rem;
        border-radius: 8px;
        color: #92400e;
    }
    
    /* Keywords styling */
    .keyword-match {
        background: #dcfce7;
        color: #166534;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.85rem;
        margin: 0.1rem;
        display: inline-block;
    }
    
    .keyword-missing {
        background: #fee2e2;
        color: #991b1b;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.85rem;
        margin: 0.1rem;
        display: inline-block;
    }
    
    /* Recommendation styling */
    .recommendation {
        background: #f8fafc;
        border-left: 4px solid #4f46e5;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def create_header():
    """Create the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>AI Resume Analyzer</h1>
        <p>Professional resume analysis and optimization tool</p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(value, label, score_type="normal"):
    """Create a metric display card"""
    score_class = ""
    if score_type == "score":
        if value >= 80:
            score_class = "score-excellent"
        elif value >= 70:
            score_class = "score-good"
        elif value >= 50:
            score_class = "score-fair"
        else:
            score_class = "score-poor"
    
    return f"""
    <div class="metric-card">
        <h3 class="{score_class}">{value}</h3>
        <p>{label}</p>
    </div>
    """

def create_info_card(title, content):
    """Create an information card"""
    return f"""
    <div class="info-card">
        <h3>{title}</h3>
        {content}
    </div>
    """

def display_skills_table(skills):
    """Display skills in a clean table format"""
    if not skills:
        st.info("No specific technical skills detected. Consider adding more technical terms to your resume.")
        return
    
    # Create a clean display of skills
    skills_data = []
    for skill in skills:
        skills_data.append({
            'Skill': skill['name'],
            'Category': skill['category'],
            'Mentions': skill['count']
        })
    
    import pandas as pd
    df = pd.DataFrame(skills_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def display_keywords(matching_keywords, missing_keywords):
    """Display matching and missing keywords"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Matching Keywords")
        if matching_keywords:
            keywords_html = ""
            for keyword in matching_keywords:
                keywords_html += f'<span class="keyword-match">{keyword}</span> '
            st.markdown(keywords_html, unsafe_allow_html=True)
        else:
            st.info("No matching keywords found")
    
    with col2:
        st.subheader("Missing Keywords")
        if missing_keywords:
            keywords_html = ""
            for keyword in missing_keywords[:10]:  # Show only top 10
                keywords_html += f'<span class="keyword-missing">{keyword}</span> '
            st.markdown(keywords_html, unsafe_allow_html=True)
        else:
            st.success("Great keyword coverage!")

def display_recommendations(recommendations):
    """Display recommendations in a styled format"""
    if not recommendations:
        st.success("Your resume looks excellent! No major improvements needed.")
        return
    
    st.subheader("Improvement Recommendations")
    for i, recommendation in enumerate(recommendations, 1):
        st.markdown(f"""
        <div class="recommendation">
            <strong>{i}.</strong> {recommendation}
        </div>
        """, unsafe_allow_html=True)

def create_sidebar():
    """Create the sidebar with features and information"""
    with st.sidebar:
        st.markdown("### Features")
        features_html = """
        <ul class="feature-list">
            <li>📄 Resume Upload & Analysis</li>
            <li>🎯 Skills Detection</li>
            <li>📊 ATS Compatibility Scoring</li>
            <li>🔍 Job Description Matching</li>
            <li>💡 Improvement Recommendations</li>
            <li>📈 Professional Insights</li>
        </ul>
        """
        st.markdown(features_html, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### Supported Formats")
        st.markdown("• TXT files")
        st.markdown("• PDF files")
        st.markdown("• DOCX files")
        
        st.markdown("---")
        st.markdown("### Tips for Better Results")
        st.markdown("• Include specific technical skills")
        st.markdown("• Use industry-standard keywords")
        st.markdown("• Quantify your achievements")
        st.markdown("• Keep format clean and readable")