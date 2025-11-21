# AI Resume Analyzer Configuration

# Application Settings
APP_TITLE = "AI Resume Analyzer"
APP_DESCRIPTION = "Intelligent Resume Analysis with Machine Learning & NLP"
VERSION = "1.0.0"

# UI Configuration
THEME = {
    "primary_color": "#667eea",
    "secondary_color": "#764ba2",
    "accent_color": "#f093fb",
    "success_color": "#0be881",
    "warning_color": "#feca57",
    "error_color": "#ff6b6b",
    "background_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
}

# Analysis Settings
DEFAULT_ANALYSIS_DEPTH = 3
MAX_FILE_SIZE_MB = 10
SUPPORTED_FILE_TYPES = ['pdf', 'docx', 'txt']

# Skill Categories Configuration
SKILL_WEIGHTS = {
    "Programming Languages": 0.25,
    "Frameworks & Libraries": 0.20,
    "Databases": 0.15,
    "Cloud & DevOps": 0.15,
    "Data Science & AI": 0.15,
    "Soft Skills": 0.10
}

# ATS Scoring Configuration
ATS_WEIGHTS = {
    "skills_diversity": 0.25,
    "section_completeness": 0.20,
    "keyword_density": 0.20,
    "format_quality": 0.15,
    "length_appropriateness": 0.10,
    "contact_information": 0.10
}

# Recommendation Categories
RECOMMENDATION_PRIORITIES = {
    "High": ["ats_compatibility", "job_alignment", "missing_sections"],
    "Medium": ["skill_enhancement", "format_improvement", "keyword_optimization"],
    "Low": ["minor_suggestions", "style_improvements"]
}

# Industry-Specific Keywords
INDUSTRY_KEYWORDS = {
    "Technology": [
        "software development", "programming", "coding", "algorithms", "data structures",
        "API", "database", "cloud computing", "DevOps", "agile", "scrum"
    ],
    "Finance": [
        "financial analysis", "investment", "portfolio management", "risk assessment",
        "compliance", "audit", "financial modeling", "Excel", "SQL", "Bloomberg"
    ],
    "Healthcare": [
        "patient care", "medical records", "HIPAA", "clinical research", "healthcare",
        "medical terminology", "patient safety", "EMR", "EHR", "clinical trials"
    ],
    "Marketing": [
        "digital marketing", "SEO", "SEM", "content marketing", "social media",
        "brand management", "campaign management", "analytics", "conversion optimization"
    ],
    "Education": [
        "curriculum development", "lesson planning", "student assessment", "classroom management",
        "educational technology", "learning management systems", "pedagogy", "instruction"
    ]
}

# Chart Configuration
CHART_CONFIG = {
    "default_height": 400,
    "default_width": 600,
    "color_scheme": "viridis",
    "font_family": "Poppins",
    "animation_duration": 800
}

# File Processing Limits
MAX_TEXT_LENGTH = 50000
MIN_TEXT_LENGTH = 100
MAX_SKILLS_TO_DISPLAY = 20
MAX_KEYWORDS_TO_DISPLAY = 30