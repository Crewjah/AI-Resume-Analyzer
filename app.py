import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from backend.resume_analyzer import ResumeAnalyzer
from backend.pdf_extractor import extract_text_from_pdf, get_pdf_metadata
from backend.keyword_matcher import calculate_match_score, extract_missing_keywords
import base64
from pathlib import Path
import time
import json

# Configure page
st.set_page_config(
    page_title="ResumeGenie - AI-Powered Career Optimizer",
    page_icon="🧞‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS for enhanced UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styling */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 50%, #2d1b69 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #ffffff;
    }
    
    .main > div {
        padding: 1rem;
        background: transparent;
    }
    
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
        height: 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, .stDeployButton {
        display: none !important;
    }
    
    /* Professional Header */
    .hero-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 24px;
        padding: 4rem 2rem;
        margin: 2rem 0 3rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #00d4ff 0%, #ff0080 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse-glow 2s ease-in-out infinite alternate;
        position: relative;
        z-index: 2;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        color: rgba(255,255,255,0.9);
        font-weight: 400;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        position: relative;
        z-index: 2;
    }
    
    @keyframes pulse-glow {
        from { 
            filter: drop-shadow(0 0 10px rgba(0,212,255,0.5));
        }
        to { 
            filter: drop-shadow(0 0 30px rgba(255,0,128,0.7)) drop-shadow(0 0 50px rgba(0,212,255,0.3));
        }
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.3);
        border-color: rgba(0,212,255,0.5);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(0 0 15px rgba(0,212,255,0.5));
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #00d4ff;
        font-family: 'Poppins', sans-serif;
    }
    
    .feature-description {
        color: rgba(255,255,255,0.8);
        line-height: 1.6;
    }
    
    /* Upload Area */
    .upload-container {
        background: linear-gradient(135deg, rgba(0,212,255,0.1) 0%, rgba(255,0,128,0.1) 100%);
        backdrop-filter: blur(20px);
        border: 3px dashed rgba(0,212,255,0.5);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-container:hover {
        border-color: rgba(255,0,128,0.7);
        background: linear-gradient(135deg, rgba(255,0,128,0.1) 0%, rgba(0,212,255,0.1) 100%);
    }
    
    /* Results Section */
    .results-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 25px 50px rgba(0,0,0,0.2);
    }
    
    /* Score Cards */
    .score-card {
        background: linear-gradient(135deg, rgba(0,212,255,0.2) 0%, rgba(255,0,128,0.2) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .score-card:hover {
        transform: scale(1.05);
        border-color: rgba(0,212,255,0.7);
    }
    
    .score-value {
        font-size: 3rem;
        font-weight: 800;
        color: #00d4ff;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .score-label {
        font-size: 1rem;
        color: rgba(255,255,255,0.8);
        font-weight: 500;
    }
    
    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #00d4ff 0%, #ff0080 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.875rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .skill-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Recommendations */
    .recommendation {
        background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(59,130,246,0.1) 100%);
        border-left: 4px solid #10b981;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(16,185,129,0.2);
    }
    
    /* Progress Bars */
    .progress-container {
        background: rgba(255,255,255,0.1);
        height: 8px;
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #00d4ff 0%, #ff0080 100%);
        border-radius: 10px;
        transition: width 2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 20px rgba(0,212,255,0.5);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #ff0080 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: transparent;
    }
    
    [data-testid="stFileUploader"] > div > div {
        background: transparent;
        border: 3px dashed rgba(0,212,255,0.5);
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"] > div > div:hover {
        border-color: rgba(255,0,128,0.7);
        background: linear-gradient(135deg, rgba(255,0,128,0.05) 0%, rgba(0,212,255,0.05) 100%);
    }
    
    /* Text Areas */
    .stTextArea > div > div > textarea {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(0,212,255,0.7);
        box-shadow: 0 0 20px rgba(0,212,255,0.3);
    }
    
    /* Plotly Charts */
    .js-plotly-plot {
        background: transparent !important;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #00d4ff;
        margin: 2rem 0 1rem 0;
        font-family: 'Poppins', sans-serif;
        text-align: center;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, #00d4ff 0%, #ff0080 100%);
        border-radius: 2px;
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 4px solid rgba(255,255,255,0.1);
        border-top: 4px solid #00d4ff;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, rgba(16,185,129,0.2) 0%, rgba(34,197,94,0.2) 100%);
        border: 1px solid rgba(16,185,129,0.4);
        border-radius: 15px;
        padding: 1rem;
        color: #10b981;
        text-align: center;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def display_hero_section():
    """Display the enhanced hero section"""
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🧞‍♂️ ResumeGenie</h1>
        <p class="hero-subtitle">
            AI-Powered Career Optimizer • Transform Your Resume into a Job-Winning Masterpiece
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_features():
    """Display key features in a professional grid"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <h3 class="feature-title">Smart Analysis</h3>
            <p class="feature-description">
                Advanced AI algorithms analyze your resume across 15+ key metrics that matter to recruiters and ATS systems.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">⚡</span>
            <h3 class="feature-title">Instant Results</h3>
            <p class="feature-description">
                Get comprehensive feedback in seconds with actionable recommendations to improve your interview chances.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🔒</span>
            <h3 class="feature-title">Privacy First</h3>
            <p class="feature-description">
                Your resume data is processed locally and never stored. We respect your privacy completely.
            </p>
        </div>
        """, unsafe_allow_html=True)

def display_score_cards(scores):
    """Display scores in professional cards"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    score_data = [
        (col1, "Overall", scores.get('overall_score', 0), "🎯"),
        (col2, "Content", scores.get('content_quality', 0), "📝"),
        (col3, "Keywords", scores.get('keyword_optimization', 0), "🔤"),
        (col4, "ATS Score", scores.get('ats_compatibility', 0), "🤖"),
        (col5, "Structure", scores.get('structure_score', 0), "🏗️")
    ]
    
    for col, label, score, icon in score_data:
        with col:
            st.markdown(f"""
            <div class="score-card">
                <div class="score-value">{score}</div>
                <div class="score-label">{icon} {label}</div>
            </div>
            """, unsafe_allow_html=True)

def display_skill_tags(skills, skill_type="Technical"):
    """Display skills as modern tags"""
    if not skills:
        return
    
    tags_html = ""
    for skill in skills[:10]:  # Limit to 10 skills
        tags_html += f'<span class="skill-tag">{skill.title()}</span>'
    
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <h4 style="color: #00d4ff; margin-bottom: 1rem;">{skill_type} Skills:</h4>
        <div>{tags_html}</div>
    </div>
    """, unsafe_allow_html=True)

