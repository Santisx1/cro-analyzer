import React from 'react';
import './FunnelChart.css';

interface FunnelData {
  stage: string;
  users: number;
}

interface FunnelChartProps {
  data: FunnelData[];
}

export default function FunnelChart({ data }: FunnelChartProps) {
  if (!data || data.length === 0) {
    return <div className="chart-empty">Sem dados disponíveis</div>;
  }

  const maxUsers = Math.max(...data.map(d => d.users));

  return (
    <div className="funnel-chart">
      {data.map((step, index) => {
        const percentage = (step.users / maxUsers) * 100;
        const dropoff = index > 0 ? ((data[index - 1].users - step.users) / data[index - 1].users * 100).toFixed(1) : 0;

        return (
          <div key={index} className="funnel-step">
            <div className="step-bar" style={{ width: `${percentage}%` }}>
              <span className="step-label">{step.stage}</span>
            </div>
            <div className="step-info">
              <span className="users">{step.users.toLocaleString()} usuários</span>
              {index > 0 && <span className="dropoff">↓ {dropoff}% queda</span>}
            </div>
          </div>
        );
      })}
    </div>
  );
}
