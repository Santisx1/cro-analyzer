"""
Unit tests for CRO Analyzer
"""

import sys
import os
import pytest
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from analyzer import CROAnalyzer


class TestCROAnalyzer:
    """Test CRO Analyzer functionality"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample event data for testing"""
        data = {
            'event_name': [
                'page_view', 'view_item', 'add_to_cart', 'begin_checkout', 'purchase',
                'page_view', 'view_item', 'add_to_cart',
                'page_view', 'view_item'
            ],
            'timestamp': pd.date_range('2024-03-20', periods=10, freq='H'),
            'user_id': ['u1', 'u1', 'u1', 'u1', 'u1', 'u2', 'u2', 'u2', 'u3', 'u3'],
            'event_value': [0, 10, 15, 15, 99.99, 0, 12, 12, 0, 8],
            'page_url': ['/', '/product/1', '/cart', '/checkout', '/confirmation',
                        '/', '/product/2', '/cart', '/', '/product/3']
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return CROAnalyzer()
    
    @pytest.fixture
    def funnel_steps(self):
        """Standard funnel steps"""
        return ['page_view', 'view_item', 'add_to_cart', 'begin_checkout', 'purchase']
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer can be initialized"""
        assert analyzer is not None
        assert analyzer.data_processor is not None
        assert analyzer.recommendation_engine is not None
    
    def test_analysis_execution(self, analyzer, sample_data, funnel_steps):
        """Test complete analysis execution"""
        results = analyzer.analyze(
            events_data=sample_data,
            funnel_steps=funnel_steps
        )
        
        assert results is not None
        assert 'timestamp' in results
        assert 'summary' in results
        assert 'funnel_metrics' in results
        assert 'abandonment_points' in results
        assert 'recommendations' in results
    
    def test_conversion_rate_calculation(self, analyzer, sample_data, funnel_steps):
        """Test conversion rate is calculated correctly"""
        results = analyzer.analyze(
            events_data=sample_data,
            funnel_steps=funnel_steps
        )
        
        # Check conversion rates exist and are reasonable
        conversion_rates = results['funnel_metrics']['conversion_rates']
        assert len(conversion_rates) > 0
        
        # All should be between 0 and 100
        for rate in conversion_rates.values():
            assert 0 <= rate <= 100
    
    def test_abandonment_point_identification(self, analyzer, sample_data, funnel_steps):
        """Test abandonment points are identified"""
        results = analyzer.analyze(
            events_data=sample_data,
            funnel_steps=funnel_steps
        )
        
        abandonment = results['abandonment_points']
        
        # Should have some abandonment points
        assert len(abandonment) > 0
        
        # Each point should have required fields
        for point in abandonment:
            assert 'step' in point
            assert 'drop_off_rate' in point
            assert 'severity' in point
            assert point['drop_off_rate'] > 0
    
    def test_recommendations_generation(self, analyzer, sample_data, funnel_steps):
        """Test recommendations are generated"""
        results = analyzer.analyze(
            events_data=sample_data,
            funnel_steps=funnel_steps
        )
        
        recommendations = results['recommendations']
        
        # Should have recommendations
        assert len(recommendations) > 0
        
        # Each should have required fields
        for rec in recommendations:
            assert 'title' in rec
            assert 'actions' in rec
            assert 'priority' in rec
            assert len(rec['actions']) > 0
    
    def test_summary_statistics(self, analyzer, sample_data, funnel_steps):
        """Test summary statistics are generated"""
        results = analyzer.analyze(
            events_data=sample_data,
            funnel_steps=funnel_steps
        )
        
        summary = results['summary']
        
        assert summary['total_events'] == 10
        assert summary['unique_users'] == 3
        assert 'date_range' in summary
        assert 'events_per_user' in summary
    
    def test_invalid_data_handling(self, analyzer):
        """Test handling of invalid data"""
        invalid_data = pd.DataFrame({
            'wrong_column': [1, 2, 3]
        })
        
        with pytest.raises(ValueError):
            analyzer.analyze(
                events_data=invalid_data,
                funnel_steps=['page_view', 'purchase']
            )
    
    def test_get_analysis_results(self, analyzer, sample_data, funnel_steps):
        """Test retrieving analysis results"""
        analyzer.analyze(
            events_data=sample_data,
            funnel_steps=funnel_steps
        )
        
        results = analyzer.get_analysis_results()
        assert results is not None
        assert len(results) > 0


class TestDataProcessor:
    """Test Data Processor functionality"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data"""
        data = {
            'event_name': ['page_view', 'add_to_cart', 'purchase'],
            'timestamp': pd.date_range('2024-03-20', periods=3, freq='H'),
            'user_id': ['u1', 'u1', 'u1'],
            'event_value': [0, 50, 100],
            'page_url': ['/', '/cart', '/confirmation']
        }
        return pd.DataFrame(data)
    
    def test_data_processor_loading(self, sample_data):
        """Test data processor can load data"""
        from data_processor import DataProcessor
        
        processor = DataProcessor()
        loaded_data = processor.load_ga4_events(sample_data)
        
        assert loaded_data is not None
        assert len(loaded_data) == 3
    
    def test_funnel_building(self, sample_data):
        """Test funnel building"""
        from data_processor import DataProcessor
        
        processor = DataProcessor()
        processor.load_ga4_events(sample_data)
        
        funnel = processor.build_conversion_funnel(
            ['page_view', 'add_to_cart', 'purchase']
        )
        
        assert 'steps' in funnel
        assert 'conversion_rates' in funnel
        assert 'drop_off_rates' in funnel


class TestRecommendationEngine:
    """Test Recommendation Engine"""
    
    def test_recommendation_generation(self):
        """Test recommendations are generated correctly"""
        from recommendations import RecommendationEngine
        
        engine = RecommendationEngine()
        
        # Mock funnel metrics
        funnel_metrics = {
            'steps': ['page_view', 'add_to_cart', 'purchase'],
            'conversion_rates': {
                'page_view': 100,
                'add_to_cart': 50,
                'purchase': 40
            },
            'drop_off_rates': {
                'page_view': 0,
                'add_to_cart': 50,
                'purchase': 60
            }
        }
        
        abandonment = [
            {'step': 'add_to_cart', 'drop_off_rate': 50, 'severity': 'high'}
        ]
        
        recommendations = engine.generate_recommendations(
            funnel_metrics, abandonment
        )
        
        assert len(recommendations) > 0
        assert recommendations[0]['priority'] in ['high', 'medium', 'low']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
