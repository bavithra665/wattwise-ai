from flask import jsonify, request
from flask_login import login_required, current_user
from app.api import bp
from app.models import EnergyData, EnergyInsight, AIRecommendation
from app.energy_analyzer import EnergyAnalyzer
from app.ai_consultant import AIConsultant

@bp.route('/energy-stats')
@login_required
def energy_stats():
    """Get energy statistics for dashboard"""
    data = EnergyData.query.filter_by(user_id=current_user.id).order_by(EnergyData.timestamp.desc()).limit(100).all()
    
    stats = {
        'total_consumption': sum(d.energy_kwh for d in data),
        'total_cost': sum(d.cost_inr or 0 for d in data),
        'anomaly_count': sum(1 for d in data if d.is_anomaly),
        'department_breakdown': {}
    }
    
    # Department breakdown
    for record in data:
        dept = record.department
        if dept not in stats['department_breakdown']:
            stats['department_breakdown'][dept] = 0
        stats['department_breakdown'][dept] += record.energy_kwh
    
    return jsonify(stats)

@bp.route('/analyze-insight/<int:insight_id>')
@login_required
def analyze_insight(insight_id):
    """Get AI analysis for a specific insight"""
    insight = EnergyInsight.query.filter_by(id=insight_id, user_id=current_user.id).first()
    if not insight:
        return jsonify({'error': 'Insight not found'}), 404
    
    consultant = AIConsultant()
    analysis = consultant.get_insight_analysis(insight, current_user.id)
    
    return jsonify(analysis)

@bp.route('/insight/<int:insight_id>')
@login_required
def get_insight_details(insight_id):
    """Get detailed information about a specific insight"""
    insight = EnergyInsight.query.filter_by(id=insight_id, user_id=current_user.id).first()
    if not insight:
        return jsonify({'error': 'Insight not found'}), 404
    
    # Get related energy data
    energy_data = EnergyData.query.filter_by(
        user_id=current_user.id,
        department=insight.department
    ).order_by(EnergyData.timestamp.desc()).limit(20).all()
    
    # Get recommendations
    recommendations = AIRecommendation.query.filter_by(insight_id=insight.id).all()
    
    details = {
        'id': insight.id,
        'title': insight.title,
        'description': insight.description,
        'insight_type': insight.insight_type,
        'department': insight.department,
        'equipment': insight.equipment,
        'severity': insight.severity,
        'potential_savings_inr': insight.potential_savings_inr,
        'created_at': insight.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'energy_data': [
            {
                'timestamp': data.timestamp.strftime('%Y-%m-%d %H:%M'),
                'energy_kwh': data.energy_kwh,
                'cost_inr': data.cost_inr,
                'is_anomaly': data.is_anomaly
            }
            for data in energy_data
        ],
        'recommendations': [
            {
                'recommendation': rec.recommendation,
                'priority': rec.priority,
                'estimated_savings_inr': rec.estimated_savings_inr,
                'implementation_difficulty': rec.implementation_difficulty
            }
            for rec in recommendations
        ]
    }
    
    return jsonify(details)
