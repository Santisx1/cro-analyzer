'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import DashboardLayout from '../components/DashboardLayout';
import KPICard from '../components/KPICard';
import FunnelChart from '../components/FunnelChart';
import RecommendationsList from '../components/RecommendationsList';
import HistoryTable from '../components/HistoryTable';
import './dashboard.css';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

interface DashboardData {
  kpis: {
    conversion_rate: number;
    average_session_duration: number;
    bounce_rate: number;
    pages_per_session: number;
  };
  funnel: Array<{ stage: string; users: number }>;
  recommendations: Array<{ id: string; type: string; title: string; description: string; impact: string }>;
  history: Array<{ id: string; date: string; conversion_rate: number; status: string }>;
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [running, setRunning] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (!token) {
      router.push('/');
      return;
    }
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('authToken');
      const response = await fetch(`${API_URL}/api/analysis/latest`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch dashboard data');
      }

      const result = await response.json();
      setData(result);
      setError('');
    } catch (err) {
      setError('Erro ao carregar dados');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunAnalysis = async () => {
    setRunning(true);
    try {
      const token = localStorage.getItem('authToken');
      const response = await fetch(`${API_URL}/api/analysis/run`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to run analysis');
      }

      // Refresh dashboard after analysis
      await fetchDashboardData();
    } catch (err) {
      setError('Erro ao executar análise');
      console.error(err);
    } finally {
      setRunning(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userEmail');
    router.push('/');
  };

  if (loading) {
    return (
      <DashboardLayout onLogout={handleLogout}>
        <div className="loading">Carregando...</div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout onLogout={handleLogout}>
        <div className="error">{error}</div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout onLogout={handleLogout}>
      <div className="dashboard-content">
        {/* Header */}
        <div className="dashboard-header">
          <div>
            <h1>Análise de CRO</h1>
            <p>Otimização de Taxa de Conversão em Tempo Real</p>
          </div>
          <button
            className="btn-primary"
            onClick={handleRunAnalysis}
            disabled={running}
          >
            {running ? 'Analisando...' : 'Executar Análise'}
          </button>
        </div>

        {/* KPI Cards */}
        <div className="kpi-grid">
          {data && (
            <>
              <KPICard
                title="Taxa de Conversão"
                value={data.kpis.conversion_rate}
                unit="%"
                trend="up"
              />
              <KPICard
                title="Tempo de Sessão"
                value={data.kpis.average_session_duration}
                unit="s"
                trend="up"
              />
              <KPICard
                title="Taxa de Rejeição"
                value={data.kpis.bounce_rate}
                unit="%"
                trend="down"
              />
              <KPICard
                title="Páginas por Sessão"
                value={data.kpis.pages_per_session}
                unit="pág"
                trend="up"
              />
            </>
          )}
        </div>

        {/* Charts Section */}
        <div className="charts-section">
          {data?.funnel && (
            <div className="chart-card">
              <h2>Funil de Conversão</h2>
              <FunnelChart data={data.funnel} />
            </div>
          )}
        </div>

        {/* Recommendations */}
        {data?.recommendations && (
          <div className="recommendations-section">
            <h2>Recomendações</h2>
            <RecommendationsList recommendations={data.recommendations} />
          </div>
        )}

        {/* History */}
        {data?.history && (
          <div className="history-section">
            <h2>Histórico de Análises</h2>
            <HistoryTable history={data.history} />
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
