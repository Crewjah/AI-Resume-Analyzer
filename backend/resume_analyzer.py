import re
from collections import Counter
from typing import Dict, List, Any
import string

class ResumeAnalyzer:
    """
    Professional resume analyzer with enhanced NLP and scoring algorithms.
    Provides comprehensive analysis across multiple dimensions for better job matching.
    """
    
    def __init__(self):
        """Initialize the analyzer with comprehensive skill databases."""
        # Enhanced technical skills database with more comprehensive coverage
        self.technical_skills = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 
            'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'matlab', 'perl', 'shell',
            'bash', 'powershell', 'vba', 'sql', 'plsql', 'nosql',
            
            # Web Technologies
            'html', 'css', 'scss', 'sass', 'less', 'bootstrap', 'tailwind', 'react', 
            'angular', 'vue', 'svelte', 'ember', 'backbone', 'jquery', 'node.js', 
            'express', 'next.js', 'nuxt.js', 'gatsby', 'webpack', 'vite', 'babel',
            
            # Backend Frameworks
            'django', 'flask', 'fastapi', 'spring', 'spring boot', 'laravel', 'symfony',
            'rails', 'express.js', 'koa', 'nest.js', '.net', 'asp.net', 'mvc',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
            'dynamodb', 'firebase', 'oracle', 'sql server', 'sqlite', 'neo4j',
            'clickhouse', 'influxdb', 'couchbase',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins',
            'gitlab ci', 'github actions', 'terraform', 'ansible', 'vagrant', 'chef',
            'puppet', 'helm', 'istio', 'prometheus', 'grafana', 'elk stack', 'nginx',
            'apache', 'linux', 'ubuntu', 'centos', 'debian',
            
            # Data Science & AI
            'machine learning', 'deep learning', 'artificial intelligence', 'nlp',
            'computer vision', 'data science', 'data analysis', 'big data', 'pandas',
            'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'opencv',
            'matplotlib', 'seaborn', 'plotly', 'tableau', 'power bi', 'apache spark',
            'hadoop', 'kafka', 'airflow', 'jupyter', 'anaconda',
            
            # Mobile Development
            'ios', 'android', 'react native', 'flutter', 'xamarin', 'ionic', 'cordova',
            'swift ui', 'jetpack compose',
            
            # Tools & Methodologies
            'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'slack',
            'trello', 'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd',
            'microservices', 'api', 'rest', 'graphql', 'soap', 'json', 'xml',
            'oauth', 'jwt', 'ssl', 'https', 'cdn', 'load balancing'
        }
        
        # Enhanced soft skills database
        self.soft_skills = {
            'leadership', 'communication', 'teamwork', 'collaboration', 'problem solving',
            'critical thinking', 'creativity', 'innovation', 'adaptability', 'flexibility',
            'time management', 'organization', 'project management', 'analytical thinking',
            'attention to detail', 'multitasking', 'decision making', 'strategic thinking',
            'emotional intelligence', 'empathy', 'conflict resolution', 'negotiation',
            'presentation skills', 'public speaking', 'mentoring', 'coaching', 'delegation',
            'customer service', 'client management', 'relationship building', 'networking',
            'cultural awareness', 'cross-functional collaboration', 'remote work',
            'self-motivated', 'proactive', 'results-driven', 'goal-oriented'
        }
        
        # Action verbs that indicate strong achievements
        self.action_verbs = {
            'achieved', 'accomplished', 'delivered', 'developed', 'designed', 'implemented',
            'created', 'built', 'established', 'founded', 'launched', 'initiated',
            'led', 'managed', 'supervised', 'coordinated', 'directed', 'guided',
            'improved', 'enhanced', 'optimized', 'streamlined', 'increased', 'boosted',
            'reduced', 'decreased', 'minimized', 'saved', 'generated', 'produced',
            'analyzed', 'evaluated', 'assessed', 'researched', 'investigated',
            'collaborated', 'partnered', 'facilitated', 'mentored', 'trained',
            'presented', 'communicated', 'negotiated', 'resolved', 'solved'
        }
    
    def analyze(self, resume_text: str) -> Dict[str, Any]:
        """
        Perform comprehensive resume analysis with enhanced algorithms.
        
        Args:
            resume_text: The extracted text from resume
            
        Returns:
            Dictionary containing detailed analysis results
        """
        if not resume_text or not resume_text.strip():
            return self._get_empty_result()
        
        # Clean and normalize text
        clean_text = self._clean_text(resume_text)
        
        # Extract information
        skills = self._extract_skills(clean_text)
        keywords = self._extract_keywords(clean_text)
        
        # Calculate individual scores with enhanced algorithms
        content_score = self._calculate_content_score(clean_text, resume_text)
        keyword_score = self._calculate_keyword_score(keywords, clean_text)
        ats_score = self._calculate_ats_score(clean_text, resume_text)
        structure_score = self._calculate_structure_score(clean_text, resume_text)
        completeness_score = self._calculate_completeness_score(clean_text, resume_text)
        
        # Calculate weighted overall score
        overall_score = int(
            content_score * 0.25 +
            keyword_score * 0.20 +
            ats_score * 0.25 +
            structure_score * 0.15 +
            completeness_score * 0.15
        )
        
        # Generate intelligent recommendations
        recommendations = self._generate_recommendations(
            clean_text, resume_text, skills, overall_score, 
            content_score, keyword_score, ats_score, structure_score, completeness_score
        )
        
        return {
            'overall_score': max(1, min(100, overall_score)),
            'content_score': max(1, min(100, content_score)),
            'keyword_score': max(1, min(100, keyword_score)),
            'ats_score': max(1, min(100, ats_score)),
            'structure_score': max(1, min(100, structure_score)),
            'completeness_score': max(1, min(100, completeness_score)),
            'skills': skills,
            'keywords': dict(list(keywords.items())[:15]),  # Top 15 keywords
            'recommendations': recommendations,
            'word_count': len(clean_text.split()),
            'action_verbs_count': len(self._extract_action_verbs(clean_text)),
            'sections_detected': self._detect_sections(clean_text)
        }
    
    def _get_empty_result(self) -> Dict[str, Any]:
        """Return default result for empty input."""
        return {
            'overall_score': 1,
            'content_score': 1,
            'keyword_score': 1,
            'ats_score': 1,
            'structure_score': 1,
            'completeness_score': 1,
            'skills': [],
            'keywords': {},
            'recommendations': ['Please upload a valid resume file with content.'],
            'word_count': 0,
            'action_verbs_count': 0,
            'sections_detected': []
        }
    
    def _clean_text(self, text: str) -> str:
        """Enhanced text cleaning and normalization."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        # Remove excessive special characters but keep important ones
        text = re.sub(r'[^\w\s.,@()\-+#&/:]', ' ', text)
        # Remove multiple spaces again
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def _extract_skills(self, text: str) -> List[str]:
        """Enhanced skills extraction with better matching."""
        found_skills = set()
        text_lower = text.lower()
        
        # Check for technical skills with word boundaries
        for skill in self.technical_skills:
            pattern = rf'\b{re.escape(skill)}\b'
            if re.search(pattern, text_lower):
                # Capitalize properly for display
                found_skills.add(skill.title() if ' ' not in skill else skill)
        
        # Check for soft skills
        for skill in self.soft_skills:
            pattern = rf'\b{re.escape(skill)}\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill.title())
        
        return sorted(list(found_skills))
    
    def _extract_keywords(self, text: str) -> Dict[str, int]:
        """Enhanced keyword extraction with better filtering."""
        # Comprehensive stopwords
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
            'he', 'she', 'it', 'they', 'we', 'you', 'i', 'me', 'my', 'your', 'his',
            'her', 'its', 'our', 'their', 'who', 'what', 'when', 'where', 'why', 'how',
            'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'now'
        }
        
        # Extract words and filter
        words = re.findall(r'\b[a-z]{3,}\b', text)
        
        # Filter out stopwords and common resume words
        resume_stopwords = {'resume', 'cv', 'curriculum', 'vitae', 'name', 'address', 'phone', 'email'}
        filtered_words = [
            word for word in words 
            if word not in stopwords 
            and word not in resume_stopwords
            and len(word) > 3
            and not word.isdigit()
        ]
        
        # Count frequencies
        word_freq = Counter(filtered_words)
        
        # Return top keywords
        return dict(word_freq.most_common(20))
    
    def _extract_action_verbs(self, text: str) -> List[str]:
        """Extract action verbs from resume text."""
        found_verbs = []
        for verb in self.action_verbs:
            if re.search(rf'\b{verb}\b', text):
                found_verbs.append(verb)
        return found_verbs
    
    def _detect_sections(self, text: str) -> List[str]:
        """Detect common resume sections."""
        sections = []
        section_patterns = {
            'contact': r'\b(contact|phone|email|address|linkedin)\b',
            'summary': r'\b(summary|profile|objective|about)\b',
            'experience': r'\b(experience|work|employment|career|position)\b',
            'education': r'\b(education|degree|university|college|school)\b',
            'skills': r'\b(skills|technical|competencies|proficiencies)\b',
            'projects': r'\b(projects|portfolio|work)\b',
            'certifications': r'\b(certification|certificate|license)\b',
            'achievements': r'\b(achievement|award|accomplishment|honor)\b'
        }
        
        for section, pattern in section_patterns.items():
            if re.search(pattern, text):
                sections.append(section)
        
        return sections
    
    
    def _calculate_content_score(self, text: str, original_text: str = "") -> int:
        """Enhanced content quality score calculation."""
        word_count = len(text.split())
        
        # Base score from word count (optimal 400-800 words)
        if 400 <= word_count <= 800:
            word_score = 100
        elif 300 <= word_count < 400 or 800 < word_count <= 1000:
            word_score = 85
        elif 200 <= word_count < 300 or 1000 < word_count <= 1200:
            word_score = 70
        elif 150 <= word_count < 200 or 1200 < word_count <= 1500:
            word_score = 55
        else:
            word_score = 40
        
        # Bonus points for action verbs
        action_verbs_found = len(self._extract_action_verbs(text))
        action_verb_bonus = min(20, action_verbs_found * 3)
        
        # Bonus for quantified achievements (numbers, percentages)
        quantified_pattern = r'\b\d+%|\b\d+\+|increased|improved|reduced|saved|generated|\$\d+|grew by'
        quantified_matches = len(re.findall(quantified_pattern, text, re.IGNORECASE))
        quantified_bonus = min(15, quantified_matches * 5)
        
        # Penalty for excessive repetition
        words = text.split()
        if len(words) > 0:
            unique_words = len(set(words))
            repetition_ratio = unique_words / len(words)
            if repetition_ratio < 0.3:  # Too much repetition
                repetition_penalty = 15
            elif repetition_ratio < 0.5:
                repetition_penalty = 5
            else:
                repetition_penalty = 0
        else:
            repetition_penalty = 0
        
        final_score = word_score + action_verb_bonus + quantified_bonus - repetition_penalty
        return max(5, min(100, final_score))
    
    def _calculate_keyword_score(self, keywords: Dict[str, int], text: str = "") -> int:
        """Enhanced keyword optimization score."""
        if not keywords:
            return 20
        
        # Base score from keyword diversity
        unique_keywords = len(keywords)
        
        if unique_keywords >= 20:
            diversity_score = 100
        elif unique_keywords >= 15:
            diversity_score = 90
        elif unique_keywords >= 12:
            diversity_score = 80
        elif unique_keywords >= 10:
            diversity_score = 70
        elif unique_keywords >= 7:
            diversity_score = 60
        elif unique_keywords >= 5:
            diversity_score = 50
        else:
            diversity_score = 30
        
        # Bonus for technical keywords
        tech_keywords_found = sum(1 for keyword in keywords.keys() 
                                if any(tech in keyword.lower() for tech in self.technical_skills))
        tech_bonus = min(15, tech_keywords_found * 2)
        
        # Bonus for industry-relevant terms
        industry_terms = {'development', 'management', 'analysis', 'design', 'implementation', 
                         'optimization', 'strategy', 'solution', 'innovation', 'research'}
        industry_count = sum(1 for keyword in keywords.keys() 
                           if any(term in keyword.lower() for term in industry_terms))
        industry_bonus = min(10, industry_count * 2)
        
        final_score = diversity_score + tech_bonus + industry_bonus
        return max(10, min(100, final_score))
    
    def _calculate_ats_score(self, text: str, original_text: str = "") -> int:
        """Enhanced ATS (Applicant Tracking System) compatibility score."""
        score = 100
        
        # Check for excessive special characters
        if original_text:
            special_char_ratio = sum(1 for c in original_text if c in '!@#$%^&*()+=[]{}|\\:";\'<>?/~`') / max(len(original_text), 1)
            if special_char_ratio > 0.05:
                score -= 20
            elif special_char_ratio > 0.03:
                score -= 10
        
        # Check for standard sections
        required_sections = ['experience', 'education', 'skills']
        optional_sections = ['summary', 'objective', 'projects', 'certification']
        
        required_found = sum(1 for section in required_sections if section in text)
        optional_found = sum(1 for section in optional_sections if section in text)
        
        if required_found < 3:
            score -= 25
        elif required_found < 2:
            score -= 40
        
        # Bonus for having optional sections
        score += min(10, optional_found * 3)
        
        # Check for contact information
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        has_phone = bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\(\d{3}\)\s?\d{3}[-.]?\d{4}', text))
        
        if not has_email:
            score -= 15
        if not has_phone:
            score -= 10
        
        # Check for proper formatting indicators
        has_bullets = '•' in original_text or '*' in original_text if original_text else False
        has_dates = bool(re.search(r'\b(19|20)\d{2}\b', text))
        
        if not has_dates:
            score -= 10
        if has_bullets:
            score += 5
        
        return max(10, min(100, score))
    
    def _calculate_structure_score(self, text: str, original_text: str = "") -> int:
        """Enhanced resume structure and formatting score."""
        score = 100
        sections_found = self._detect_sections(text)
        
        # Essential sections check
        essential_sections = ['contact', 'experience', 'education', 'skills']
        essential_found = sum(1 for section in essential_sections if section in sections_found)
        
        if essential_found == 4:
            structure_score = 100
        elif essential_found == 3:
            structure_score = 85
        elif essential_found == 2:
            structure_score = 70
        else:
            structure_score = 50
        
        # Check for chronological order (dates)
        date_pattern = r'\b(19|20)\d{2}\b|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{4}\b'
        dates_found = re.findall(date_pattern, text, re.IGNORECASE)
        if len(dates_found) >= 2:
            chronology_bonus = 10
        else:
            chronology_bonus = 0
        
        # Check for consistent formatting
        consistent_formatting = 0
        if re.search(r'university|college|bachelor|master|phd', text):
            consistent_formatting += 5
        if re.search(r'company|corporation|inc|ltd|llc', text):
            consistent_formatting += 5
        
        # Penalty for too many short lines (poor formatting)
        if original_text:
            lines = original_text.split('\n')
            short_lines = sum(1 for line in lines if 0 < len(line.strip()) < 3)
            if len(lines) > 0 and short_lines / len(lines) > 0.3:
                formatting_penalty = 15
            else:
                formatting_penalty = 0
        else:
            formatting_penalty = 0
        
        final_score = structure_score + chronology_bonus + consistent_formatting - formatting_penalty
        return max(20, min(100, final_score))
    
    def _calculate_completeness_score(self, text: str, original_text: str = "") -> int:
        """Enhanced completeness score calculation."""
        score = 100
        
        # Essential elements check
        essential_checks = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\(\d{3}\)\s?\d{3}[-.]?\d{4}',
            'experience_indicators': r'\b(experience|worked|developed|managed|led|created|built)\b',
            'education': r'\b(education|degree|university|college|bachelor|master|phd|diploma)\b',
            'skills': r'\b(skills|proficient|technologies|languages|expertise|competencies)\b',
            'timeframe': r'\b(19|20)\d{2}\b|\b(years?|months?)\b',
            'achievements': r'\b(achieved|accomplished|increased|improved|reduced|saved|generated)\b'
        }
        
        # Check each essential element
        for element, pattern in essential_checks.items():
            if not re.search(pattern, text, re.IGNORECASE):
                if element in ['email', 'phone']:
                    score -= 20
                elif element in ['experience_indicators', 'education', 'skills']:
                    score -= 15
                else:
                    score -= 10
        
        # Bonus for comprehensive content
        word_count = len(text.split())
        if word_count >= 400:
            completeness_bonus = 10
        elif word_count >= 300:
            completeness_bonus = 5
        else:
            completeness_bonus = 0
        
        final_score = score + completeness_bonus
        return max(15, min(100, final_score))
    
    def _generate_recommendations(
        self, 
        text: str, 
        original_text: str,
        skills: List[str], 
        overall_score: int,
        content_score: int,
        keyword_score: int,
        ats_score: int,
        structure_score: int,
        completeness_score: int
    ) -> List[str]:
        """Generate intelligent, prioritized recommendations."""
        recommendations = []
        word_count = len(text.split())
        
        # Content improvements
        if content_score < 70:
            if word_count < 300:
                recommendations.append(
                    "Expand your resume content. Add more details about your achievements, responsibilities, and impact in each role (aim for 400-800 words total)."
                )
            elif word_count > 1000:
                recommendations.append(
                    "Condense your resume content. Focus on the most relevant and impactful achievements (aim for 400-800 words total)."
                )
            
            action_verbs = self._extract_action_verbs(text)
            if len(action_verbs) < 5:
                recommendations.append(
                    "Use more powerful action verbs to describe your achievements. Examples: 'Led team of 10', 'Developed new system', 'Increased efficiency by 30%'."
                )
        
        # Keywords and skills
        if keyword_score < 70:
            recommendations.append(
                "Optimize your keyword usage. Include more industry-relevant terms and technical skills that match your target role."
            )
        
        if len(skills) < 8:
            recommendations.append(
                "Add more relevant skills to your resume. Include both technical skills (programming languages, tools) and soft skills (leadership, communication)."
            )
        
        # ATS compatibility
        if ats_score < 70:
            recommendations.append(
                "Improve ATS compatibility by using standard section headings (Experience, Education, Skills), avoiding complex formatting, and including contact information clearly."
            )
        
        # Structure improvements
        if structure_score < 70:
            recommendations.append(
                "Enhance your resume structure. Ensure you have clear sections for Contact Info, Professional Summary, Experience, Education, and Skills."
            )
            
            dates_found = re.findall(r'\b(19|20)\d{2}\b', text)
            if len(dates_found) < 2:
                recommendations.append(
                    "Include specific dates (years) for your work experience and education to show career progression clearly."
                )
        
        # Completeness improvements
        if completeness_score < 70:
            has_email = bool(re.search(r'@', text))
            has_quantified = bool(re.search(r'\d+%|\d+\+|increased|improved|reduced', text))
            
            if not has_email:
                recommendations.append(
                    "Ensure your contact information is complete and easily visible, including email address and phone number."
                )
            
            if not has_quantified:
                recommendations.append(
                    "Add quantified achievements with specific numbers, percentages, or metrics (e.g., 'Increased sales by 25%', 'Managed team of 15', '$2M budget')."
                )
        
        # Overall quality recommendations
        if overall_score < 60:
            recommendations.append(
                "Consider tailoring your resume for each job application by incorporating keywords and requirements from the specific job posting."
            )
        
        # Professional tips
        if overall_score >= 80:
            recommendations.append(
                "Your resume is strong! Consider creating multiple versions tailored for different types of roles or industries."
            )
        
        # Limit to top 6 recommendations and prioritize by impact
        return recommendations[:6] if recommendations else [
            "Great job! Your resume meets most best practices. Keep it updated with your latest achievements and tailor it for specific job applications."
        ]
