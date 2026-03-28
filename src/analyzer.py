"""
Main CRO Analysis Engine
Coordinates analysis, data processing, and recommendation generation
"""

from typing import Dict, List, Optional
import json
import sys
from pathlib import Path

# Ensure relative imports work
try:
    from .data_processor import DataProcessor
    from .recommendations import RecommendationEngine
except ImportError:
    from data_processor import DataProcessor
    from recommendations import RecommendationEngine


class CROAnalyzer:
    """Main CRO analysis orchestrator"""
    
    def __init__(self):
        """Initialize CRO analyzer"""
        self.data_processor = DataProcessor()
        self.recommendation_engine = RecommendationEngine()
        self.analysis_results = {}
    
    def analyze(
        self,
        events_data,
        funnel_steps: List[str],
        heatmap_data=None,
        time_window_hours: int = 24
    ) -> Dict:
        """
        Run complete CRO analysis
        
        Args:
            events_data: GA4 events data
            funnel_steps: List of conversion funnel steps
            heatmap_data: Optional heatmap data
            time_window_hours: Time window for analysis
            
        Returns:
            Complete analysis results
        """
        # Process data
        self.data_processor.load_ga4_events(events_data)
        if heatmap_data is not None:
            self.data_processor.load_heatmap_data(heatmap_data)
        
        # Build funnel
        funnel_metrics = self.data_processor.build_conversion_funnel(
            funnel_steps,
            time_window_hours
        )
        
        # Identify problems
        abandonment_points = self.data_processor.identify_abandonment_points()
        
        # Generate recommendations
        recommendations = self.recommendation_engine.generate_recommendations(
            funnel_metrics,
            abandonment_points
        )
        
        # Compile results
        self.analysis_results = {
            'timestamp': self._get_timestamp(),
            'summary': self.data_processor.get_summary_statistics(),
            'funnel_metrics': funnel_metrics,
            'abandonment_points': abandonment_points,
            'recommendations': recommendations,
            'total_conversion_rate': funnel_metrics['conversion_rates'].get(
                funnel_steps[-1], 0
            ) if funnel_steps else 0
        }
        
        return self.analysis_results
    
    def get_analysis_results(self) -> Dict:
        """Get latest analysis results"""
        return self.analysis_results
    
    def export_results(self, filename: str) -> None:
        """
        Export analysis results to JSON
        
        Args:
            filename: Output filename
        """
        if not self.analysis_results:
            raise ValueError("No analysis results to export")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
