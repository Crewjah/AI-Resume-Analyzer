"""
Main Streamlit application for AI Resume Analyzer
Modular architecture with separate components
"""
import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Import custom modules
from src.analyzer import ResumeAnalyzer
from ui_components import (
    load_css, create_hero_header, create_metric_card, create_glass_card,
    display_skills_showcase, display_keywords_showcase, create_progress_bar,
    create_status_badge, create_recommendation_card, show_loading_animation,
    create_upload_zone, create_feature_showcase, create_success_message, 
    create_error_message
)
from src.config import APP_CONFIG, SUPPORTED_FILE_TYPES, SCORING_THRESHOLDS

# Configure page
st.set_page_config(
    page_title=APP_CONFIG['title'],
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function with modern UI"""
    # Load custom CSS
    load_css()
    
    # Create hero header
    create_hero_header()
    
    # Initialize analyzer
    analyzer = ResumeAnalyzer()
    
    # Sidebar with features
    with st.sidebar:
        create_feature_showcase()
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: white; margin-top: 2rem; padding: 1rem; 
         border-radius: 8px;">
            <h4 style="color: #cfe6ff; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.6px;">
                Supported file formats
            </h4>
            <p style="color: #9fb0c8;">TXT, PDF, DOCX</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File upload section with modern design
        create_glass_card(
            content="""
            <div style="text-align: center; padding: 1rem 0.5rem;">
                <h4 style="color: #cfe6ff; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.25rem;">Upload resume</h4>
                <p style="color: #9fb0c8; font-size: 0.98rem; margin: 0;">Provide your resume file to begin analysis.</p>
            </div>
            """,
            title="Upload"
        )
        
        uploaded_file = st.file_uploader(
            "Select your resume file",
            type=SUPPORTED_FILE_TYPES,
            help=f"Supported formats: {', '.join(SUPPORTED_FILE_TYPES).upper()}",
            label_visibility="collapsed",
            key="neural_resume_uploader"
        )
        
        # Job description section with modern design
        create_glass_card(
            content="""
            <div style="text-align: center; padding: 2rem 1rem;">
                <div style="font-size: 4rem; margin-bottom: 1.5rem;">🎯</div>
                <h4 style="color: var(--neon-purple); font-size: 1.3rem; font-weight: 700; 
                 margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 2px; 
                 text-shadow: 0 0 20px var(--neon-purple);">HOLOGRAPHIC JOB MATRIX</h4>
                <div style="color: var(--neon-orange); font-size: 1rem; font-weight: 600; 
                 margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 1px;">(OPTIONAL)</div>
                <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; line-height: 1.7; margin: 0;">
                    Input target position parameters for <br>
                    <span style="color: var(--neon-cyan); font-weight: 600;">quantum compatibility analysis</span> 
                    and <span style="color: var(--neon-purple); font-weight: 600;">neural matching algorithms</span>
                </p>
            </div>
            """,
            title="🌐 Quantum Job Synchronization"
        )
        
        job_description = st.text_area(
            "Job description (optional)",
            height=160,
            placeholder="Paste the job description to get a role-specific match (optional).",
            label_visibility="collapsed",
            key="quantum_job_matrix"
        )
    
    with col2:
        # Status panel with modern design
            if uploaded_file:
            file_size = len(uploaded_file.getvalue()) / 1024  # KB
            create_status_badge("File Uploaded Successfully", "success")
            
            create_glass_card(
                content=f"""
                <div style="text-align: center; padding: 2rem 1rem;">
                    <h4 style="color: #cfe6ff; font-size: 1.05rem; font-weight: 600; margin-bottom: 0.6rem;">File details</h4>
                    <div style="background: rgba(0,245,255,0.15); padding: 1.5rem; border-radius: 16px; 
                     border: 1px solid rgba(0,245,255,0.4); margin-bottom: 1.5rem;">
                        <p style="color: #cfe6ff; font-family: 'JetBrains Mono', monospace; 
                         font-size: 1rem; margin: 0; word-break: break-all; font-weight: 600;">{uploaded_file.name}</p>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #9fb0c8; font-size: 0.98rem; margin-bottom: 1rem;">
                            Size: <span style="color: #cfe6ff; font-weight: 600;">{file_size:.1f} KB</span>
                        </div>
                        <div style="color: #9fb0c8; font-weight: 600; font-size: 0.98rem;">
                            Ready for analysis
                        </div>
                    </div>
                </div>
                """,
                title="📊 Upload Status"
            )
            
            if job_description:
                st.info("Job description provided — role-specific matching enabled")
            else:
                st.info("No job description — generic analysis will be provided")
        else:
            create_status_badge("Waiting for resume", "warning")
            
            create_glass_card(
                content="""
                <div style="text-align: center; padding: 2rem 1rem;">
                    <h4 style="color: #cfe6ff; font-size: 1.05rem; margin-bottom: 0.5rem;">Waiting for resume</h4>
                    <p style="color: #9fb0c8;">Upload a resume file to see results and recommendations.</p>
                </div>
                """,
                title="System Status"
            )
    
    # Analysis section with modern button
    if uploaded_file:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Analyze", type="primary", use_container_width=True, key="neural_analyze_button"):
            analyze_resume(analyzer, uploaded_file, job_description)

def analyze_resume(analyzer, uploaded_file, job_description):
    """Perform resume analysis and display results with modern UI"""
    
    # Show loading animation
    loading_placeholder = st.empty()
    with loading_placeholder:
        show_loading_animation("Analyzing your resume...")
        time.sleep(1)  # Brief pause for animation effect
    
    try:
        # Extract text from file
        resume_text = analyzer.extract_text_from_file(uploaded_file)
        
        # Perform analysis
        results = analyzer.analyze_resume(resume_text, job_description)

        # If analyzer determined the text is invalid, show error and return
        if isinstance(results, dict) and results.get('valid') is False:
            loading_placeholder.empty()
            create_error_message(results.get('message', 'Invalid resume content'))
            return
        
        # Clear loading animation
        loading_placeholder.empty()
        
        # Display success message
        create_success_message("Analysis completed")
        
        # Display results with modern UI
        display_modern_results(results)
        
    except Exception as e:
        loading_placeholder.empty()
        create_error_message(f"An error occurred during analysis: {str(e)}")
    
def display_modern_results(results):
    """Display analysis results with modern UI components"""
    
    # Display key metrics with modern cards
    st.markdown("<h2 style='text-align: center; color: white; margin: 3rem 0 2rem 0; font-weight: 700;'>📊 Analysis Results</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ats_score = results['ats_score']
        create_metric_card(
            title="ATS Score",
            value=f"{ats_score}%",
            description=get_score_description(ats_score),
            icon="🎯"
        )
    
    with col2:
        skill_count = results['skill_count']
        create_metric_card(
            title="Skills Detected",
            value=str(skill_count),
            description=f"{skill_count} unique skills found",
            icon="⚡"
        )
    
    with col3:
        if results['job_analysis']:
            match_score = results['job_analysis']['match_score']
            create_metric_card(
                title="Job Match",
                value=f"{match_score}%",
                description=get_match_description(match_score),
                icon="🔍"
            )
        else:
            create_metric_card(
                title="Job Match",
                value="N/A",
                description="Add job description",
                icon="🔍"
            )
    
    with col4:
        exp_years = results['experience_years']
        exp_text = f"{exp_years}" if exp_years > 0 else "0"
        create_metric_card(
            title="Experience",
            value=f"{exp_text}Y",
            description="Years detected",
            icon="👨‍💼"
        )
    
    # Progress bars for scores
    st.markdown("<br><h3 style='color: white; text-align: center; margin: 2rem 0;'>📈 Score Breakdown</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        create_progress_bar(ats_score, 100, "🎯 ATS Compatibility Score")
    
    with col2:
        if results['job_analysis']:
            create_progress_bar(results['job_analysis']['match_score'], 100, "🔍 Job Match Score")
        else:
            create_progress_bar(0, 100, "🔍 Job Match Score (No Job Description)")
    
    # Display detailed sections
    display_detailed_sections(results)

def get_score_description(score):
    """Get description based on score"""
    if score >= 80:
        return "Excellent compatibility"
    elif score >= 60:
        return "Good compatibility"
    elif score >= 40:
        return "Fair compatibility"
    else:
        return "Needs improvement"

def get_match_description(score):
    """Get match description based on score"""
    if score >= 80:
        return "Excellent match"
    elif score >= 60:
        return "Good match"
    elif score >= 40:
        return "Fair match"
    else:
        return "Poor match"

def display_detailed_sections(results):
    """Display detailed analysis sections with modern UI"""
    
    st.markdown("<br><h2 style='color: white; text-align: center; margin: 3rem 0 2rem 0; font-weight: 700;'>🔍 Detailed Analysis</h2>", unsafe_allow_html=True)
    
    # Skills Analysis
    st.markdown("<h3 style='color: white; margin: 2rem 0 1rem 0;'>🚀 Skills Portfolio</h3>", unsafe_allow_html=True)
    display_skills_showcase(results['skills'])
    
    # Keywords Analysis
    if results['keywords']:
        st.markdown("<h3 style='color: white; margin: 2rem 0 1rem 0;'>🔑 Important Keywords</h3>", unsafe_allow_html=True)
        display_keywords_showcase(results['keywords'], "Professional Keywords", "🔑")
    
    # Job Analysis Section
    if results['job_analysis']:
        st.markdown("<h3 style='color: white; margin: 2rem 0 1rem 0;'>🎯 Job Match Analysis</h3>", unsafe_allow_html=True)
        
        job_analysis = results['job_analysis']
        
        col1, col2 = st.columns(2)
        with col1:
            if job_analysis['matched_keywords']:
                display_keywords_showcase(
                    job_analysis['matched_keywords'], 
                    "Matched Keywords", 
                    "✅"
                )
        
        with col2:
            if job_analysis['missing_keywords']:
                display_keywords_showcase(
                    job_analysis['missing_keywords'][:10], 
                    "Missing Keywords", 
                    "❌"
                )
    
    # Recommendations Section
    if results['recommendations']:
        st.markdown("<h3 style='color: white; margin: 2rem 0 1rem 0;'>💡 Improvement Recommendations</h3>", unsafe_allow_html=True)
        
        for i, recommendation in enumerate(results['recommendations'][:5], 1):
            create_recommendation_card(
                title=f"Recommendation #{i}",
                content=recommendation,
                icon="💡"
            )

def display_skills_analysis(results):
    """Display skills analysis tab content"""
    st.subheader("Detected Skills")
    
    if results['skills']:
        # Display skills table
        display_skills_table(results['skills'])
        
        # Skills by category
        st.subheader("Skills by Category")
        categories = {}
        for skill in results['skills']:
            category = skill.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append(skill['name'])
        
        for category, skills in categories.items():
            with st.expander(f"{category} ({len(skills)} skills)"):
                st.write(", ".join(skills))
    else:
        st.info("💡 No specific technical skills were detected in your resume. Consider adding more technical terms relevant to your field.")

def display_job_matching(results):
    """Display job matching analysis"""
    if not results['job_analysis']:
        st.info("📝 Upload a job description to see matching analysis and get personalized recommendations.")
        return
    
    job_analysis = results['job_analysis']
    match_score = job_analysis['match_score']
    
    # Match score summary
    st.subheader(f"Match Score: {match_score}%")
    
    if match_score >= 70:
        st.success("🎉 Excellent match! Your resume aligns well with this job.")
    elif match_score >= 50:
        st.warning("👍 Good match! Consider adding some missing keywords.")
    elif match_score >= 30:
        st.warning("⚠️ Fair match. Your resume needs some improvements for this role.")
    else:
        st.error("❌ Low match. Consider significant improvements for this specific role.")
    
    # Display keywords (standardized key: 'matched_keywords')
    matched = job_analysis.get('matched_keywords') or job_analysis.get('matching_keywords') or []
    missing = job_analysis.get('missing_keywords', [])
    display_keywords(matched, missing)
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Job Keywords", job_analysis['total_job_keywords'])
    with col2:
        st.metric("Matching Keywords", len(matched))
    with col3:
        st.metric("Missing Keywords", len(missing))

if __name__ == "__main__":
    main()