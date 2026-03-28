"""
Supabase Integration for CRO Examples and Competitor Insights
Store and retrieve visual examples, competitor analyses, and recommendations
"""

from typing import Dict, List, Optional
import json


class SupabaseExamplesManager:
    """Manage CRO examples and competitor insights in Supabase"""
    
    def __init__(self, supabase_url: Optional[str] = None, supabase_key: Optional[str] = None):
        """
        Initialize Supabase connection
        
        Args:
            supabase_url: Supabase project URL
            supabase_key: Supabase public key
        """
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.client = None
        
        if supabase_url and supabase_key:
            self._init_client()
    
    def _init_client(self):
        """Initialize Supabase client"""
        try:
            from supabase import create_client
            self.client = create_client(self.supabase_url, self.supabase_key)
            print("✅ Supabase connected successfully")
        except ImportError:
            print("⚠️  Supabase client not installed. Run: pip install supabase")
        except Exception as e:
            print(f"⚠️  Could not connect to Supabase: {e}")
    
    def store_example(
        self,
        recommendation_id: str,
        title: str,
        description: str,
        example_type: str,  # 'good' | 'bad' | 'competitor'
        image_url: Optional[str] = None,
        video_url: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Store a CRO example in Supabase
        
        Args:
            recommendation_id: Linked recommendation ID
            title: Example title
            description: Example description
            example_type: Type of example
            image_url: URL to example image
            video_url: URL to example video
            metadata: Additional metadata
            
        Returns:
            True if successful
        """
        if not self.client:
            print("❌ Supabase client not initialized")
            return False
        
        try:
            data = {
                'recommendation_id': recommendation_id,
                'title': title,
                'description': description,
                'type': example_type,
                'image_url': image_url,
                'video_url': video_url,
                'metadata': json.dumps(metadata or {}),
                'created_at': 'now()'
            }
            
            response = self.client.table('cro_examples').insert(data).execute()
            return bool(response.data)
        except Exception as e:
            print(f"❌ Error storing example: {e}")
            return False
    
    def get_examples_for_recommendation(
        self,
        recommendation_id: str,
        example_type: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve examples for a recommendation
        
        Args:
            recommendation_id: Recommendation ID
            example_type: Filter by type (optional)
            
        Returns:
            List of examples
        """
        if not self.client:
            return []
        
        try:
            query = self.client.table('cro_examples').select('*').eq('recommendation_id', recommendation_id)
            
            if example_type:
                query = query.eq('type', example_type)
            
            response = query.execute()
            return response.data
        except Exception as e:
            print(f"⚠️  Error retrieving examples: {e}")
            return []
    
    def store_competitor_analysis(
        self,
        competitor_name: str,
        website_url: str,
        strengths: List[str],
        weaknesses: List[str],
        insights: str,
        image_url: Optional[str] = None,
        cro_score: Optional[float] = None
    ) -> bool:
        """
        Store competitor analysis in Supabase
        
        Args:
            competitor_name: Competitor name
            website_url: Competitor website
            strengths: List of strengths
            weaknesses: List of weaknesses
            insights: Key insights
            image_url: Screenshot URL
            cro_score: CRO score (0-100)
            
        Returns:
            True if successful
        """
        if not self.client:
            print("❌ Supabase client not initialized")
            return False
        
        try:
            data = {
                'name': competitor_name,
                'website_url': website_url,
                'strengths': json.dumps(strengths),
                'weaknesses': json.dumps(weaknesses),
                'insights': insights,
                'screenshot_url': image_url,
                'cro_score': cro_score,
                'created_at': 'now()'
            }
            
            response = self.client.table('competitor_analysis').insert(data).execute()
            return bool(response.data)
        except Exception as e:
            print(f"❌ Error storing competitor analysis: {e}")
            return False
    
    def get_competitor_insights(
        self,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get latest competitor insights
        
        Args:
            limit: Number of records to retrieve
            
        Returns:
            List of competitor analyses
        """
        if not self.client:
            return []
        
        try:
            response = self.client.table('competitor_analysis').select('*').order(
                'created_at', desc=True
            ).limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"⚠️  Error retrieving competitors: {e}")
            return []
    
    def upload_image(
        self,
        file_path: str,
        bucket_name: str = 'cro-examples'
    ) -> Optional[str]:
        """
        Upload image to Supabase Storage
        
        Args:
            file_path: Local file path
            bucket_name: Storage bucket name
            
        Returns:
            Public URL if successful
        """
        if not self.client:
            return None
        
        try:
            with open(file_path, 'rb') as f:
                file_name = file_path.split('/')[-1]
                response = self.client.storage.from_(bucket_name).upload(
                    file_name,
                    f.read()
                )
            
            # Generate public URL
            public_url = self.client.storage.from_(bucket_name).get_public_url(file_name)
            return public_url
        except Exception as e:
            print(f"⚠️  Error uploading image: {e}")
            return None


# Example SQL schema for Supabase

SUPABASE_SCHEMA = """
-- CRO Examples table
CREATE TABLE cro_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recommendation_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    type TEXT NOT NULL CHECK (type IN ('good', 'bad', 'competitor')),
    image_url TEXT,
    video_url TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Competitor Analysis table
CREATE TABLE competitor_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    website_url TEXT,
    strengths JSONB,
    weaknesses JSONB,
    insights TEXT,
    screenshot_url TEXT,
    cro_score NUMERIC,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- CRO Reports table
CREATE TABLE cro_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_name TEXT NOT NULL,
    report_data JSONB NOT NULL,
    total_conversion_rate NUMERIC,
    critical_issues INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE cro_examples ENABLE ROW LEVEL SECURITY;
ALTER TABLE competitor_analysis ENABLE ROW LEVEL SECURITY;
ALTER TABLE cro_reports ENABLE ROW LEVEL SECURITY;

-- Create public policies (adjust as needed)
CREATE POLICY "public_read" ON cro_examples FOR SELECT USING (true);
CREATE POLICY "public_read_competitor" ON competitor_analysis FOR SELECT USING (true);
"""
