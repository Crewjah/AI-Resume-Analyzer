#!/usr/bin/env python3
"""
Resume Analysis Engine
Comprehensive resume analysis with ATS scoring, skills detection, and job matching.

Classes:
    ResumeAnalyzer: Main analyzer class with resume processing and analysis methods
"""

import re
from io import BytesIO
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path

# PDF support
try:
    from pypdf import PdfReader
    PDF_LIBRARY = 'pypdf'
except ImportError:
    try:
        from PyPDF2 import PdfReader
        PDF_LIBRARY = 'PyPDF2'
    except ImportError:
        PdfReader = None
        PDF_LIBRARY = None

# DOCX support
try:
    from docx import Document
except ImportError:
    Document = None


class ResumeAnalyzer:
    """
    Comprehensive resume analyzer for ATS scores, skills extraction, and job matching.
    
    Attributes:
        skills_database (List[str]): Comprehensive list of detectable skills
        skill_categories (Dict[str, List[str]]): Skills grouped by category
        min_word_count (int): Minimum words for valid resume
        professional_keywords (List[str]): Action words and professional terms
    """
    
    def __init__(self):
        """Initialize the analyzer with skills database and configuration."""
        # Comprehensive skills database
        self.skills_database = [
            # Programming Languages
            "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", ".NET",
            "PHP", "Ruby", "Go", "Rust", "Swift", "Kotlin", "Scala", "Groovy",
            "R", "MATLAB", "Objective-C", "Perl", "Haskell", "Clojure", "Erlang",
            
            # Web Technologies
            "HTML", "CSS", "SCSS", "LESS", "React", "Angular", "Vue.js", "Svelte",
            "Next.js", "Nuxt.js", "Gatsby", "Node.js", "Express", "Django", "Flask",
            "FastAPI", "Spring", "Laravel", "Symfony", "ASP.NET", "Ruby on Rails",
            "GraphQL", "REST API", "WebSocket", "AJAX",
            
            # Mobile Development
            "React Native", "Flutter", "Android", "iOS", "Xamarin", "Swift",
            "Kotlin", "Java Mobile", "PhoneGap", "Ionic",
            
            # Databases & Data
            "SQL", "MySQL", "PostgreSQL", "MongoDB", "Firebase", "Firestore",
            "Redis", "SQLite", "Oracle", "SQL Server", "MariaDB", "Cassandra",
            "DynamoDB", "CosmosDB", "Elasticsearch", "Neo4j", "Memcached",
            "Data Warehouse", "Data Lake", "Hadoop", "Spark", "Hive",
            
            # Cloud & DevOps
            "AWS", "Azure", "Google Cloud", "DigitalOcean", "Heroku", "Vercel",
            "Netlify", "Docker", "Kubernetes", "Jenkins", "GitLab CI", "GitHub Actions",
            "CircleCI", "Travis CI", "Terraform", "CloudFormation", "Ansible",
            "Prometheus", "Grafana", "ELK Stack", "DataDog", "New Relic",
            
            # Version Control
            "Git", "GitHub", "GitLab", "Bitbucket", "Mercurial", "SVN",
            
            # Data Science & AI/ML
            "Machine Learning", "Deep Learning", "Neural Networks", "TensorFlow",
            "PyTorch", "Scikit-learn", "Keras", "Pandas", "NumPy", "SciPy",
            "Matplotlib", "Seaborn", "Plotly", "Data Analysis", "Statistical Analysis",
            "Natural Language Processing", "NLP", "Computer Vision", "OpenCV",
            "Jupyter", "Anaconda", "Apache Spark", "Big Data",
            
            # Testing & QA
            "Unit Testing", "Integration Testing", "JUnit", "Pytest", "Jest",
            "Mocha", "Jasmine", "Selenium", "TestNG", "Cucumber", "BDD",
            "TDD", "Automated Testing", "QA", "Bug Tracking",
            
            # Other Technologies
            "Linux", "Windows", "macOS", "Unix", "Shell Script", "Bash",
            "PowerShell", "YAML", "JSON", "XML", "Regex", "API Design",
            "Microservices", "Agile", "Scrum", "Kanban", "Waterfall",
            "OAuth", "JWT", "Security", "Encryption", "SSL/TLS",
            "Apache", "Nginx", "IIS", "Load Balancing", "Caching",
            "Message Queues", "RabbitMQ", "Kafka", "AWS SQS", "WebRTC"
        ]
        
        # Skill categories for organized output
        self.skill_categories = {
            'Programming Languages': [
                "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", ".NET",
                "PHP", "Ruby", "Go", "Rust", "Swift", "Kotlin", "Scala"
            ],
            'Web Technologies': [
                "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express",
                "Django", "Flask", "FastAPI", "GraphQL", "REST API"
            ],
            'Databases': [
                "SQL", "MySQL", "PostgreSQL", "MongoDB", "Firebase", "Redis",
                "Oracle", "SQLite", "DynamoDB", "Elasticsearch"
            ],
            'Cloud & DevOps': [
                "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins",
                "GitLab CI", "GitHub Actions", "Terraform", "Ansible"
            ],
            'Data Science & AI': [
                "Machine Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy",
                "Scikit-learn", "Deep Learning", "NLP", "Data Analysis"
            ],
            'Mobile Development': [
                "React Native", "Flutter", "Android", "iOS", "Swift", "Kotlin"
            ],
            'Other': []  # Fallback category
        }
        
        # Professional action words and keywords
        self.professional_keywords = [
            "led", "managed", "developed", "implemented", "designed", "created",
            "achieved", "improved", "increased", "optimized", "enhanced", "designed",
            "built", "architected", "directed", "coordinated", "collaborated",
            "contributed", "facilitated", "executed", "delivered", "maintained",
            "mentored", "trained", "supervised", "oversaw", "responsible",
            "spearheaded", "pioneered", "investigated", "analyzed", "evaluated",
            "demonstrated", "established", "initiated", "introduced", "launched",
            "streamlined", "reduced", "decreased", "automated", "accelerated",
            "communicated", "negotiated", "presented", "resolved", "identified",
            "solved", "strategic", "tactical", "leadership", "innovation"
        ]
        
        # Configuration
        self.min_word_count = 50
        self.max_experience_years = 60  # Reasonable max experience
    
    # ========== File Extraction Methods ==========
    
    def extract_text_from_file(self, file_path: str) -> str:
        """
        Extract text from various file formats (PDF, DOCX, TXT).
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            Extracted text from the file
        """
        try:
            path = Path(file_path)
            
            if path.suffix.lower() == '.pdf':
                return self._extract_pdf_text(file_path)
            elif path.suffix.lower() == '.docx':
                return self._extract_docx_text(file_path)
            elif path.suffix.lower() == '.txt':
                return self._extract_text_file(file_path)
            else:
                # Try to read as text
                return self._extract_text_file(file_path)
        
        except Exception as e:
            return f""
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file."""
        if PdfReader is None:
            return ""
        
        try:
            with open(file_path, 'rb') as file:
                pdf = PdfReader(file)
                text = ""
                
                for page in pdf.pages:
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except Exception:
                        continue
                
                return text.strip()
        
        except Exception:
            return ""
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        if Document is None:
            return ""
        
        try:
            doc = Document(file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n"
            
            return text.strip()
        
        except Exception:
            return ""
    
    def _extract_text_file(self, file_path: str) -> str:
        """Extract text from plain text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception:
            return ""
    
    # ========== Text Analysis Methods ==========
    
    def detect_skills(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect skills mentioned in resume text.
        
        Args:
            text: Resume text to analyze
            
        Returns:
            List of detected skills with metadata, sorted by frequency
        """
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.skills_database:
            # Case-insensitive word boundary matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            if matches:
                found_skills.append({
                    'name': skill,
                    'count': len(matches),
                    'category': self._categorize_skill(skill)
                })
        
        # Sort by frequency (most mentioned first)
        found_skills.sort(key=lambda x: x['count'], reverse=True)
        return found_skills
    
    def _categorize_skill(self, skill: str) -> str:
        """Categorize a skill based on predefined categories."""
        for category, skills in self.skill_categories.items():
            if skill in skills:
                return category
        return 'Other'
    
    def calculate_ats_score(self, text: str, detected_skills: List[Dict]) -> int:
        """
        Calculate ATS (Applicant Tracking System) compatibility score.
        
        Args:
            text: Resume text
            detected_skills: List of detected skills
            
        Returns:
            ATS score (0-100)
        """
        score = 0
        words = text.split()
        word_count = len(words)
        
        # 1. Skills Diversity (40 points max)
        skill_count = len(detected_skills)
        if skill_count >= 15:
            score += 40
        elif skill_count >= 10:
            score += 35
        elif skill_count >= 7:
            score += 28
        elif skill_count >= 4:
            score += 20
        elif skill_count >= 2:
            score += 10
        else:
            score += 5
        
        # 2. Content Length (20 points max)
        if 300 <= word_count <= 800:
            score += 20
        elif 200 <= word_count <= 1200:
            score += 15
        elif word_count >= 100:
            score += 10
        else:
            score += 5
        
        # 3. Professional Keywords (20 points max)
        text_lower = text.lower()
        keyword_matches = sum(
            1 for keyword in self.professional_keywords
            if keyword in text_lower
        )
        score += min(20, keyword_matches * 2)
        
        # 4. Contact Information (10 points max)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        
        if re.search(email_pattern, text):
            score += 5
        if re.search(phone_pattern, text):
            score += 5
        
        # 5. Structure Indicators (10 points max)
        sections = ['experience', 'education', 'skills', 'summary', 'objective',
                   'projects', 'certifications', 'languages']
        section_count = sum(1 for section in sections if section in text_lower)
        score += min(10, section_count)
        
        return min(100, max(0, score))
    
    def extract_experience_years(self, text: str) -> int:
        """
        Extract estimated years of experience from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            Estimated years of experience
        """
        patterns = [
            r'(\d+)\s*(?:\+)?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)',
            r'(\d+)\s+(?:years?|yrs?)\s+(?:of\s+)?(?:professional\s+)?(?:experience|exp)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                years = int(match.group(1))
                return min(years, self.max_experience_years)
        
        return 0
    
    def analyze_job_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze resume match against job description.
        
        Args:
            resume_text: Resume text
            job_description: Job description text
            
        Returns:
            Job matching analysis with scores and keyword comparisons
        """
        if not job_description.strip():
            return {
                'match_score': 0,
                'matched_keywords': [],
                'missing_keywords': [],
                'total_job_keywords': 0
            }
        
        # Tokenize and filter
        resume_words = set(
            word.lower() for word in resume_text.split()
            if word.isalpha() and len(word) > 3
        )
        job_words = set(
            word.lower() for word in job_description.split()
            if word.isalpha() and len(word) > 3
        )
        
        # Remove common words
        common_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy',
            'did', 'does', 'let', 'put', 'say', 'she', 'too', 'use', 'will', 'work',
            'team', 'company', 'role', 'position', 'candidate', 'must', 'should',
            'able', 'with', 'have', 'this', 'that', 'they', 'from', 'would',
            'there', 'been', 'many', 'some', 'time', 'very', 'when', 'come',
            'here', 'just', 'like', 'long', 'make', 'over', 'such', 'take', 'than',
            'them', 'well', 'were'
        }
        
        job_keywords = job_words - common_words
        matched = list(resume_words.intersection(job_keywords))[:15]
        missing = list(job_keywords - resume_words)[:15]
        
        # Calculate match score
        match_score = int((len(matched) / len(job_keywords)) * 100) if job_keywords else 0
        
        return {
            'match_score': min(100, match_score),
            'matched_keywords': matched,
            'missing_keywords': missing,
            'total_job_keywords': len(job_keywords)
        }
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract important professional keywords from resume.
        
        Args:
            text: Resume text
            
        Returns:
            List of extracted keywords
        """
        keywords = []
        text_lower = text.lower()
        
        for keyword in self.professional_keywords:
            if keyword in text_lower:
                keywords.append(keyword.title())
        
        return list(set(keywords))[:10]  # Return unique, max 10
    
    def validate_resume(self, text: str) -> Tuple[bool, str]:
        """
        Validate that extracted text is a legitimate resume.
        
        Args:
            text: Extracted resume text
            
        Returns:
            (is_valid, error_message)
        """
        if not text or not isinstance(text, str):
            return False, 'No text extracted from file'
        
        word_count = len(text.split())
        
        if word_count < self.min_word_count:
            return False, f'Resume too short ({word_count} words). Minimum {self.min_word_count} required.'
        
        return True, ''
    
    def generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Generate actionable recommendations to improve resume.
        
        Args:
            analysis: Analysis results dictionary
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # ATS score recommendations
        ats = analysis.get('ats_score', 0)
        if ats < 50:
            recommendations.append('Add more relevant technical skills and certifications to improve ATS score')
        if ats < 70:
            recommendations.append('Include more action verbs and quantifiable achievements')
        
        # Skills recommendations
        skill_count = analysis.get('skill_count', 0)
        if skill_count < 5:
            recommendations.append('Add 3-5 more relevant technical skills to your profile')
        elif skill_count > 20:
            recommendations.append('Focus on top 10-15 most relevant skills; trim less important ones')
        
        # Content length
        words = analysis.get('word_count', 0)
        if words < 200:
            recommendations.append('Expand your resume with more detailed job descriptions and achievements')
        elif words > 1000:
            recommendations.append('Condense your resume to 1 page; focus on most relevant experience')
        
        # Job matching
        job_match = analysis.get('job_analysis', {})
        if job_match:
            match_score = job_match.get('match_score', 0)
            missing = job_match.get('missing_keywords', [])
            
            if match_score < 50 and missing:
                recommendations.append(f'Add keywords from job description: {", ".join(missing[:3])}')
            elif match_score < 70:
                recommendations.append('Incorporate more job-specific keywords naturally in your descriptions')
        
        # Experience
        if analysis.get('experience_years', 0) == 0:
            recommendations.append('Clearly state your years of professional experience')
        
        # Default positive message
        if not recommendations:
            recommendations.append('Your resume looks well-structured! Keep it updated with latest skills')
        
        return recommendations
    
    # ========== Main Analysis Method ==========
    
    def analyze_resume(self, resume_text: str, job_description: str = '') -> Dict[str, Any]:
        """
        Perform comprehensive resume analysis.
        
        Args:
            resume_text: Extracted resume text
            job_description: Optional job description for matching
            
        Returns:
            Complete analysis results with all metrics
        """
        # Validate resume
        is_valid, error_msg = self.validate_resume(resume_text)
        
        if not is_valid:
            return {
                'valid': False,
                'message': error_msg,
                'word_count': len(resume_text.split()),
                'ats_score': 0,
                'skill_count': 0,
                'experience_years': 0,
                'job_analysis': None,
                'skills': {},
                'keywords': [],
                'recommendations': [error_msg]
            }
        
        # Analyze
        word_count = len(resume_text.split())
        detected_skills = self.detect_skills(resume_text)
        ats_score = self.calculate_ats_score(resume_text, detected_skills)
        experience_years = self.extract_experience_years(resume_text)
        job_analysis = self.analyze_job_match(resume_text, job_description) if job_description else None
        keywords = self.extract_keywords(resume_text)
        
        # Format skills by category
        skills_by_category = {}
        for skill in detected_skills[:20]:  # Top 20 skills
            cat = skill['category']
            if cat not in skills_by_category:
                skills_by_category[cat] = []
            skills_by_category[cat].append(skill['name'])
        
        # Compile results
        results = {
            'word_count': word_count,
            'ats_score': ats_score,
            'skill_count': len(detected_skills),
            'skills': skills_by_category,
            'keywords': keywords,
            'experience_years': experience_years,
            'job_analysis': job_analysis
        }
        
        # Generate recommendations
        results['recommendations'] = self.generate_recommendations(results)
        
        return results
