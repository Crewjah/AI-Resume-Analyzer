import re
from collections import Counter
from typing import Dict, List, Any
import string

class ResumeAnalyzer:
    """
    Main class for analyzing resumes using NLP techniques.
    Extracts skills, calculates scores, and provides recommendations.
    """
    
    def __init__(self):
        """Initialize the analyzer with NLP model."""
        # Common skills database
        self.technical_skills = {
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
            'typescript', 'go', 'rust', 'scala', 'r', 'matlab', 'sql', 'html', 'css',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'express',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'opencv',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'git', 'linux',
            'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch', 'cassandra',
            'machine learning', 'deep learning', 'nlp', 'computer vision', 'data science',
            'artificial intelligence', 'blockchain', 'cloud computing', 'devops', 'agile',
            'restful api', 'graphql', 'microservices', 'ci/cd', 'test automation'
        }
        
        self.soft_skills = {
            'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
            'creativity', 'adaptability', 'time management', 'collaboration', 'analytical',
            'project management', 'presentation', 'negotiation', 'conflict resolution',
            'decision making', 'emotional intelligence', 'mentoring', 'strategic thinking'
        }
    
    def analyze(self, resume_text: str) -> Dict[str, Any]:
        """
        Perform comprehensive resume analysis.
        
        Args:
            resume_text: The extracted text from resume
            
        Returns:
            Dictionary containing analysis results
        """
        # Clean text
        clean_text = self._clean_text(resume_text)
        
        # Extract information
        skills = self._extract_skills(clean_text)
        keywords = self._extract_keywords(clean_text)
        
        # Calculate scores
        content_score = self._calculate_content_score(clean_text)
        keyword_score = self._calculate_keyword_score(keywords)
        ats_score = self._calculate_ats_score(clean_text)
        structure_score = self._calculate_structure_score(clean_text)
        completeness_score = self._calculate_completeness_score(clean_text)
        
        # Overall score (weighted average)
        overall_score = int(
            content_score * 0.25 +
            keyword_score * 0.20 +
            ats_score * 0.25 +
            structure_score * 0.15 +
            completeness_score * 0.15
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            clean_text, skills, overall_score, ats_score
        )
        
        return {
            'overall_score': overall_score,
            'content_score': content_score,
            'keyword_score': keyword_score,
            'ats_score': ats_score,
            'structure_score': structure_score,
            'completeness_score': completeness_score,
            'skills': skills,
            'keywords': keywords,
            'recommendations': recommendations,
            'word_count': len(clean_text.split())
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep periods and commas
        text = re.sub(r'[^\w\s.,@-]', '', text)
        return text.strip().lower()
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical and soft skills from resume."""
        found_skills = []
        text_lower = text.lower()
        
        # Check for technical skills
        for skill in self.technical_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        # Check for soft skills
        for skill in self.soft_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))
    
    def _extract_keywords(self, text: str) -> Dict[str, int]:
        """Extract and count important keywords."""
        # Remove stopwords and punctuation
        words = text.split()
        
        # Simple stopwords list
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
        
        # Filter words
        filtered_words = [
            word for word in words 
            if word not in stopwords and len(word) > 3 and word.isalpha()
        ]
        
        # Count frequencies
        word_freq = Counter(filtered_words)
        
        # Return top keywords
        return dict(word_freq.most_common(15))
    
    def _calculate_content_score(self, text: str) -> int:
        """Calculate content quality score based on word count and structure."""
        word_count = len(text.split())
        
        # Ideal resume length: 400-800 words
        if 400 <= word_count <= 800:
            score = 100
        elif 300 <= word_count < 400 or 800 < word_count <= 1000:
            score = 85
        elif 200 <= word_count < 300 or 1000 < word_count <= 1200:
            score = 70
        else:
            score = 60
        
        # Check for action verbs
        action_verbs = [
            'developed', 'managed', 'created', 'designed', 'implemented',
            'led', 'achieved', 'improved', 'increased', 'reduced',
            'analyzed', 'collaborated', 'coordinated', 'established'
        ]
        
        action_verb_count = sum(1 for verb in action_verbs if verb in text)
        if action_verb_count >= 5:
            score = min(100, score + 10)
        
        return score
    
    def _calculate_keyword_score(self, keywords: Dict[str, int]) -> int:
        """Calculate keyword optimization score."""
        if not keywords:
            return 50
        
        # Check keyword diversity
        unique_keywords = len(keywords)
        
        if unique_keywords >= 15:
            score = 100
        elif unique_keywords >= 10:
            score = 85
        elif unique_keywords >= 7:
            score = 70
        else:
            score = 60
        
        return score
    
    def _calculate_ats_score(self, text: str) -> int:
        """Calculate ATS (Applicant Tracking System) compatibility score."""
        score = 100
        
        # Check for common ATS-unfriendly elements
        # Penalize for excessive special characters
        special_char_ratio = sum(1 for c in text if c in string.punctuation) / max(len(text), 1)
        if special_char_ratio > 0.05:
            score -= 15
        
        # Check for standard sections
        sections = [
            'experience', 'education', 'skills', 'projects',
            'summary', 'objective', 'certification', 'achievement'
        ]
        
        sections_found = sum(1 for section in sections if section in text)
        if sections_found < 3:
            score -= 20
        
        # Check for email and contact info
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            score -= 10
        
        return max(0, score)
    
    def _calculate_structure_score(self, text: str) -> int:
        """Calculate resume structure and formatting score."""
        score = 100
        
        # Check for key sections
        has_contact = bool(re.search(r'@|phone|email|linkedin', text))
        has_experience = 'experience' in text or 'work' in text
        has_education = 'education' in text or 'degree' in text or 'university' in text
        has_skills = 'skills' in text or 'technologies' in text
        
        sections_present = sum([has_contact, has_experience, has_education, has_skills])
        
        if sections_present < 3:
            score -= 30
        elif sections_present == 3:
            score -= 10
        
        # Check for dates (indicates proper chronology)
        date_pattern = r'\b(19|20)\d{2}\b|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{4}\b'
        if not re.search(date_pattern, text, re.IGNORECASE):
            score -= 15
        
        return max(0, score)
    
    def _calculate_completeness_score(self, text: str) -> int:
        """Calculate how complete the resume is."""
        score = 100
        
        # Check for essential elements
        essential_elements = {
            'email': r'@',
            'experience_indicators': r'(experience|worked|developed|managed)',
            'education': r'(education|degree|university|college|bachelor|master)',
            'skills': r'(skills|proficient|technologies|languages)',
            'timeframe': r'\b(19|20)\d{2}\b'
        }
        
        for element, pattern in essential_elements.items():
            if not re.search(pattern, text, re.IGNORECASE):
                score -= 15
        
        return max(0, score)
    
    def _generate_recommendations(
        self, 
        text: str, 
        skills: List[str], 
        overall_score: int,
        ats_score: int
    ) -> List[str]:
        """Generate personalized recommendations for resume improvement."""
        recommendations = []
        
        # Word count recommendations
        word_count = len(text.split())
        if word_count < 300:
            recommendations.append(
                "Your resume is too brief. Add more details about your experience and achievements (aim for 400-800 words)."
            )
        elif word_count > 1000:
            recommendations.append(
                "Your resume is too lengthy. Focus on the most relevant experiences and achievements (aim for 400-800 words)."
            )
        
        # Skills recommendations
        if len(skills) < 5:
            recommendations.append(
                "Add more relevant skills to your resume. Include both technical and soft skills that match your field."
            )
        
        # ATS recommendations
        if ats_score < 70:
            recommendations.append(
                "Improve ATS compatibility by using standard section headings (Experience, Education, Skills) and avoiding complex formatting."
            )
        
        # Action verbs
        action_verbs = ['developed', 'managed', 'led', 'achieved', 'implemented']
        if not any(verb in text for verb in action_verbs):
            recommendations.append(
                "Use strong action verbs to describe your achievements (e.g., developed, managed, led, achieved, implemented)."
            )
        
        # Contact information
        if not re.search(r'@', text):
            recommendations.append(
                "Ensure your contact information is clearly visible, including email and phone number."
            )
        
        # Quantifiable achievements
        if not re.search(r'\d+%|\d+\+|increased|decreased|improved', text):
            recommendations.append(
                "Add quantifiable achievements with metrics (e.g., 'Increased efficiency by 30%', 'Managed team of 5')."
            )
        
        # If no recommendations, add positive feedback
        if not recommendations:
            recommendations.append(
                "Your resume is well-structured! Consider tailoring it for specific job applications for better results."
            )
        
        return recommendations[:6]  # Return top 6 recommendations
