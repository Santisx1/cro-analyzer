"""
Data processing module for GA4 and heatmap data
Handles data cleaning, transformation, and preparation for analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


class DataProcessor:
    """Process and clean conversion funnel data from various sources"""
    
    def __init__(self):
        """Initialize data processor"""
        self.events_data = None
        self.heatmap_data = None
        self.processed_funnel = None
    
    def load_ga4_events(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Load and validate GA4 event data
        
        Args:
            data: DataFrame with GA4 events
            
        Returns:
            Cleaned DataFrame
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        
        # Validate required columns
        required_cols = ['event_name', 'timestamp', 'user_id', 'event_value']
        if not all(col in data.columns for col in required_cols):
            raise ValueError(f"Missing required columns: {required_cols}")
        
        # Convert timestamp to datetime
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        # Remove duplicates
        data = data.drop_duplicates(subset=['user_id', 'event_name', 'timestamp'])
        
        self.events_data = data.reset_index(drop=True)
        return self.events_data
    
    def load_heatmap_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Load and validate heatmap data (clicks, scrolls, etc)
        
        Args:
            data: DataFrame with heatmap events
            
        Returns:
            Cleaned DataFrame
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        
        required_cols = ['page_url', 'interaction_type', 'timestamp', 'user_id']
        if not all(col in data.columns for col in required_cols):
            raise ValueError(f"Missing required columns: {required_cols}")
        
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        self.heatmap_data = data.reset_index(drop=True)
        return self.heatmap_data
    
    def build_conversion_funnel(
        self, 
        funnel_steps: List[str],
        time_window_hours: int = 24
    ) -> Dict:
        """
        Build conversion funnel from event data
        
        Args:
            funnel_steps: List of events in order (e.g., ['page_view', 'add_to_cart', 'purchase'])
            time_window_hours: Time window to track funnel completion
            
        Returns:
            Dictionary with funnel metrics
        """
        if self.events_data is None:
            raise ValueError("No events data loaded. Call load_ga4_events first")
        
        # Sort by user and timestamp
        df = self.events_data.sort_values(['user_id', 'timestamp'])
        
        funnel_metrics = {
            'steps': funnel_steps,
            'step_counts': {},
            'step_users': {},
            'conversion_rates': {},
            'drop_off_rates': {},
            'time_between_steps': {}
        }
        
        # Count users at each step
        for step in funnel_steps:
            step_data = df[df['event_name'] == step]
            unique_users = step_data['user_id'].nunique()
            funnel_metrics['step_counts'][step] = len(step_data)
            funnel_metrics['step_users'][step] = unique_users
        
        # Calculate conversion rates
        total_users = df['user_id'].nunique()
        prev_users = total_users
        
        for step in funnel_steps:
            current_users = funnel_metrics['step_users'][step]
            conversion_rate = (current_users / prev_users * 100) if prev_users > 0 else 0
            drop_off_rate = 100 - conversion_rate
            
            funnel_metrics['conversion_rates'][step] = round(conversion_rate, 2)
            funnel_metrics['drop_off_rates'][step] = round(drop_off_rate, 2)
            
            prev_users = current_users
        
        self.processed_funnel = funnel_metrics
        return funnel_metrics
    
    def identify_abandonment_points(self) -> List[Dict]:
        """
        Identify where users are dropping off
        
        Returns:
            List of abandonment points with details
        """
        if self.processed_funnel is None:
            raise ValueError("No funnel data processed. Call build_conversion_funnel first")
        
        abandonment_points = []
        funnel_steps = self.processed_funnel['steps']
        drop_off_rates = self.processed_funnel['drop_off_rates']
        
        for i, step in enumerate(funnel_steps):
            drop_off = drop_off_rates.get(step, 0)
            
            if drop_off > 20:  # Flag if more than 20% drop-off
                abandonment_points.append({
                    'step': step,
                    'position': i + 1,
                    'drop_off_rate': drop_off,
                    'severity': 'high' if drop_off > 50 else 'medium'
                })
        
        return sorted(abandonment_points, key=lambda x: x['drop_off_rate'], reverse=True)
    
    def get_summary_statistics(self) -> Dict:
        """
        Get summary statistics of processed data
        
        Returns:
            Dictionary with summary metrics
        """
        if self.events_data is None:
            raise ValueError("No events data loaded")
        
        return {
            'total_events': len(self.events_data),
            'unique_users': self.events_data['user_id'].nunique(),
            'date_range': {
                'start': str(self.events_data['timestamp'].min()),
                'end': str(self.events_data['timestamp'].max())
            },
            'events_per_user': round(len(self.events_data) / self.events_data['user_id'].nunique(), 2),
            'event_types': self.events_data['event_name'].nunique()
        }
