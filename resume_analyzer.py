import re
import io
import spacy
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import PyPDF2
import docx
from typing import Dict, List, Tuple, Any
import streamlit as st

class ResumeAnalyzer:
    """Advanced resume analyzer using NLP and ML techniques"""
    
    def __init__(self):
        """Initialize the analyzer with required models and data"""
        self.load_models()
        self.setup_skill_categories()
        self.setup_patterns()
    
    def load_models(self):
        """Load NLP models"""
        try:
            # Try to load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if spaCy model not available
            st.warning("⚠️ spaCy model not found. Some features may be limited.")
            self.nlp = None
    
    def setup_skill_categories(self):
        """Define skill categories and keywords"""
        self.skill_categories = {
            "Programming Languages": [
                "Python", "Java", "JavaScript", "C++", "C#", "PHP", "Ruby", "Go", "Rust",
                "TypeScript", "Swift", "Kotlin", "R", "MATLAB", "Scala", "Perl", "HTML", "CSS"
            ],
            "Frameworks & Libraries": [
                "React", "Angular", "Vue.js", "Django", "Flask", "Spring", "Express.js",
                "Laravel", "Rails", "ASP.NET", "jQuery", "Bootstrap", "Tailwind", 
                "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy"
            ],
            "Databases": [
                "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle", 
                "SQL Server", "Cassandra", "DynamoDB", "Firebase", "Elasticsearch"
            ],
            "Cloud & DevOps": [
                "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins",
                "Git", "GitHub", "GitLab", "CI/CD", "Terraform", "Ansible", "Linux"
            ],
            "Data Science & AI": [
                "Machine Learning", "Deep Learning", "Data Analysis", "Statistics",
                "Big Data", "Hadoop", "Spark", "Tableau", "Power BI", "Excel",
                "NLP", "Computer Vision", "Neural Networks"
            ],
            "Soft Skills": [
                "Leadership", "Communication", "Problem Solving", "Team Work",
                "Project Management", "Critical Thinking", "Creativity", "Adaptability"
            ]
        }
        
        # Flatten all skills for easy searching
        self.all_skills = []
        for category, skills in self.skill_categories.items():
            self.all_skills.extend([(skill, category) for skill in skills])
    
    def setup_patterns(self):
        """Setup regex patterns for information extraction"""
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            'years_experience': r'(\d+)[\+\s]*(?:years?|yrs?)[\s]*(?:of\s*)?(?:experience|exp)',
            'degree': r'(bachelor|master|phd|doctorate|bs|ms|mba|ba|ma|bsc|msc)',
            'gpa': r'gpa[:\s]*(\d+\.?\d*)',
        }
    
    def extract_text_from_file(self, uploaded_file) -> str:
        """Extract text from uploaded file"""
        try:
            if uploaded_file.type == "application/pdf":
                return self._extract_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return self._extract_from_docx(uploaded_file)
            elif uploaded_file.type == "text/plain":
                return str(uploaded_file.read(), "utf-8")
            else:
                st.error(f"Unsupported file type: {uploaded_file.type}")
                return ""
        except Exception as e:
            st.error(f"Error extracting text: {str(e)}")
            return ""
    
    def _extract_from_pdf(self, file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    def _extract_from_docx(self, file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(io.BytesIO(file.read()))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    def analyze_resume(self, resume_text: str, job_description: str = "", 
                      analysis_type: str = "Complete Analysis", 
                      depth: int = 3, industry: str = "Technology") -> Dict[str, Any]:
        """Perform comprehensive resume analysis"""
        
        results = {
            'resume_text': resume_text,
            'word_count': len(resume_text.split()),
            'character_count': len(resume_text),
        }
        
        # Basic information extraction
        results.update(self._extract_basic_info(resume_text))
        
        # Skills analysis
        skills_data = self._analyze_skills(resume_text)
        results.update(skills_data)
        
        # ATS Score calculation
        results['ats_score'] = self._calculate_ats_score(resume_text, skills_data)
        
        # Job matching (if job description provided)
        if job_description.strip():
            results['job_analysis'] = self._analyze_job_match(resume_text, job_description)
            results['match_score'] = results['job_analysis']['match_score']
        else:
            results['match_score'] = 0
            results['job_analysis'] = None
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results, industry, depth)
        
        # Additional analysis based on type
        if analysis_type == "Complete Analysis":
            results.update(self._detailed_analysis(resume_text))
        
        return results
    
    def _extract_basic_info(self, text: str) -> Dict[str, Any]:
        """Extract basic information from resume"""
        info = {}
        
        # Extract email
        email_match = re.search(self.patterns['email'], text, re.IGNORECASE)
        info['email'] = email_match.group() if email_match else None
        
        # Extract phone
        phone_match = re.search(self.patterns['phone'], text)
        info['phone'] = phone_match.group() if phone_match else None
        
        # Extract years of experience
        exp_match = re.search(self.patterns['years_experience'], text, re.IGNORECASE)
        info['experience_years'] = int(exp_match.group(1)) if exp_match else 0
        
        # Extract education level
        degree_match = re.search(self.patterns['degree'], text, re.IGNORECASE)
        info['education_level'] = degree_match.group(1).title() if degree_match else "Not specified"
        
        # Extract GPA
        gpa_match = re.search(self.patterns['gpa'], text, re.IGNORECASE)
        info['gpa'] = float(gpa_match.group(1)) if gpa_match else None
        
        # Identify sections
        info['sections'] = self._identify_sections(text)
        
        return info
    
    def _identify_sections(self, text: str) -> List[str]:
        """Identify resume sections"""
        common_sections = [
            "summary", "objective", "experience", "education", "skills", 
            "projects", "certifications", "awards", "publications", "references"
        ]
        
        found_sections = []
        text_lower = text.lower()
        
        for section in common_sections:
            if section in text_lower:
                found_sections.append(section.title())
        
        return found_sections
    
    def _analyze_skills(self, text: str) -> Dict[str, Any]:
        """Analyze skills mentioned in the resume"""
        text_lower = text.lower()
        found_skills = []
        skill_categories_found = {}
        
        for skill, category in self.all_skills:
            if skill.lower() in text_lower:
                # Calculate confidence based on frequency and context
                count = text_lower.count(skill.lower())
                confidence = min(100, count * 20 + 60)  # Base confidence + frequency bonus
                
                found_skills.append({
                    'name': skill,
                    'category': category,
                    'confidence': confidence,
                    'count': count
                })
                
                # Count by category
                if category not in skill_categories_found:
                    skill_categories_found[category] = 0
                skill_categories_found[category] += 1
        
        # Sort skills by confidence
        found_skills.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'skills': found_skills,
            'skill_count': len(found_skills),
            'top_skills': found_skills[:15],
            'skill_categories': skill_categories_found
        }
    
    def _calculate_ats_score(self, text: str, skills_data: Dict) -> int:
        """Calculate ATS compatibility score"""
        score = 0
        
        # Base score for having text
        if len(text) > 100:
            score += 20
        
        # Skills diversity bonus
        skill_count = skills_data['skill_count']
        if skill_count >= 10:
            score += 25
        elif skill_count >= 5:
            score += 15
        elif skill_count >= 2:
            score += 10
        
        # Section completeness
        sections = self._identify_sections(text)
        essential_sections = ['experience', 'education', 'skills']
        section_score = sum(10 for section in essential_sections 
                          if section.lower() in [s.lower() for s in sections])
        score += section_score
        
        # Format indicators
        if re.search(r'\b\d{4}\b', text):  # Years
            score += 5
        if re.search(r'@', text):  # Email
            score += 5
        if re.search(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text):  # Phone
            score += 5
        
        # Length appropriateness
        word_count = len(text.split())
        if 300 <= word_count <= 800:
            score += 10
        elif 200 <= word_count <= 1000:
            score += 5
        
        return min(100, score)
    
    def _analyze_job_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze how well the resume matches the job description"""
        
        # Vectorize both texts
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        
        try:
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            match_score = int(similarity * 100)
        except:
            match_score = 50  # Default if vectorization fails
        
        # Extract keywords from job description
        job_keywords = self._extract_keywords(job_description)
        resume_keywords = self._extract_keywords(resume_text)
        
        # Find matching and missing keywords
        matching_keywords = list(set(job_keywords) & set(resume_keywords))
        missing_keywords = list(set(job_keywords) - set(resume_keywords))
        
        return {
            'match_score': match_score,
            'matching_keywords': matching_keywords[:20],
            'missing_keywords': missing_keywords[:20],
            'job_keywords': job_keywords[:30],
            'resume_keywords': resume_keywords[:30]
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Simple keyword extraction - can be enhanced with more sophisticated NLP
        blob = TextBlob(text.lower())
        
        # Get noun phrases and important words
        keywords = []
        
        # Add noun phrases
        for phrase in blob.noun_phrases:
            if len(phrase.split()) <= 3 and len(phrase) > 3:
                keywords.append(phrase)
        
        # Add important single words
        words = blob.words
        for word in words:
            if (len(word) > 4 and 
                word.isalpha() and 
                word not in ['experience', 'years', 'work', 'company', 'team', 'project']):
                keywords.append(str(word))
        
        # Remove duplicates and return most frequent
        from collections import Counter
        keyword_counts = Counter(keywords)
        return [word for word, count in keyword_counts.most_common(50)]
    
    def _generate_recommendations(self, results: Dict, industry: str, depth: int) -> List[Dict]:
        """Generate improvement recommendations"""
        recommendations = []
        
        # ATS Score recommendations
        if results['ats_score'] < 70:
            recommendations.append({
                'title': 'Improve ATS Compatibility',
                'description': 'Your resume may not pass through Applicant Tracking Systems effectively. Consider adding more relevant keywords, improving formatting, and ensuring all sections are clearly labeled.',
                'priority': 'High'
            })
        
        # Skills recommendations
        if results['skill_count'] < 8:
            recommendations.append({
                'title': 'Add More Technical Skills',
                'description': f'Consider adding more skills relevant to {industry}. Include both technical and soft skills that are commonly required in your target roles.',
                'priority': 'Medium'
            })
        
        # Job matching recommendations
        if 'job_analysis' in results and results['job_analysis']:
            if results['match_score'] < 60:
                recommendations.append({
                    'title': 'Improve Job Description Alignment',
                    'description': 'Your resume could better match the job requirements. Try incorporating more keywords from the job description naturally into your experience descriptions.',
                    'priority': 'High'
                })
        
        # Section recommendations
        essential_sections = ['experience', 'education', 'skills', 'summary']
        missing_sections = [section for section in essential_sections 
                          if section.lower() not in [s.lower() for s in results.get('sections', [])]]
        
        if missing_sections:
            recommendations.append({
                'title': 'Add Missing Resume Sections',
                'description': f'Consider adding these important sections: {", ".join(missing_sections)}. These sections help recruiters quickly find relevant information.',
                'priority': 'Medium'
            })
        
        # Experience recommendations
        if results.get('experience_years', 0) == 0:
            recommendations.append({
                'title': 'Highlight Your Experience',
                'description': 'Make sure to clearly state your years of experience. If you\'re entry-level, emphasize internships, projects, and relevant coursework.',
                'priority': 'Medium'
            })
        
        # Industry-specific recommendations
        if industry == 'Technology':
            if not any('github' in results['resume_text'].lower() or 'portfolio' in results['resume_text'].lower()):
                recommendations.append({
                    'title': 'Add Portfolio/GitHub Links',
                    'description': 'For technology roles, including links to your GitHub profile or portfolio can significantly strengthen your application.',
                    'priority': 'High'
                })
        
        return recommendations[:depth + 2]  # Return recommendations based on depth
    
    def _detailed_analysis(self, text: str) -> Dict[str, Any]:
        """Perform detailed analysis for complete analysis type"""
        
        analysis = {}
        
        # Readability analysis
        blob = TextBlob(text)
        sentences = blob.sentences
        
        analysis['readability'] = {
            'sentence_count': len(sentences),
            'avg_sentence_length': sum(len(s.words) for s in sentences) / len(sentences) if sentences else 0,
            'complexity_score': self._calculate_complexity(text)
        }
        
        # Sentiment analysis
        sentiment = blob.sentiment
        analysis['sentiment'] = {
            'polarity': round(sentiment.polarity, 2),
            'subjectivity': round(sentiment.subjectivity, 2),
            'tone': 'Positive' if sentiment.polarity > 0.1 else 'Negative' if sentiment.polarity < -0.1 else 'Neutral'
        }
        
        # Keyword density
        words = text.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 4 and word.isalpha():
                word_freq[word] = word_freq.get(word, 0) + 1
        
        analysis['top_keywords'] = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        
        return analysis
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate text complexity score"""
        sentences = text.split('.')
        words = text.split()
        
        if len(sentences) == 0:
            return 0
        
        avg_sentence_length = len(words) / len(sentences)
        
        # Simple complexity based on sentence length and word length
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        complexity = (avg_sentence_length * 0.4 + avg_word_length * 0.6) / 10
        return min(10, max(1, complexity))