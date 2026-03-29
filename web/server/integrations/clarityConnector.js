/**
 * Microsoft Clarity Integration
 * 
 * PARA QUE SERVE:
 * - Conecta com Microsoft Clarity para dados de heatmaps
 * - Importa mapas de calor, gravações de sessão, user feedback
 * - Ajuda a identificar onde usuários clicam e abandonam
 * 
 * FLUXO:
 * Seu site → Clarity tracking code → API daqui → Dashboard
 */

class ClarityConnector {
  constructor(clarityToken, projectId) {
    this.token = clarityToken;
    this.projectId = projectId;
    this.baseURL = 'https://www.clarity.microsoft.com/api/v1';
  }

  /**
   * Conectar e validar credenciais Clarity
   * 
   * Para que serve: Verifica se o token é válido
   * Retorna: true se autenticou, false se erro
   */
  async authenticate() {
    try {
      const response = await fetch(`${this.baseURL}/projects/${this.projectId}`, {
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        console.log('✅ Microsoft Clarity autenticado');
        return true;
      } else {
        console.error('❌ Token Clarity inválido');
        return false;
      }
    } catch (error) {
      console.error('❌ Erro conectar Clarity:', error);
      return false;
    }
  }

  /**
   * Buscar dados de heatmap (mapa de calor)
   * 
   * Para que serve: Mostra ONDE usuários clicam mais na página
   * Útil para: Identificar área principal de interesse
   * Retorna: Coordenadas x,y com densidade de cliques
   */
  async fetchHeatmapData(dateStart, dateEnd) {
    try {
      const response = await fetch(
        `${this.baseURL}/projects/${this.projectId}/heatmaps?` +
        `startDate=${dateStart}&endDate=${dateEnd}`,
        {
          headers: {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) throw new Error('Erro buscar heatmap');
      
      const data = await response.json();
      console.log(`✅ Heatmap com ${data.data?.length || 0} pontos encontrados`);
      return data.data || [];
    } catch (error) {
      console.error('❌ Erro buscar heatmap Clarity:', error);
      return [];
    }
  }

  /**
   * Buscar taxa de rejeição e sessões por página
   * 
   * Para que serve: Identifica quais páginas as pessoas abandonam
   * Retorna: {page, sessionCount, bounceRate, avgTimeOnPage}
   */
  async fetchPageMetrics(dateStart, dateEnd) {
    try {
      const response = await fetch(
        `${this.baseURL}/projects/${this.projectId}/pages?` +
        `startDate=${dateStart}&endDate=${dateEnd}`,
        {
          headers: {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) throw new Error('Erro buscar métricas página');

      const data = await response.json();
      return this._parsePageMetrics(data.data || []);
    } catch (error) {
      console.error('❌ Erro buscar métricas Clarity:', error);
      return [];
    }
  }

  /**
   * Buscar sessões que levaram a conversão vs sem conversão
   * 
   * Para que serve: Compara comportamento de conversores vs não-conversores
   * Retorna: Média de cliques, tempo, scroll, etc por tipo
   */
  async fetchConversionSessionComparison(dateStart, dateEnd) {
    try {
      // Busca sessões que converteram
      const convertedResponse = await fetch(
        `${this.baseURL}/projects/${this.projectId}/sessions?` +
        `startDate=${dateStart}&endDate=${dateEnd}&converted=true`,
        {
          headers: {
            'Authorization': `Bearer ${this.token}`,
          },
        }
      );

      // Busca sessões que NÃO converteram
      const abandonedResponse = await fetch(
        `${this.baseURL}/projects/${this.projectId}/sessions?` +
        `startDate=${dateStart}&endDate=${dateEnd}&converted=false`,
        {
          headers: {
            'Authorization': `Bearer ${this.token}`,
          },
        }
      );

      if (!convertedResponse.ok || !abandonedResponse.ok) {
        throw new Error('Erro buscar comparação sessões');
      }

      const converted = await convertedResponse.json();
      const abandoned = await abandonedResponse.json();

      return {
        converted: this._parseSessionMetrics(converted.data || []),
        abandoned: this._parseSessionMetrics(abandoned.data || []),
        comparison: this._compareMetrics(converted.data, abandoned.data),
      };
    } catch (error) {
      console.error('❌ Erro buscar comparação conversão:', error);
      return null;
    }
  }

  /**
   * Buscar gravações de sessão (session recordings)
   * 
   * Para que serve: Pega URLs de vídeos reais de usuários navegando
   * Ótimo para: Entender exatamente porque abandonam
   * Retorna: URLs das gravações mais relevantes
   */
  async fetchSessionRecordings(filter = 'abandoned', limit = 10) {
    try {
      const response = await fetch(
        `${this.baseURL}/projects/${this.projectId}/recordings?` +
        `filter=${filter}&limit=${limit}`,
        {
          headers: {
            'Authorization': `Bearer ${this.token}`,
          },
        }
      );

      if (!response.ok) throw new Error('Erro buscar gravações');

      const data = await response.json();
      return data.data || [];
    } catch (error) {
      console.error('❌ Erro buscar session recordings:', error);
      return [];
    }
  }

  /**
   * Buscar feedback e comentários dos usuários
   * 
   * Para que serve: Coleta diretamente o que usuários acham
   * Útil para: Entender frustração e sugestões
   * Retorna: Array de comentários com sentimento (positive/negative/neutral)
   */
  async fetchUserFeedback(dateStart, dateEnd) {
    try {
      const response = await fetch(
        `${this.baseURL}/projects/${this.projectId}/feedback?` +
        `startDate=${dateStart}&endDate=${dateEnd}`,
        {
          headers: {
            'Authorization': `Bearer ${this.token}`,
          },
        }
      );

      if (!response.ok) throw new Error('Erro buscar feedback');

      const data = await response.json();
      return this._parseFeedback(data.data || []);
    } catch (error) {
      console.error('❌ Erro buscar feedback:', error);
      return [];
    }
  }

  // Helpers privados
  _parsePageMetrics(pages) {
    return pages.map(page => ({
      url: page.uri,
      sessions: page.sessionCount,
      bounceRate: page.bounceRate || 0,
      timeOnPage: page.avgTimeOnPage || 0,
      clicks: page.clickCount || 0,
    }));
  }

  _parseSessionMetrics(sessions) {
    const metrics = {
      totalSessions: sessions.length,
      avgClicks: 0,
      avgScrollDepth: 0,
      avgTimeSpent: 0,
      avgPageViews: 0,
    };

    sessions.forEach(session => {
      metrics.avgClicks += session.clicks || 0;
      metrics.avgScrollDepth += session.scrollDepth || 0;
      metrics.avgTimeSpent += session.duration || 0;
      metrics.avgPageViews += session.pageViews || 0;
    });

    if (sessions.length > 0) {
      metrics.avgClicks /= sessions.length;
      metrics.avgScrollDepth /= sessions.length;
      metrics.avgTimeSpent /= sessions.length;
      metrics.avgPageViews /= sessions.length;
    }

    return metrics;
  }

  _compareMetrics(converted, abandoned) {
    const conv = this._parseSessionMetrics(converted);
    const aband = this._parseSessionMetrics(abandoned);

    return {
      clickDiff: ((conv.avgClicks - aband.avgClicks) / aband.avgClicks * 100).toFixed(1),
      scrollDiff: ((conv.avgScrollDepth - aband.avgScrollDepth) / aband.avgScrollDepth * 100).toFixed(1),
      timeDiff: ((conv.avgTimeSpent - aband.avgTimeSpent) / aband.avgTimeSpent * 100).toFixed(1),
      insight: 'Usuários que conversam tendem a...',
    };
  }

  _parseFeedback(feedbackItems) {
    return feedbackItems.map(item => ({
      comment: item.text,
      sentiment: this._analyzeSentiment(item.text),
      timestamp: item.createdAt,
      page: item.pageUri,
    }));
  }

  _analyzeSentiment(text) {
    const positive = ['bom', 'ótimo', 'gosto', 'adorei', 'excelente'];
    const negative = ['ruim', 'horrível', 'problema', 'difícil', 'perdido'];
    
    const lowerText = text.toLowerCase();
    if (positive.some(word => lowerText.includes(word))) return 'positive';
    if (negative.some(word => lowerText.includes(word))) return 'negative';
    return 'neutral';
  }
}

export default ClarityConnector;
