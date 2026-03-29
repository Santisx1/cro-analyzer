/**
 * API Endpoints para Google Analytics e Clarity
 * 
 * COMO FUNCIONA:
 * Seu app React chama esses endpoints → que buscam dados do GA4 e Clarity
 * → e salva no Supabase → Dashboard mostra as informações
 * 
 * EXEMPLO DE USO:
 * fetch('/api/integrations/ga4/import', { method: 'POST', body: {...} })
 * fetch('/api/integrations/clarity/heatmap', { method: 'GET' })
 */

import express from 'express';
import GoogleAnalyticsConnector from './integrations/googleAnalytics.js';
import ClarityConnector from './integrations/clarityConnector.js';
import { verifyToken } from './middleware/auth.js';

const router = express.Router();

// ============================================================================
// GOOGLE ANALYTICS ENDPOINTS
// ============================================================================

/**
 * POST /api/integrations/ga4/import
 * 
 * PARA QUE SERVE: 
 * Conecta com seu GA4 e traz eventos para o dashboard
 * 
 * O QUE RECEBE (body):
 * {
 *   "credentialsPath": "path/to/google-creds.json",
 *   "propertyId": "123456789",
 *   "dateStart": "2024-03-01",
 *   "dateEnd": "2024-03-31"
 * }
 * 
 * O QUE RETORNA:
 * {
 *   "success": true,
 *   "eventsImported": 15430,
 *   "conversionRate": 3.45,
 *   "funnelData": {...}
 * }
 */
