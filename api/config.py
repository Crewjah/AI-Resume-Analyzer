"""
Configuration settings for the AI Resume Analyzer
"""

# Application settings
APP_CONFIG = {
    'title': 'AI Resume Analyzer',
    'description': 'Professional resume analysis and optimization tool',
    'version': '2.0.0',
    'max_file_size_mb': 10
}

# Supported file types
SUPPORTED_FILE_TYPES = ['txt', 'pdf', 'docx']

# Analysis thresholds
SCORING_THRESHOLDS = {
    'ats_excellent': 80,
    'ats_good': 70,
    'ats_fair': 50,
    'skills_minimum': 5,
    'skills_good': 8,
    'word_count_min': 200,
    'word_count_max': 1000,
    'word_count_optimal_min': 300,
    'word_count_optimal_max': 800
}

# Skills categories and weights
SKILL_CATEGORIES = {
    'Programming': 0.25,
    'Web Technologies': 0.20,
    'Databases': 0.15,
    'Cloud & DevOps': 0.20,
    'Data Science': 0.15,
    'Other': 0.05
}

# Professional keywords for ATS scoring
PROFESSIONAL_KEYWORDS = [
    'experience', 'responsible', 'managed', 'developed', 'implemented',
    'achieved', 'improved', 'led', 'created', 'designed', 'collaborated',
    'supervised', 'coordinated', 'executed', 'optimized', 'delivered',
    'established', 'maintained', 'analyzed', 'strategic', 'innovative'
]

# Common resume sections
RESUME_SECTIONS = [
    'experience', 'education', 'skills', 'summary', 'objective',
    'projects', 'certifications', 'achievements', 'awards'
]

# Job matching settings
JOB_MATCHING = {
    'min_keyword_length': 3,
    'exclude_common_words': True,
    'max_keywords_display': 15
}

# Common words to exclude from job matching
COMMON_WORDS = {
    'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
    'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
    'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy',
    'did', 'does', 'let', 'put', 'say', 'she', 'too', 'use', 'will', 'work',
    'team', 'company', 'role', 'position', 'candidate', 'must', 'should',
    'able', 'with', 'have', 'this', 'that', 'they', 'from', 'would', 'there',
    'been', 'many', 'some', 'time', 'very', 'when', 'come', 'here', 'just',
    'like', 'long', 'make', 'over', 'such', 'take', 'than', 'them', 'well',
    'were', 'what', 'your', 'each', 'which', 'their', 'said', 'into', 'only',
    'other', 'after', 'first', 'good', 'great', 'right', 'think', 'where',
    'being', 'every', 'large', 'found', 'still', 'between', 'never', 'again',
    'change', 'small', 'group', 'world', 'public', 'general', 'important'
}

# UI Color scheme
COLORS = {
    'primary': '#4f46e5',
    'secondary': '#7c3aed',
    'success': '#059669',
    'warning': '#d97706',
    'error': '#dc2626',
    'info': '#0891b2'
}