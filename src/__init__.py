"""
CRO Analysis Package
Automated Conversion Rate Optimization analysis and recommendations
"""

__version__ = "1.0.0"
__author__ = "CRO Analysis Team"

from .analyzer import CROAnalyzer
from .data_processor import DataProcessor
from .recommendations import RecommendationEngine

__all__ = [
    "CROAnalyzer",
    "DataProcessor", 
    "RecommendationEngine",
]
