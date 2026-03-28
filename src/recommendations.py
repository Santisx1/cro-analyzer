"""
AI-powered recommendation engine for CRO optimization
Generates actionable recommendations based on analysis data
"""

from typing import Dict, List, Optional


class RecommendationEngine:
    """Generate CRO optimization recommendations"""
    
    # Recommendation templates by issue type
    RECOMMENDATIONS_DB = {
        'high_cart_abandonment': {
            'title': 'Reduzir abandono de carrinho',
            'actions': [
                'Implementar recuperação de carrinho abandonado via email',
                'Simplificar processo de checkout (menos steps)',
                'Adicionar garantia de satisfação ou política de retorno',
                'Testar diferentes métodos de pagamento'
            ],
            'priority': 'high',
            'expected_impact': '25-40%'
        },
        'high_page_abandonment': {
            'title': 'Reduzir taxa de rejeição da página',
            'actions': [
                'Melhorar headline e proposta de valor',
                'Otimizar tempo de carregamento da página',
                'Aumentar clareza visual do CTA',
                'Testar diferentes layouts e cores'
            ],
            'priority': 'high',
            'expected_impact': '15-30%'
        },
        'form_friction': {
            'title': 'Otimizar formulários',
            'actions': [
                'Reduzir número de campos do formulário',
                'Implementar auto-preenchimento',
                'Adicionar indicador de progresso',
                'Usar validação em tempo real'
            ],
            'priority': 'medium',
            'expected_impact': '10-20%'
        },
        'low_engagement': {
            'title': 'Aumentar engajamento',
            'actions': [
                'Adicionar elementos interativos (videos, demos)',
                'Implementar conteúdo social proof (reviews, testimonials)',
                'Criar urgência (contador regressivo, stock limitado)',
                'Testar ofertas time-limited'
            ],
            'priority': 'medium',
            'expected_impact': '10-15%'
        },
        'mobile_issues': {
            'title': 'Otimizar para mobile',
            'actions': [
                'Fazer mobile-first design',
                'Testar botões com espaço entre eles',
                'Otimizar imagens e performance',
                'Simplificar navegação para mobile'
            ],
            'priority': 'high',
            'expected_impact': '20-35%'
        }
    }
    
    def __init__(self):
        """Initialize recommendation engine"""
        self.recommendations = []
    
    def generate_recommendations(
        self,
        funnel_metrics: Dict,
        abandonment_points: List[Dict]
    ) -> List[Dict]:
        """
        Generate recommendations based on analysis
        
        Args:
            funnel_metrics: Funnel analysis metrics
            abandonment_points: Identified abandonment points
            
        Returns:
            List of actionable recommendations
        """
        recommendations = []
        
        # Analyze abandonment points
        for point in abandonment_points:
            step = point['step']
            drop_off = point['drop_off_rate']
            
            # Identify issue type and generate recommendation
            if 'cart' in step.lower() and drop_off > 30:
                rec = self._create_recommendation(
                    'high_cart_abandonment',
                    step,
                    drop_off
                )
                recommendations.append(rec)
            
            elif 'page' in step.lower() and drop_off > 40:
                rec = self._create_recommendation(
                    'high_page_abandonment',
                    step,
                    drop_off
                )
                recommendations.append(rec)
            
            elif 'form' in step.lower() and drop_off > 25:
                rec = self._create_recommendation(
                    'form_friction',
                    step,
                    drop_off
                )
                recommendations.append(rec)
            
            else:
                rec = self._create_generic_recommendation(step, drop_off)
                recommendations.append(rec)
        
        # Add general engagement recommendations if low overall conversion
        overall_conversion = funnel_metrics['conversion_rates'].get(
            funnel_metrics['steps'][-1], 0
        ) if funnel_metrics['steps'] else 0
        
        if overall_conversion < 5:
            rec = self._create_recommendation(
                'low_engagement',
                'overall_funnel',
                100 - overall_conversion
            )
            recommendations.append(rec)
        
        # Sort by priority and expected impact
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        recommendations.sort(
            key=lambda x: (
                priority_order.get(x['priority'], 3),
                -float(x['expected_impact'].split('-')[1].strip('%'))
            )
        )
        
        self.recommendations = recommendations
        return recommendations
    
    def _create_recommendation(
        self,
        rec_type: str,
        step: str,
        severity: float
    ) -> Dict:
        """
        Create a recommendation from template
        
        Args:
            rec_type: Type of recommendation
            step: Funnel step
            severity: Drop-off rate or severity
            
        Returns:
            Recommendation dictionary
        """
        if rec_type not in self.RECOMMENDATIONS_DB:
            return self._create_generic_recommendation(step, severity)
        
        template = self.RECOMMENDATIONS_DB[rec_type]
        
        return {
            'id': f"{rec_type}_{step.replace(' ', '_')}",
            'type': rec_type,
            'step': step,
            'title': template['title'],
            'description': f"Otimizar a etapa '{step}' que tem {severity:.1f}% de abandono",
            'actions': template['actions'],
            'priority': template['priority'],
            'expected_impact': template['expected_impact'],
            'effort': 'medium',
            'metrics_to_track': ['conversion_rate', 'drop_off_rate', 'time_on_page']
        }
    
    def _create_generic_recommendation(
        self,
        step: str,
        severity: float
    ) -> Dict:
        """
        Create generic recommendation
        
        Args:
            step: Funnel step
            severity: Drop-off rate
            
        Returns:
            Recommendation dictionary
        """
        return {
            'id': f"generic_{step.replace(' ', '_')}",
            'type': 'generic_optimization',
            'step': step,
            'title': f'Otimizar a etapa #{step}',
            'description': f"A etapa '{step}' tem {severity:.1f}% de abandono. Recomenda-se análise detalhada.",
            'actions': [
                'Conduzir User Testing nesta etapa',
                'Analisar heatmaps e session recordings',
                'Implementar A/B testing de variações',
                'Coletar feedback de usuários'
            ],
            'priority': 'high' if severity > 50 else 'medium',
            'expected_impact': '15-25%',
            'effort': 'medium',
            'metrics_to_track': ['conversion_rate', 'drop_off_rate', 'user_feedback']
        }
