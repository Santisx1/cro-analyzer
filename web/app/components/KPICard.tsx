import React from 'react';
import './KPICard.css';

interface KPICardProps {
  title: string;
  value: number;
  unit: string;
  trend: 'up' | 'down';
}

export default function KPICard({ title, value, unit, trend }: KPICardProps) {
  return (
    <div className="kpi-card">
      <div className="kpi-header">
        <h3>{title}</h3>
        <span className={`trend-${trend}`}>{trend === 'up' ? '📈' : '📉'}</span>
      </div>
      <div className="kpi-value">
        <span className="number">{value.toFixed(1)}</span>
        <span className="unit">{unit}</span>
      </div>
    </div>
  );
}
