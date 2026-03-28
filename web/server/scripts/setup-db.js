#!/usr/bin/env node

/**
 * Setup Supabase Database Tables
 * Cria schema necessário para o CRO Analyzer
 */

import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

dotenv.config();

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY;

if (!SUPABASE_URL || !SUPABASE_SERVICE_KEY) {
  console.error('❌ SUPABASE_URL e SUPABASE_SERVICE_KEY são obrigatórios no .env');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

const SQL = `
-- Drop existing tables if needed
DROP TABLE IF EXISTS competitor_analysis CASCADE;
DROP TABLE IF EXISTS cro_examples CASCADE;
DROP TABLE IF EXISTS cro_reports CASCADE;

-- Main reports table
CREATE TABLE cro_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  analysis_data JSONB NOT NULL,
  funnel_steps TEXT[] NOT NULL,
  metrics JSONB,
  recommendations JSONB,
  summary TEXT,
  source TEXT DEFAULT 'web',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Examples table
CREATE TABLE cro_examples (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  recommendation_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  type TEXT,
  image_url TEXT,
  video_url TEXT,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Competitor analysis table
CREATE TABLE competitor_analysis (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  website_url TEXT,
  strengths TEXT[],
  weaknesses TEXT[],
  insights TEXT,
  screenshot_url TEXT,
  cro_score FLOAT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_cro_reports_created_at ON cro_reports(created_at DESC);
CREATE INDEX idx_cro_reports_source ON cro_reports(source);
CREATE INDEX idx_cro_examples_recommendation ON cro_examples(recommendation_id);
CREATE INDEX idx_competitor_cro_score ON competitor_analysis(cro_score DESC);

-- Enable RLS (Row Level Security)
ALTER TABLE cro_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE cro_examples ENABLE ROW LEVEL SECURITY;
ALTER TABLE competitor_analysis ENABLE ROW LEVEL SECURITY;

-- Create RLS policies (allow all for now, restrict later)
CREATE POLICY "Allow all access to cro_reports" ON cro_reports
  FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all access to cro_examples" ON cro_examples
  FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all access to competitor_analysis" ON competitor_analysis
  FOR ALL USING (true) WITH CHECK (true);

-- Grant permissions
GRANT ALL ON cro_reports TO anon, authenticated;
GRANT ALL ON cro_examples TO anon, authenticated;
GRANT ALL ON competitor_analysis TO anon, authenticated;
`;

async function setupDatabase() {
  console.log('🔧 Setup do Banco de Dados CRO Analyzer...\n');

  try {
    console.log('📌 Conectando ao Supabase...');
    const { error: authError } = await supabase.auth.getSession();
    console.log('✅ Conectado!\n');

    console.log('📋 Criando tabelas...');
    
    // Execute SQL using Supabase CLI or direct query
    // Since we can't execute raw SQL directly, we'll use the REST API approach
    
    const tables = [
      {
        name: 'cro_reports',
        columns: {
          id: 'uuid',
          analysis_data: 'jsonb',
          funnel_steps: 'text[]',
          metrics: 'jsonb',
          recommendations: 'jsonb',
          summary: 'text',
          source: 'text',
          created_at: 'timestamp',
          updated_at: 'timestamp'
        }
      },
      {
        name: 'cro_examples',
        columns: {
          id: 'uuid',
          recommendation_id: 'text',
          title: 'text',
          description: 'text',
          type: 'text',
          image_url: 'text',
          video_url: 'text',
          metadata: 'jsonb',
          created_at: 'timestamp'
        }
      },
      {
        name: 'competitor_analysis',
        columns: {
          id: 'uuid',
          name: 'text',
          website_url: 'text',
          strengths: 'text[]',
          weaknesses: 'text[]',
          insights: 'text',
          screenshot_url: 'text',
          cro_score: 'float8',
          created_at: 'timestamp'
        }
      }
    ];

    for (const table of tables) {
      console.log(`\n  📦 Criando tabela: ${table.name}`);
      
      // Test if table exists by trying to query it
      const { error: queryError } = await supabase
        .from(table.name)
        .select('*')
        .limit(1);

      if (queryError && queryError.code === 'PGRST116') {
        console.log(`     ⚠️  Tabela ${table.name} não existe`);
        console.log(`     ℹ️  Use o SQL abaixo no Supabase Editor:\n${SQL}`);
      } else if (!queryError) {
        console.log(`     ✅ Tabela ${table.name} já existe`);
      } else {
        console.log(`     ⚠️  Erro: ${queryError.message}`);
      }
    }

    console.log('\n✅ Setup completo!\n');
    
    console.log('📌 Próximos passos:');
    console.log('   1. Acesse: https://app.supabase.com/project/YOUR_PROJECT_ID/editor');
    console.log('   2. Cole o SQL acima em uma nova query');
    console.log('   3. Execute (Ctrl+Enter)');
    console.log('   4. Pronto!\n');

    console.log('💡 Ou use Supabase CLI:');
    console.log('   supabase db push\n');

  } catch (error) {
    console.error('❌ Erro:', error.message);
    process.exit(1);
  }
}

// Run setup
setupDatabase();
