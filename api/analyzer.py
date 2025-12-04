"""Thin wrapper that re-exports the centralized ResumeAnalyzer from src package."""

from src.analyzer import ResumeAnalyzer

__all__ = ["ResumeAnalyzer"]