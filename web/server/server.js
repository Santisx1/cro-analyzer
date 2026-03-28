import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import { createClient } from '@supabase/supabase-js';

// Setup
dotenv.config();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Supabase
const SUPABASE_URL = process.env.SUPABASE_URL || '';
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY || '';
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// ==========================================
// AUTHENTICATION ROUTES
// ==========================================

// Register
app.post('/api/auth/register', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email e senha são obrigatórios' });
    }

    const { data, error } = await supabase.auth.signUpWithPassword({
      email,
      password
    });

    if (error) {
      return res.status(400).json({ error: error.message });
    }

    return res.json({ 
      message: 'Usuário registrado com sucesso',
      user: data.user 
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

// Login
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email e senha são obrigatórios' });
    }

    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    });

    if (error) {
      return res.status(400).json({ error: error.message });
    }

    return res.json({
      message: 'Login bem-sucedido',
      session: data.session,
      user: data.user
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

// Verify token
app.post('/api/auth/verify', async (req, res) => {
  try {
    const { token } = req.body;

    if (!token) {
      return res.status(400).json({ error: 'Token obrigatório' });
    }

    const { data, error } = await supabase.auth.getUser(token);

    if (error) {
      return res.status(401).json({ error: 'Token inválido' });
    }

    return res.json({ user: data.user });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

// ==========================================
// ANALYSIS ROUTES
// ==========================================

// Get latest analysis
app.get('/api/analysis/latest', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('cro_reports')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(1)
      .single();

    if (error && error.code !== 'PGRST116') {
      return res.status(400).json({ error: error.message });
    }

    return res.json(data || null);
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

// Get all analyses
app.get('/api/analysis/history', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 10;
    const { data, error } = await supabase
      .from('cro_reports')
      .select('id, created_at, summary, metrics')
      .order('created_at', { ascending: false })
      .limit(limit);

    if (error) {
      return res.status(400).json({ error: error.message });
    }

    return res.json(data || []);
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

// Get analysis by ID
app.get('/api/analysis/:id', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('cro_reports')
      .select('*')
      .eq('id', req.params.id)
      .single();

    if (error) {
      return res.status(400).json({ error: error.message });
    }

    return res.json(data);
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

// Save analysis result
app.post('/api/analysis/save', async (req, res) => {
  try {
    const { analysis_data, funnel_steps, metrics, recommendations } = req.body;

    if (!analysis_data || !funnel_steps) {
      return res.status(400).json({ error: 'Dados obrigatórios faltando' });
    }

    const { data, error } = await supabase
      .from('cro_reports')
      .insert([{
        analysis_data,
        funnel_steps,
        metrics: metrics || {},
        recommendations: recommendations || [],
        summary: `Analysis - ${new Date().toLocaleString('pt-BR')}`,
        created_at: new Date().toISOString()
      }])
      .select()
      .single();

    if (error) {
      return res.status(400).json({ error: error.message });
    }

    return res.status(201).json(data);
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

// ==========================================
// RECOMMENDATIONS ROUTES
// ==========================================

// Get examples for recommendation
app.get('/api/examples/:recommendation_id', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('cro_examples')
      .select('*')
      .eq('recommendation_id', req.params.recommendation_id);

    if (error) {
      return res.status(400).json({ error: error.message });
    }

    return res.json(data || []);
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

// ==========================================
// COMPETITOR ANALYSIS ROUTES
// ==========================================

// Get competitor insights
app.get('/api/competitors', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('competitor_analysis')
      .select('*')
      .order('cro_score', { ascending: false });

    if (error) {
      return res.status(400).json({ error: error.message });
    }

    return res.json(data || []);
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

// ==========================================
// HEALTH CHECK
// ==========================================

app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Serve main page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/dashboard.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ CRO Analyzer Web rodando em http://localhost:${PORT}`);
  console.log(`   API: http://localhost:${PORT}/api`);
  console.log(`   Dashboard: http://localhost:${PORT}/dashboard`);
});

export { app, supabase };
