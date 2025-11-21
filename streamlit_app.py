"""
Main Streamlit application for AI Resume Analyzer
Modular architecture with separate components
"""
import streamlit as st
import pandas as pd
from datetime import datetime

# Import custom modules
from analyzer import ResumeAnalyzer
from ui_components import (
    load_css, create_header, create_metric_card, create_info_card,
    display_skills_table, display_keywords, display_recommendations, create_sidebar
)
from config import APP_CONFIG, SUPPORTED_FILE_TYPES, SCORING_THRESHOLDS

# Configure page
st.set_page_config(
    page_title=APP_CONFIG['title'],
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    # Load custom CSS
    load_css()
    
    # Create header
    create_header()
    
    # Create sidebar
    create_sidebar()
    
    # Initialize analyzer
    analyzer = ResumeAnalyzer()
    
    # Main content layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File upload section
        st.markdown(create_info_card(
            "Upload Resume", 
            "Choose your resume file to analyze"
        ), unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Select your resume file",
            type=SUPPORTED_FILE_TYPES,
            help=f"Supported formats: {', '.join(SUPPORTED_FILE_TYPES).upper()}"
        )
        
        # Job description section
        st.markdown(create_info_card(
            "Job Description (Optional)", 
            "Add a job description for better matching analysis"
        ), unsafe_allow_html=True)
        
        job_description = st.text_area(
            "Paste the job description here",
            height=150,
            placeholder="Paste the complete job description to get personalized keyword matching..."
        )
    
    with col2:
        # Status and info panel
        st.markdown(create_info_card(
            "Analysis Status", 
            ""
        ), unsafe_allow_html=True)
        
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            file_size = len(uploaded_file.getvalue()) / 1024  # KB
            st.info(f"📏 File size: {file_size:.1f} KB")
            
            if job_description:
                st.info("🎯 Job description provided - enhanced matching available")
            else:
                st.warning("💡 Add job description for better insights")
        else:
            st.warning("⏳ Please upload a resume file")
    
    # Analysis section
    if uploaded_file:
        if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
            analyze_resume(analyzer, uploaded_file, job_description)

def analyze_resume(analyzer, uploaded_file, job_description):
    """Perform resume analysis and display results"""
    
    # Show analysis progress
    with st.spinner("Analyzing your resume..."):
        # Extract text from file
        resume_text = analyzer.extract_text_from_file(uploaded_file)
        
        # Check if text extraction was successful
        if resume_text.startswith("Error reading file") or "requires additional setup" in resume_text:
            st.error(resume_text)
            return
        
        # Perform analysis
        results = analyzer.analyze_resume(resume_text, job_description)
    
    # Display success message
    st.success("✅ Analysis completed successfully!")
    
    # Display key metrics
    display_metrics(results)
    
    # Display detailed results in tabs
    display_detailed_results(results)

def display_metrics(results):
    """Display key metrics in cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            create_metric_card(results['ats_score'], "ATS Score", "score"),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_metric_card(results['skill_count'], "Skills Found"),
            unsafe_allow_html=True
        )
    
    with col3:
        if results['job_analysis']:
            match_score = results['job_analysis']['match_score']
            st.markdown(
                create_metric_card(f"{match_score}%", "Job Match", "score"),
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                create_metric_card("-", "Job Match"),
                unsafe_allow_html=True
            )
    
    with col4:
        exp_text = f"{results['experience_years']} years" if results['experience_years'] > 0 else "Not specified"
        st.markdown(
            create_metric_card(exp_text, "Experience"),
            unsafe_allow_html=True
        )

def display_detailed_results(results):
    """Display detailed analysis results in tabs"""
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "🛠️ Skills Analysis", 
        "🎯 Job Matching", 
        "💡 Recommendations"
    ])
    
    with tab1:
        display_overview(results)
    
    with tab2:
        display_skills_analysis(results)
    
    with tab3:
        display_job_matching(results)
    
    with tab4:
        display_recommendations(results['recommendations'])

def display_overview(results):
    """Display overview tab content"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Resume Statistics")
        st.metric("Word Count", results['word_count'])
        st.metric("Skills Detected", results['skill_count'])
        st.metric("ATS Score", f"{results['ats_score']}/100")
        
        # ATS Score interpretation
        ats_score = results['ats_score']
        if ats_score >= SCORING_THRESHOLDS['ats_excellent']:
            st.success("🎉 Excellent ATS compatibility!")
        elif ats_score >= SCORING_THRESHOLDS['ats_good']:
            st.info("👍 Good ATS compatibility")
        elif ats_score >= SCORING_THRESHOLDS['ats_fair']:
            st.warning("⚠️ Fair ATS compatibility - room for improvement")
        else:
            st.error("❌ Poor ATS compatibility - needs significant improvement")
    
    with col2:
        st.subheader("Quick Insights")
        
        # Experience insight
        if results['experience_years'] > 0:
            st.write(f"👨‍💼 **Experience Level:** {results['experience_years']} years")
        else:
            st.write("👨‍💼 **Experience Level:** Not clearly specified")
        
        # Skills insight
        skill_count = results['skill_count']
        if skill_count >= SCORING_THRESHOLDS['skills_good']:
            st.write(f"🛠️ **Skills:** Strong technical profile ({skill_count} skills)")
        elif skill_count >= SCORING_THRESHOLDS['skills_minimum']:
            st.write(f"🛠️ **Skills:** Moderate technical profile ({skill_count} skills)")
        else:
            st.write(f"🛠️ **Skills:** Limited technical skills mentioned ({skill_count} skills)")
        
        # Word count insight
        word_count = results['word_count']
        if SCORING_THRESHOLDS['word_count_optimal_min'] <= word_count <= SCORING_THRESHOLDS['word_count_optimal_max']:
            st.write(f"📄 **Length:** Optimal length ({word_count} words)")
        elif word_count < SCORING_THRESHOLDS['word_count_min']:
            st.write(f"📄 **Length:** Too brief ({word_count} words)")
        elif word_count > SCORING_THRESHOLDS['word_count_max']:
            st.write(f"📄 **Length:** Too lengthy ({word_count} words)")
        else:
            st.write(f"📄 **Length:** Acceptable ({word_count} words)")

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
    
    # Display keywords
    display_keywords(job_analysis['matching_keywords'], job_analysis['missing_keywords'])
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Job Keywords", job_analysis['total_job_keywords'])
    with col2:
        st.metric("Matching Keywords", len(job_analysis['matching_keywords']))
    with col3:
        st.metric("Missing Keywords", len(job_analysis['missing_keywords']))

if __name__ == "__main__":
    main()