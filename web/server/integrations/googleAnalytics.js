/**
 * Google Analytics 4 Integration
 * 
 * PARA QUE SERVE:
 * - Conecta com sua propriedade Google Analytics 4
 * - Importa eventos de conversão (page_view, add_to_cart, purchase, etc)
 * - Alimenta o motor de análise CRO com dados reais
 * 
 * FLUXO:
 * Seu site → Google Analytics → API daqui → Dashboard
 */

import { google } from 'googleapis';

const analyticsData = google.analyticsdata('v1beta');

class GoogleAnalyticsConnector {
  constructor(credentials) {
    this.credentials = credentials;
    this.auth = null;
  }

  /**
   * Autenticar com Google
   * 
   * Para que serve: Valida sua credencial e conecta com GA4
   * Retorna: true se conectou, false se erro
   */
  async authenticate() {
    try {
      this.auth = new google.auth.GoogleAuth({
        keyFile: this.credentials,
        scopes: ['https://www.googleapis.com/auth/analytics.readonly'],
      });
      console.log('✅ Google Analytics autenticado');
      return true;
    } catch (error) {
      console.error('❌ Erro autenticar GA4:', error);
      return false;
    }
  }

  /**
   * Buscar eventos de conversão
   * 
   * Para que serve: Pega todos os eventos (page_view, add_to_cart, purchase)
   * Entrada: propertyId (ID do seu GA4), dataMin, dataMax
   * Retorna: Array com todos os eventos do período
   */
  async fetchConversionEvents(propertyId, dateStart, dateEnd) {
    try {
      const response = await analyticsData.properties.runReport({
        auth: this.auth,
        property: `properties/${propertyId}`,
        requestBody: {
          dateRanges: [{ startDate: dateStart, endDate: dateEnd }],
          dimensions: [
            { name: 'eventName' },
            { name: 'date' },
            { name: 'userId' },
          ],
          metrics: [
            { name: 'eventCount' },
            { name: 'activeUsers' },
          ],
        },
      });

      console.log(`✅ ${response.data.rowCount} eventos encontrados no GA4`);
      return this._parseGAResponse(response.data);
    } catch (error) {
      console.error('❌ Erro buscar eventos GA4:', error);
      return [];
    }
  }

  /**
   * Buscar dados de funil customizado
   * 
   * Para que serve: Rastreia sequência específica de eventos
   * Ex: page_view → add_to_cart → checkout → purchase
   * Retorna: Taxa de conversão por etapa
   */
  async fetchFunnelData(propertyId, funnelSteps, dateStart, dateEnd) {
    try {
      const response = await analyticsData.properties.runReport({
        auth: this.auth,
        property: `properties/${propertyId}`,
        requestBody: {
          dateRanges: [{ startDate: dateStart, endDate: dateEnd }],
          dimensions: [{ name: 'eventName' }],
          metrics: [
            { name: 'activeUsers' },
            { name: 'eventCount' },
            { name: 'sessions' },
          ],
          dimensionFilter: {
            filter: {
              fieldName: 'eventName',
              stringFilter: {
                matchType: 'EXACT',
                value: funnelSteps.join('|'),
              },
            },
          },
        },
      });

      return this._calculateFunnelConversion(response.data, funnelSteps);
    } catch (error) {
      console.error('❌ Erro buscar funil GA4:', error);
      return [];
    }
  }

  /**
   * Buscar tempo de sessão e bounce rate
   * 
   * Para que serve: Pega métricas de comportamento do usuário
   * Retorna: sessionsAverage, bounceRate, avgSessionDuration
   */
  async fetchSessionMetrics(propertyId, dateStart, dateEnd) {
    try {
      const response = await analyticsData.properties.runReport({
        auth: this.auth,
        property: `properties/${propertyId}`,
        requestBody: {
          dateRanges: [{ startDate: dateStart, endDate: dateEnd }],
          metrics: [
            { name: 'sessions' },
            { name: 'bounceRate' },
            { name: 'averageSessionDuration' },
            { name: 'screenPageViews' },
          ],
        },
      });

      return this._parseSessionMetrics(response.data);
    } catch (error) {
      console.error('❌ Erro buscar métricas GA4:', error);
      return {};
    }
  }

  // Helpers privados
  _parseGAResponse(data) {
    if (!data.rows) return [];
    return data.rows.map(row => ({
      eventName: row.dimensionValues[0].value,
      date: row.dimensionValues[1].value,
      userId: row.dimensionValues[2].value,
      count: parseInt(row.metricValues[0].value),
      users: parseInt(row.metricValues[1].value),
    }));
  }

  _calculateFunnelConversion(data, funnelSteps) {
    // Calcula taxa de conversão por step
    const metrics = {};
    funnelSteps.forEach((step, idx) => {
      metrics[step] = {
        position: idx + 1,
        users: 0, // Será preenchido dos dados
        conversionRate: 0,
      };
    });
    return metrics;
  }

  _parseSessionMetrics(data) {
    if (!data.rows) return {};
    const row = data.rows[0];
    return {
      sessions: parseInt(row.metricValues[0].value),
      bounceRate: parseFloat(row.metricValues[1].value),
      avgSessionDuration: parseFloat(row.metricValues[2].value),
      pageViews: parseInt(row.metricValues[3].value),
    };
  }
}

export default GoogleAnalyticsConnector;
