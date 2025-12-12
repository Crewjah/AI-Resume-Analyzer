"""
Legacy configuration moved to `src/config.py`. Kept for reference.
"""
try:
    from src.config import APP_CONFIG, SUPPORTED_FILE_TYPES, SCORING_THRESHOLDS  # type: ignore
except Exception:
    APP_CONFIG = {
        'title': 'AI Resume Analyzer (legacy)',
        'description': 'Legacy config. Use src/config.py for canonical settings.'
    }
    SUPPORTED_FILE_TYPES = ['txt', 'pdf', 'docx']
    SCORING_THRESHOLDS = {}
