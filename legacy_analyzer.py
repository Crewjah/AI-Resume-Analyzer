"""
Legacy analyzer moved to `src/analyzer.py`. Kept for reference.
"""
from typing import Any

# This file intentionally re-exports the canonical analyzer if available.
try:
    from src.analyzer import ResumeAnalyzer  # type: ignore
except Exception:
    # Fallback minimal shim for compatibility
    class ResumeAnalyzer:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("Use src.analyzer.ResumeAnalyzer; legacy analyzer not available in this environment")
