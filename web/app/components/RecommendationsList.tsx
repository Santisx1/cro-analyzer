import React from 'react';
import './RecommendationsList.css';

interface Recommendation {
  id: string;
  type: string;
  title: string;
  description: string;
  impact: string;
}

interface RecommendationsListProps {
  recommendations: Recommendation[];
}

export default function RecommendationsList({ recommendations }: RecommendationsListProps) {
  if (!recommendations || recommendations.length === 0) {
    return <div className="recommendations-empty">Nenhuma recomendação disponível</div>;
  }

  const getImpactColor = (impact: string) => {
    switch (impact.toLowerCase()) {
      case 'alto':
      case 'high':
        return 'impact-high';
      case 'médio':
      case 'medium':
        return 'impact-medium';
      case 'baixo':
      case 'low':
        return 'impact-low';
      default:
        return 'impact-low';
    }
  };

  return (
    <div className="recommendations-list">
      {recommendations.map((rec) => (
        <div key={rec.id} className="recommendation-item">
          <div className="recommendation-header">
            <div className="header-left">
              <h3>{rec.title}</h3>
              <span className="type">{rec.type}</span>
            </div>
            <span className={`impact ${getImpactColor(rec.impact)}`}>
              {rec.impact}
            </span>
          </div>
          <p className="description">{rec.description}</p>
        </div>
      ))}
    </div>
  );
}
