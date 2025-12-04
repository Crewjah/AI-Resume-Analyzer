"""
Resume analysis engine with skills detection and scoring (centralized)
"""
import re
from typing import Dict, List, Any
import io

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    from docx import Document
except ImportError:
    Document = None


class ResumeAnalyzer:
    def __init__(self):
        self.skills_database = [
            # Programming Languages
            "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "PHP", "Ruby", "Go", "Swift", "Kotlin", "Rust",
            # Web Technologies
            "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask", "FastAPI", "Laravel",
            # Databases
            "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle", "Cassandra", "DynamoDB",
            # Cloud & DevOps
            "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "Git", "GitHub", "GitLab", "CI/CD",
            # Data Science & AI
            "Machine Learning", "Data Analysis", "Pandas", "NumPy", "TensorFlow", "PyTorch", "Scikit-learn",
            # Mobile Development
            "React Native", "Flutter", "Android", "iOS", "Xamarin",
            # Other Technologies
            "Linux", "REST API", "GraphQL", "Microservices", "Agile", "Scrum", "Apache", "Nginx"
        ]
        # Minimum number of words to consider a file a valid resume
        self.MIN_WORD_COUNT = 50

    def extract_text_from_file(self, uploaded_file) -> str:
        """Extract text from uploaded file"""
        try:
            # Support: file path (str), Flask FileStorage (.content_type), Streamlit UploadedFile (.type), or file-like
            if isinstance(uploaded_file, str):
                with open(uploaded_file, 'rb') as f:
                    data = f.read()
                if uploaded_file.lower().endswith('.pdf'):
                    return self._extract_pdf_text(io.BytesIO(data))
                elif uploaded_file.lower().endswith('.docx'):
                    return self._extract_docx_text(io.BytesIO(data))
                else:
                    return data.decode('utf-8', errors='ignore')

            content_type = getattr(uploaded_file, 'content_type', None) or getattr(uploaded_file, 'type', None)

            raw = None
            try:
                raw = uploaded_file.read()
            except Exception:
                stream = getattr(uploaded_file, 'stream', None)
                if stream:
                    raw = stream.read()

            if raw is None:
                return ''

            if isinstance(raw, bytes):
                b = io.BytesIO(raw)
            else:
                return str(raw)

            if content_type and 'pdf' in content_type:
                return self._extract_pdf_text(b)
            if content_type and ('word' in content_type or 'officedocument' in content_type or 'docx' in content_type):
                return self._extract_docx_text(b)

            filename = getattr(uploaded_file, 'name', '') or getattr(uploaded_file, 'filename', '')
            if isinstance(filename, str):
                if filename.lower().endswith('.pdf'):
                    return self._extract_pdf_text(b)
                if filename.lower().endswith('.docx'):
                    return self._extract_docx_text(b)

            try:
                return b.getvalue().decode('utf-8', errors='ignore')
            except Exception:
                return ''

        except Exception as e:
            return f"Error reading file: {str(e)}"

    def detect_skills(self, text: str) -> List[Dict[str, Any]]:
        """Detect skills mentioned in the text"""
        found_skills = []
        # Use word-boundary aware matching to avoid substring false positives
        for skill in self.skills_database:
            try:
                # Escape skill for regex and allow variations like dots or +
                pattern = r"\b" + re.escape(skill) + r"\b"
                matches = re.findall(pattern, text, flags=re.IGNORECASE)
                count = len(matches)
            except Exception:
                # Fallback to simple in-check
                count = text.lower().count(skill.lower())

            if count:
                found_skills.append({
                    'name': skill,
                    'count': count,
                    'category': self._get_skill_category(skill)
                })

        # Sort by frequency
        found_skills.sort(key=lambda x: x['count'], reverse=True)
        return found_skills

    def _get_skill_category(self, skill: str) -> str:
        """Categorize skills"""
        programming_langs = ["Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "PHP", "Ruby", "Go", "Swift"]
        web_tech = ["HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask"]
        databases = ["SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite"]
        cloud_devops = ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "Git"]

        if skill in programming_langs:
            return "Programming"
        elif skill in web_tech:
            return "Web Technologies"
        elif skill in databases:
            return "Databases"
        elif skill in cloud_devops:
            return "Cloud & DevOps"
        else:
            return "Other"

    def calculate_ats_score(self, text: str, skills: List[Dict]) -> int:
        """Calculate ATS compatibility score"""
        score = 0
        word_count = len(text.split())

        # Skills diversity (40 points)
        skill_count = len(skills)
        if skill_count >= 10:
            score += 40
        elif skill_count >= 6:
            score += 30
        elif skill_count >= 3:
            score += 20
        else:
            score += 10

        # Content length (20 points)
        if 300 <= word_count <= 800:
            score += 20
        elif 200 <= word_count <= 1000:
            score += 15
        else:
            score += 10

        # Professional keywords (20 points)
        professional_keywords = [
            "experience", "responsible", "managed", "developed", "implemented",
            "achieved", "improved", "led", "created", "designed", "collaborated"
        ]
        keyword_count = sum(1 for keyword in professional_keywords if keyword in text.lower())
        score += min(20, keyword_count * 2)

        # Contact information (10 points)
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            score += 5
        if re.search(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text):
            score += 5

        # Structure indicators (10 points)
        sections = ["experience", "education", "skills", "summary", "objective"]
        section_count = sum(1 for section in sections if section in text.lower())
        score += min(10, section_count * 2)

        return min(100, score)

    def extract_experience_years(self, text: str) -> int:
        """Extract years of experience from text"""
        patterns = [
            r'(\d+)[\+\s]*(?:years?|yrs?)[\s]*(?:of\s*)?(?:experience|exp)',
            r'(\d+)[\+\s]*(?:year|yr)[\s]*(?:of\s*)?(?:experience|exp)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))

        return 0

    def analyze_job_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze how well resume matches job description"""
        if not job_description.strip():
            return {
                'match_score': 0,
                'matched_keywords': [],
                'missing_keywords': [],
                'total_job_keywords': 0
            }

        # Clean and tokenize text
        resume_words = set(word.lower() for word in resume_text.split() if word.isalpha() and len(word) > 3)
        job_words = set(word.lower() for word in job_description.split() if word.isalpha() and len(word) > 3)

        # Filter relevant keywords (avoid common words)
        common_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our',
            'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two',
            'who', 'boy', 'did', 'does', 'let', 'put', 'say', 'she', 'too', 'use', 'will', 'work', 'team',
            'company', 'role', 'position', 'candidate', 'must', 'should', 'able', 'with', 'have', 'this',
            'that', 'they', 'from', 'would', 'there', 'been', 'many', 'some', 'time', 'very', 'when', 'come',
            'here', 'just', 'like', 'long', 'make', 'over', 'such', 'take', 'than', 'them', 'well', 'were'
        }

        job_keywords = job_words - common_words

        # Find matches
        matching_keywords = list(resume_words.intersection(job_keywords))
        missing_keywords = list(job_keywords - resume_words)

        # Calculate match score
        if job_keywords:
            match_score = int((len(matching_keywords) / len(job_keywords)) * 100)
        else:
            match_score = 0

        return {
            'match_score': match_score,
            'matched_keywords': matching_keywords[:15],  # Top 15
            'missing_keywords': missing_keywords[:15],    # Top 15
            'total_job_keywords': len(job_keywords)
        }

    def validate_resume_text(self, text: str) -> Dict[str, Any]:
        """Validate extracted text to determine if it's a likely resume.

        Returns a dict: { 'valid': bool, 'reason': str }
        """
        if not text or not isinstance(text, str):
            return {'valid': False, 'reason': 'No text extracted from file.'}

        # If extractor returned an error message, treat as invalid
        lowered = text.strip().lower()
        if lowered.startswith('error') or ('requires' in lowered and ('py' in lowered or 'library' in lowered)):
            return {'valid': False, 'reason': 'File could not be processed or required libraries are missing.'}

        # Count words
        words = [w for w in re.findall(r"[A-Za-z0-9]+", text) if len(w) > 1]
        word_count = len(words)
        if word_count < self.MIN_WORD_COUNT:
            return {'valid': False, 'reason': f'Content too short ({word_count} words); not a valid resume.'}

        return {'valid': True, 'reason': ''}

    def generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations based on analysis"""
        recommendations = []

        # ATS Score recommendations
        if analysis_results['ats_score'] < 60:
            recommendations.append("Improve ATS compatibility by adding more relevant technical skills and keywords")

        # Skills recommendations
        skill_count = len(analysis_results['skills'])
        if skill_count < 5:
            recommendations.append("Add more technical skills relevant to your target role")
        elif skill_count < 8:
            recommendations.append("Consider adding more diverse skills to strengthen your profile")

        # Content length recommendations
        word_count = analysis_results['word_count']
        if word_count < 200:
            recommendations.append("Expand your resume with more detailed job descriptions and achievements")
        elif word_count > 1000:
            recommendations.append("Consider condensing your resume for better readability")

        # Job matching recommendations
        if 'job_analysis' in analysis_results and analysis_results['job_analysis']:
            match_score = analysis_results['job_analysis']['match_score']
            if match_score < 40:
                recommendations.append("Incorporate more keywords from the job description to improve relevance")
            elif match_score < 60:
                recommendations.append("Add some missing keywords naturally into your experience descriptions")

        # Experience recommendations
        if analysis_results['experience_years'] == 0:
            recommendations.append("Clearly mention your years of experience in your summary or job titles")

        # Default positive message
        if not recommendations:
            recommendations.append("Your resume looks well-structured! Keep it updated with recent skills and achievements")

        return recommendations

    def analyze_resume(self, resume_text: str, job_description: str = "") -> Dict[str, Any]:
        """Perform comprehensive resume analysis"""
        # Validate resume text
        validation = self.validate_resume_text(resume_text)
        if not validation.get('valid'):
            return {
                'valid': False,
                'message': validation.get('reason', 'Invalid resume content'),
                'word_count': len(resume_text.split()),
                'skills': {},
                'skill_count': 0,
                'keywords': [],
                'ats_score': 0,
                'experience_years': 0,
                'job_analysis': None,
                'recommendations': ["Please upload a valid resume (PDF, DOCX, or plain text) with more content."]
            }

        # Basic metrics
        word_count = len(resume_text.split())

        # Skills analysis
        skills = self.detect_skills(resume_text)

        # ATS score
        ats_score = self.calculate_ats_score(resume_text, skills)

        # Experience extraction
        experience_years = self.extract_experience_years(resume_text)

        # Job matching
        job_analysis = self.analyze_job_match(resume_text, job_description)

        # Extract professional keywords
        keywords = self._extract_keywords(resume_text)

        # Compile results
        results = {
            'word_count': word_count,
            'skills': self._format_skills_for_display(skills[:20]),  # Top 20 skills
            'skill_count': len(skills),
            'keywords': keywords,
            'ats_score': ats_score,
            'experience_years': experience_years,
            'job_analysis': job_analysis if job_description else None
        }

        # Generate recommendations
        results['recommendations'] = self.generate_recommendations(results)

        return results

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract professional keywords from text"""
        professional_keywords = [
            "leadership", "management", "communication", "problem-solving", "teamwork",
            "project management", "strategic planning", "budget management", "training",
            "analysis", "research", "development", "implementation", "optimization",
            "collaboration", "mentoring", "negotiation", "presentation", "documentation"
        ]

        found_keywords = []
        text_lower = text.lower()

        for keyword in professional_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword.title())

        return found_keywords[:10]  # Top 10 keywords

    def _format_skills_for_display(self, skills: List[Dict]) -> Dict[str, List[str]]:
        """Format skills data for UI display"""
        formatted_skills = {}

        for skill in skills:
            category = skill.get('category', 'Other')
            if category not in formatted_skills:
                formatted_skills[category] = []
            formatted_skills[category].append(skill['name'])

        return formatted_skills

    def _extract_pdf_text(self, uploaded_file) -> str:
        """Extract text from PDF file"""
        if PyPDF2 is None:
            return "PDF processing requires PyPDF2 library. Please install it or use TXT files."

        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""

            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

            return text.strip()

        except Exception as e:
            return f"Error reading PDF file: {str(e)}. Please try a different file or format."

    def _extract_docx_text(self, uploaded_file) -> str:
        """Extract text from DOCX file"""
        if Document is None:
            return "DOCX processing requires python-docx library. Please install it or use TXT files."

        try:
            doc = Document(io.BytesIO(uploaded_file.read()))
            text = ""

            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

            return text.strip()

        except Exception as e:
            return f"Error reading DOCX file: {str(e)}. Please try a different file or format."
