"""
Demo script for AI Resume Analyzer
Shows example usage and features
"""

import streamlit as st
from resume_analyzer import ResumeAnalyzer
import json

# Sample resume text for demonstration
SAMPLE_RESUME = """
John Doe
Software Engineer
Email: john.doe@email.com
Phone: (555) 123-4567

SUMMARY
Experienced software engineer with 5+ years of experience in full-stack development, 
specializing in Python, JavaScript, and cloud technologies. Proven track record of 
delivering scalable solutions and leading cross-functional teams.

EXPERIENCE
Senior Software Engineer | Tech Corporation | 2021-2023
• Developed and maintained microservices using Python, Django, and PostgreSQL
• Implemented CI/CD pipelines using Jenkins and Docker, reducing deployment time by 40%
• Led a team of 4 developers in building a customer analytics platform
• Collaborated with product managers and designers to deliver user-centric solutions

Software Engineer | StartUp Inc | 2019-2021
• Built responsive web applications using React, Node.js, and MongoDB
• Integrated payment systems using Stripe API and improved transaction success rate by 15%
• Participated in agile development processes and code reviews
• Mentored junior developers and conducted technical interviews

EDUCATION
Bachelor of Science in Computer Science | University of Technology | 2015-2019
• GPA: 3.8/4.0
• Relevant Coursework: Data Structures, Algorithms, Database Systems, Software Engineering

SKILLS
Programming Languages: Python, JavaScript, Java, TypeScript, SQL
Frameworks: Django, React, Node.js, Express.js, Flask
Databases: PostgreSQL, MongoDB, Redis, MySQL
Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, Git, GitHub
Tools: Linux, Jira, Confluence, Postman

PROJECTS
E-commerce Platform | Personal Project
• Built a full-stack e-commerce application using React and Django
• Implemented user authentication, payment processing, and inventory management
• Deployed on AWS using EC2, RDS, and S3
• GitHub: github.com/johndoe/ecommerce-platform

CERTIFICATIONS
• AWS Certified Solutions Architect - Associate (2022)
• Certified Scrum Master (2021)
"""

SAMPLE_JOB_DESCRIPTION = """
Senior Full Stack Developer - Remote

We are looking for an experienced Senior Full Stack Developer to join our growing team. 
The ideal candidate will have expertise in modern web technologies and cloud platforms.

Requirements:
• 5+ years of experience in full-stack development
• Strong proficiency in Python, JavaScript, and TypeScript
• Experience with React, Node.js, and Django frameworks
• Knowledge of cloud platforms (AWS, Azure, or Google Cloud)
• Experience with containerization (Docker, Kubernetes)
• Understanding of CI/CD pipelines and DevOps practices
• Strong database skills (PostgreSQL, MongoDB)
• Experience with version control systems (Git)
• Excellent problem-solving and communication skills
• Bachelor's degree in Computer Science or related field

Preferred Qualifications:
• Experience with microservices architecture
• Knowledge of machine learning and data science
• AWS certifications
• Experience with agile development methodologies
• Open source contributions

Responsibilities:
• Design and develop scalable web applications
• Collaborate with cross-functional teams
• Mentor junior developers
• Participate in code reviews and technical discussions
• Implement best practices for security and performance
• Contribute to architecture and design decisions
"""

def run_demo():
    """Run a demonstration of the resume analyzer"""
    
    st.title("🚀 AI Resume Analyzer Demo")
    
    st.markdown("""
    This demo showcases the capabilities of our AI Resume Analyzer using sample data.
    """)
    
    # Initialize analyzer
    analyzer = ResumeAnalyzer()
    
    # Analyze sample resume
    with st.spinner("Analyzing sample resume..."):
        results = analyzer.analyze_resume(
            SAMPLE_RESUME, 
            SAMPLE_JOB_DESCRIPTION, 
            "Complete Analysis", 
            depth=5, 
            industry="Technology"
        )
    
    # Display results
    st.success("✅ Analysis Complete!")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("ATS Score", f"{results['ats_score']}/100", delta="Good")
    
    with col2:
        st.metric("Skills Found", results['skill_count'], delta="+Technical")
    
    with col3:
        st.metric("Job Match", f"{results['match_score']}%", delta="High")
    
    with col4:
        st.metric("Experience", f"{results['experience_years']} years", delta="Senior")
    
    # Detailed results
    with st.expander("📊 Detailed Analysis Results", expanded=True):
        st.json(results, expanded=False)
    
    # Recommendations
    st.subheader("💡 Recommendations")
    for i, rec in enumerate(results.get('recommendations', []), 1):
        with st.expander(f"Recommendation {i}: {rec.get('title', 'N/A')}"):
            st.write(rec.get('description', 'No description available'))
            if rec.get('priority'):
                priority_color = {
                    'High': '🔴',
                    'Medium': '🟡', 
                    'Low': '🔵'
                }.get(rec['priority'], '⚪')
                st.write(f"Priority: {priority_color} {rec['priority']}")

if __name__ == "__main__":
    run_demo()