def create_radar_chart(scores):
    """Create a professional radar chart"""
    categories = ['Content Quality', 'Keywords', 'ATS Compatibility', 'Structure', 'Completeness']
    values = [
        scores.get('content_quality', 0),
        scores.get('keyword_optimization', 0),
        scores.get('ats_compatibility', 0),
        scores.get('structure_score', 0),
        scores.get('completeness', 0)
    ]
    
    fig = go.Figure()
    
    # Add resume scores
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Resume',
        line=dict(color='#00d4ff', width=3),
        fillcolor='rgba(0,212,255,0.2)'
    ))
    
    # Add industry average (benchmark)
    industry_avg = [75, 65, 70, 80, 75]
    fig.add_trace(go.Scatterpolar(
        r=industry_avg,
        theta=categories,
        fill='toself',
        name='Industry Average',
        line=dict(color='rgba(255,255,255,0.5)', width=2, dash='dash'),
        fillcolor='rgba(255,255,255,0.1)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='white', size=10),
                gridcolor='rgba(255,255,255,0.2)'
            ),
            angularaxis=dict(
                tickfont=dict(color='white', size=12)
            )
        ),
        showlegend=True,
        legend=dict(
            font=dict(color='white'),
            bgcolor='rgba(255,255,255,0.1)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    return fig

def display_recommendations(recommendations):
    """Display actionable recommendations"""
    if not recommendations:
        return
    
    st.markdown('<h2 class="section-header">💡 Personalized Recommendations</h2>', unsafe_allow_html=True)
    
    for i, rec in enumerate(recommendations[:5], 1):  # Show top 5 recommendations
        priority = "🔴" if i <= 2 else "🟡" if i <= 4 else "🟢"
        st.markdown(f"""
        <div class="recommendation">
            <strong>{priority} Priority #{i}</strong><br>
            {rec}
        </div>
        """, unsafe_allow_html=True)

def create_keyword_frequency_chart(word_freq):
    """Create a modern keyword frequency chart"""
    if not word_freq:
        return None
    
    # Get top 10 keywords
    top_words = dict(list(word_freq.items())[:10])
    
    fig = px.bar(
        x=list(top_words.values()),
        y=list(top_words.keys()),
        orientation='h',
        title="Most Frequent Keywords in Your Resume",
        color=list(top_words.values()),
        color_continuous_scale=[[0, '#ff0080'], [1, '#00d4ff']]
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font=dict(color='#00d4ff', size=18),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        showlegend=False,
        height=400
    )
    
    return fig

def main():
    """Main application function"""
    # Display hero section
    display_hero_section()
    
    # Display features
    display_features()
    
    # File upload section
    st.markdown('<h2 class="section-header">📄 Upload Your Resume</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your resume file",
        type=['pdf', 'txt'],
        help="Upload your resume in PDF or TXT format (Max 10MB)"
    )
    
    if uploaded_file is not None:
        # Show loading animation
        with st.spinner('🧞‍♂️ ResumeGenie is analyzing your resume...'):
            time.sleep(2)  # Simulate processing time
            
            try:
                # Extract text from uploaded file
                if uploaded_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf(uploaded_file)
                    metadata = get_pdf_metadata(uploaded_file)
                else:
                    resume_text = str(uploaded_file.read(), "utf-8")
                    metadata = {"num_pages": 1}
                
                if not resume_text.strip():
                    st.error("⚠️ Could not extract text from your resume. Please try a different file.")
                    return
                
                # Success message
                st.markdown("""
                <div class="success-message">
                    ✅ Resume uploaded and analyzed successfully!
                </div>
                """, unsafe_allow_html=True)
                
                # Analyze resume
                analyzer = ResumeAnalyzer()
                analysis = analyzer.analyze(resume_text)
                
                # Display results container
                st.markdown('<div class="results-container">', unsafe_allow_html=True)
                
                # Display scores
                st.markdown('<h2 class="section-header">🎯 Performance Dashboard</h2>', unsafe_allow_html=True)
                display_score_cards(analysis['scores'])
                
                # Create two columns for detailed analysis
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Radar chart
                    st.markdown('<h3 style="color: #00d4ff; text-align: center;">📊 Detailed Score Breakdown</h3>', unsafe_allow_html=True)
                    radar_fig = create_radar_chart(analysis['scores'])
                    st.plotly_chart(radar_fig, use_container_width=True)
                    
                    # Keyword frequency chart
                    if analysis.get('word_frequency'):
                        keyword_fig = create_keyword_frequency_chart(analysis['word_frequency'])
                        if keyword_fig:
                            st.plotly_chart(keyword_fig, use_container_width=True)
                
                with col2:
                    # Skills section
                    st.markdown('<h3 style="color: #00d4ff;">🛠️ Detected Skills</h3>', unsafe_allow_html=True)
                    
                    if analysis.get('technical_skills'):
                        display_skill_tags(analysis['technical_skills'], "Technical")
                    
                    if analysis.get('soft_skills'):
                        display_skill_tags(analysis['soft_skills'], "Soft")
                    
                    # Statistics
                    st.markdown(f"""
                    <div class="score-card">
                        <h4 style="color: #00d4ff;">📈 Resume Statistics</h4>
                        <p><strong>Word Count:</strong> {analysis.get('word_count', 0)}</p>
                        <p><strong>Skills Found:</strong> {len(analysis.get('technical_skills', [])) + len(analysis.get('soft_skills', []))}</p>
                        <p><strong>Action Verbs:</strong> {analysis.get('action_verbs_count', 0)}</p>
                        <p><strong>Readability:</strong> {analysis['scores'].get('readability', 0)}/100</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Recommendations
                if analysis.get('recommendations'):
                    display_recommendations(analysis['recommendations'])
                
                # Job description matching section
                st.markdown('<h2 class="section-header">🎯 Job Description Matching</h2>', unsafe_allow_html=True)
                
                job_description = st.text_area(
                    "Paste a job description to see how well your resume matches:",
                    height=150,
                    placeholder="Paste the job description here to get a match score..."
                )
                
                if job_description:
                    with st.spinner('🧞‍♂️ Calculating job match score...'):
                        match_score = calculate_match_score(resume_text, job_description)
                        missing_keywords = extract_missing_keywords(resume_text, job_description)
                        
                        # Display match score
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"""
                            <div class="score-card">
                                <div class="score-value">{match_score}%</div>
                                <div class="score-label">🎯 Job Match Score</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            if missing_keywords:
                                st.markdown(f"""
                                <div class="recommendation">
                                    <h4>🔍 Missing Keywords:</h4>
                                    <p>{', '.join(missing_keywords[:10])}</p>
                                </div>
                                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)  # Close results container
                
            except Exception as e:
                st.error(f"❌ Error analyzing resume: {str(e)}")
    
    else:
        # Show upload instructions
        st.markdown("""
        <div class="upload-container">
            <h3 style="color: #00d4ff; margin-bottom: 1rem;">📤 Ready to Optimize Your Resume?</h3>
            <p style="color: rgba(255,255,255,0.8); margin-bottom: 1.5rem;">
                Upload your resume and get instant feedback with actionable recommendations
            </p>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">
                Supported formats: PDF, TXT • Maximum size: 10MB
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin: 4rem 0 2rem 0; padding: 2rem; 
                background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
                border-radius: 20px; backdrop-filter: blur(10px);">
        <h3 style="color: #00d4ff; margin-bottom: 1rem;">🚀 Ready to Land Your Dream Job?</h3>
        <p style="color: rgba(255,255,255,0.8);">
            ResumeGenie has helped 50,000+ professionals optimize their resumes and land interviews at top companies.
        </p>
        <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-top: 2rem;">
            Made with ❤️ for Job Seekers Worldwide • Open Source • Privacy First • Always Free
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()