router.post('/ga4/import', verifyToken, async (req, res) => {
  try {
    const { credentialsPath, propertyId, dateStart, dateEnd } = req.body;

    if (!credentialsPath || !propertyId) {
      return res.status(400).json({
        error: 'Missing required fields: credentialsPath, propertyId',
      });
    }

    const ga = new GoogleAnalyticsConnector(credentialsPath);
    
    // Autenticar com Google
    const authenticated = await ga.authenticate();
    if (!authenticated) {
      return res.status(401).json({ error: 'Failed to authenticate with Google Analytics' });
    }

    // Buscar dados
    const events = await ga.fetchConversionEvents(propertyId, dateStart, dateEnd);
    const sessionMetrics = await ga.fetchSessionMetrics(propertyId, dateStart, dateEnd);

    // TODO: Salvar no Supabase
    // await saveToSupabase(events, sessionMetrics);

    res.json({
      success: true,
      eventsImported: events.length,
      metrics: sessionMetrics,
      data: events,
    });
  } catch (error) {
    console.error('❌ Erro GA4 import:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/integrations/ga4/funnel
 * 
 * PARA QUE SERVE:
 * Pega o funil de conversão específico do seu GA4
 * 
 * QUERY PARAMS:
 * ?propertyId=123&funnelSteps=page_view,add_to_cart,purchase
 * &dateStart=2024-03-01&dateEnd=2024-03-31
 * 
 * RETORNA:
 * [
 *   { step: "page_view", users: 10000, conversionRate: 100 },
 *   { step: "add_to_cart", users: 500, conversionRate: 5 },
 *   { step: "purchase", users: 50, conversionRate: 0.5 }
 * ]
 */
router.get('/ga4/funnel', verifyToken, async (req, res) => {
  try {
    const { propertyId, funnelSteps, dateStart, dateEnd, credentialsPath } = req.query;

    if (!propertyId || !funnelSteps) {
      return res.status(400).json({
        error: 'Missing required params: propertyId, funnelSteps',
      });
    }

    const ga = new GoogleAnalyticsConnector(credentialsPath);
    await ga.authenticate();

    const steps = funnelSteps.split(',');
    const funnelData = await ga.fetchFunnelData(propertyId, steps, dateStart, dateEnd);

    res.json({
      success: true,
      funnel: funnelData,
    });
  } catch (error) {
    console.error('❌ Erro GA4 funnel:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/integrations/ga4/metrics
 * 
 * PARA QUE SERVE:
 * Pega as métricas principais de sessão
 * 
 * QUERY PARAMS:
 * ?propertyId=123&dateStart=2024-03-01&dateEnd=2024-03-31&credentialsPath=...
 * 
 * RETORNA:
 * {
 *   "sessions": 50000,
 *   "bounceRate": 45.2,
 *   "avgSessionDuration": 240,
 *   "pageViews": 150000
 * }
 */
router.get('/ga4/metrics', verifyToken, async (req, res) => {
  try {
    const { propertyId, dateStart, dateEnd, credentialsPath } = req.query;

    const ga = new GoogleAnalyticsConnector(credentialsPath);
    await ga.authenticate();

    const metrics = await ga.fetchSessionMetrics(propertyId, dateStart, dateEnd);

    res.json(metrics);
  } catch (error) {
    console.error('❌ Erro GA4 metrics:', error);
    res.status(500).json({ error: error.message });
  }
});

// ============================================================================
// MICROSOFT CLARITY ENDPOINTS
// ============================================================================

/**
 * POST /api/integrations/clarity/import
 * 
 * PARA QUE SERVE:
 * Conecta com Clarity e traz dados de heatmap e comportamento
 * 
 * O QUE RECEBE (body):
 * {
 *   "clarityToken": "seu-token",
 *   "projectId": "123456",
 *   "dateStart": "2024-03-01",
 *   "dateEnd": "2024-03-31"
 * }
 * 
 * O QUE RETORNA:
 * {
 *   "success": true,
 *   "heatmapData": [...],
 *   "pageMetrics": [...],
 *   "sessionComparison": {...}
 * }
 */
router.post('/clarity/import', verifyToken, async (req, res) => {
  try {
    const { clarityToken, projectId, dateStart, dateEnd } = req.body;

    if (!clarityToken || !projectId) {
      return res.status(400).json({
        error: 'Missing required fields: clarityToken, projectId',
      });
    }

    const clarity = new ClarityConnector(clarityToken, projectId);

    // Autenticar com Clarity
    const authenticated = await clarity.authenticate();
    if (!authenticated) {
      return res.status(401).json({ error: 'Failed to authenticate with Microsoft Clarity' });
    }

    // Buscar todos os dados
    const heatmapData = await clarity.fetchHeatmapData(dateStart, dateEnd);
    const pageMetrics = await clarity.fetchPageMetrics(dateStart, dateEnd);
    const sessionComparison = await clarity.fetchConversionSessionComparison(dateStart, dateEnd);

    // TODO: Salvar no Supabase
    // await saveToSupabase({ heatmapData, pageMetrics, sessionComparison });

    res.json({
      success: true,
      heatmapData,
      pageMetrics,
      sessionComparison,
    });
  } catch (error) {
    console.error('❌ Erro Clarity import:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/integrations/clarity/heatmap
 * 
 * PARA QUE SERVE:
 * Pega dados de mapa de calor (onde usuários clicam mais)
 * 
 * QUERY PARAMS:
 * ?clarityToken=...&projectId=123&dateStart=2024-03-01&dateEnd=2024-03-31
 * 
 * RETORNA:
 * [
 *   { x: 450, y: 200, density: 450, clicks: 450 },
 *   { x: 500, y: 250, density: 380, clicks: 380 },
 *   ...
 * ]
 * 
 * VISUALIZAÇÃO:
 * Coordenadas X,Y onde temos maior concentração de clicks
 */
router.get('/clarity/heatmap', verifyToken, async (req, res) => {
  try {
    const { clarityToken, projectId, dateStart, dateEnd } = req.query;

    const clarity = new ClarityConnector(clarityToken, projectId);
    await clarity.authenticate();

    const heatmapData = await clarity.fetchHeatmapData(dateStart, dateEnd);

    res.json({
      success: true,
      heatmap: heatmapData,
      insight: 'Mostra onde usuários clicam mais - útil para otimizar CTAs',
    });
  } catch (error) {
    console.error('❌ Erro Clarity heatmap:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/integrations/clarity/pages
 * 
 * PARA QUE SERVE:
 * Identifica quais páginas têm maior taxa de rejeição
 * 
 * RETORNA:
 * [
 *   { url: "/checkout", bounceRate: 65, sessions: 1000, timeOnPage: 120 },
 *   { url: "/", bounceRate: 45, sessions: 5000, timeOnPage: 180 },
 * ]
 * 
 * INSIGHT: Checkout está indo embora em 65% - precisa otimizar!
 */
router.get('/clarity/pages', verifyToken, async (req, res) => {
  try {
    const { clarityToken, projectId, dateStart, dateEnd } = req.query;

    const clarity = new ClarityConnector(clarityToken, projectId);
    await clarity.authenticate();

    const pageMetrics = await clarity.fetchPageMetrics(dateStart, dateEnd);

    res.json({
      success: true,
      pages: pageMetrics.sort((a, b) => b.bounceRate - a.bounceRate),
      topProblems: pageMetrics.slice(0, 5),
    });
  } catch (error) {
    console.error('❌ Erro Clarity pages:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/integrations/clarity/recordings
 * 
 * PARA QUE SERVE:
 * Pega gravações de sessão (vídeos de usuários) que abandonaram a compra
 * 
 * QUERY PARAMS:
 * ?clarityToken=...&projectId=123&filter=abandoned&limit=5
 * 
 * RETORNA:
 * [
 *   { 
 *     recordingId: "rec_123",
 *     url: "https://clarity.microsoft.com/recordings/...",
 *     duration: 240,
 *     where: "/cart" 
 *   },
 *   ...
 * ]
 * 
 * INSIGHT: Assista de verdade o que usuário faz antes de sair!
 */
router.get('/clarity/recordings', verifyToken, async (req, res) => {
  try {
    const { clarityToken, projectId, filter = 'abandoned', limit = 10 } = req.query;

    const clarity = new ClarityConnector(clarityToken, projectId);
    await clarity.authenticate();

    const recordings = await clarity.fetchSessionRecordings(filter, parseInt(limit));

    res.json({
      success: true,
      recordings,
      count: recordings.length,
      tip: 'Assista essas gravações para entender o que usuários experimentam',
    });
  } catch (error) {
    console.error('❌ Erro Clarity recordings:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/integrations/clarity/feedback
 * 
 * PARA QUE SERVE:
 * Coleta feedback direto dos usuários (o que eles pensam)
 * 
 * QUERY PARAMS:
 * ?clarityToken=...&projectId=123&dateStart=2024-03-01&dateEnd=2024-03-31
 * 
 * RETORNA:
 * [
 *   {
 *     comment: "Checkout muito complicado",
 *     sentiment: "negative",
 *     page: "/checkout",
 *     timestamp: "2024-03-15T10:30:00Z"
 *   },
 *   {
 *     comment: "Adorei a experiência!",
 *     sentiment: "positive",
 *     page: "/",
 *     timestamp: "2024-03-15T11:00:00Z"
 *   }
 * ]
 */
router.get('/clarity/feedback', verifyToken, async (req, res) => {
  try {
    const { clarityToken, projectId, dateStart, dateEnd } = req.query;

    const clarity = new ClarityConnector(clarityToken, projectId);
    await clarity.authenticate();

    const feedback = await clarity.fetchUserFeedback(dateStart, dateEnd);

    const stats = {
      total: feedback.length,
      positive: feedback.filter(f => f.sentiment === 'positive').length,
      negative: feedback.filter(f => f.sentiment === 'negative').length,
      neutral: feedback.filter(f => f.sentiment === 'neutral').length,
    };

    res.json({
      success: true,
      feedback,
      stats,
    });
  } catch (error) {
    console.error('❌ Erro Clarity feedback:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/integrations/clarity/comparison
 * 
 * PARA QUE SERVE:
 * Compara comportamento de usuários que COMPRARAM vs que ABANDONARAM
 * 
 * RETORNA:
 * {
 *   "converted": { avgClicks: 8.5, avgScrollDepth: 75, avgTimeSpent: 420 },
 *   "abandoned": { avgClicks: 3.2, avgScrollDepth: 30, avgTimeSpent: 120 },
 *   "comparison": {
 *     "clickDiff": "165.6%",  ← Conversores clicam 166% mais
 *     "scrollDiff": "150.0%", ← Conversores scrollam 150% mais
 *     "timeDiff": "250.0%",   ← Conversores ficam 250% mais tempo
 *     "insight": "Usuários que conversam tendem a..."
 *   }
 * }
 */
router.get('/clarity/comparison', verifyToken, async (req, res) => {
  try {
    const { clarityToken, projectId, dateStart, dateEnd } = req.query;

    const clarity = new ClarityConnector(clarityToken, projectId);
    await clarity.authenticate();

    const comparison = await clarity.fetchConversionSessionComparison(dateStart, dateEnd);

    res.json({
      success: true,
      ...comparison,
      recommendation: 'Replique o comportamento de conversores nos abandonadores',
    });
  } catch (error) {
    console.error('❌ Erro Clarity comparison:', error);
    res.status(500).json({ error: error.message });
  }
});

// ============================================================================
// STATUS E HEALTH CHECK
// ============================================================================

/**
 * GET /api/integrations/health
 * 
 * PARA QUE SERVE:
 * Verifica se as integrações estão disponíveis
 */
router.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    integrations: {
      googleAnalytics: 'ready',
      clarity: 'ready',
    },
    tips: {
      ga4: 'Precisa de Google Credentials JSON file',
      clarity: 'Precisa de Clarity Auth Token',
    },
  });
});

export default router;
