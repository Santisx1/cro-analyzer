import React from 'react';
import './HistoryTable.css';

interface HistoryItem {
  id: string;
  date: string;
  conversion_rate: number;
  status: string;
}

interface HistoryTableProps {
  history: HistoryItem[];
}

export default function HistoryTable({ history }: HistoryTableProps) {
  if (!history || history.length === 0) {
    return <div className="table-empty">Histórico vazio</div>;
  }

  return (
    <div className="history-table-wrapper">
      <table className="history-table">
        <thead>
          <tr>
            <th>Data</th>
            <th>Taxa de Conversão</th>
            <th>Status</th>
            <th>Detalhes</th>
          </tr>
        </thead>
        <tbody>
          {history.map((item) => (
            <tr key={item.id}>
              <td>{new Date(item.date).toLocaleDateString('pt-BR')}</td>
              <td className="conversion-rate">{item.conversion_rate.toFixed(2)}%</td>
              <td>
                <span className={`status-badge status-${item.status.toLowerCase()}`}>
                  {item.status}
                </span>
              </td>
              <td className="actions">
                <button className="link-action">Ver Relatório</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
