import google.generativeai as genai
import os
from datetime import datetime, timedelta
from app.models import EnergyData, EnergyInsight, AIRecommendation, db
import logging

logger = logging.getLogger(__name__)

class AIConsultant:
    def __init__(self, user=None):
        # Configure Gemini AI
        api_key = None
        
        if user:
            if hasattr(user, 'gemini_api_key') and user.gemini_api_key:
                api_key = user.gemini_api_key
        
        # Fallback to environment variable
        if not api_key:
            api_key = os.environ.get('GEMINI_API_KEY')
        
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-flash-latest')
            except Exception as e:
                logger.error(f"Error creating Gemini model: {str(e)}")
                self.model = None
        else:
            logger.warning("Gemini API key not found. AI features will be limited.")
            self.model = None
    
    def get_insight_analysis(self, insight, user_id):
        """Get AI analysis for a specific energy insight"""
        
        # Get user to access API key directly if needed
        from app.models import User
        user = User.query.get(user_id)
        if user:
             if user.gemini_api_key and not self.model:
                 # Re-initialize if model is missing but user has key
                 try:
                     genai.configure(api_key=user.gemini_api_key)
                     # self.model = genai.GenerativeModel('gemini-flash-latest')
                     self.model = genai.GenerativeModel('gemini-flash-latest')
                 except Exception as e:
                     logger.error(f"Failed to re-initialize model: {e}")

        if not self.model:
            return self._fallback_analysis(insight, "AI Model not initialized (Check API Key)")
        
        try:
            # Get relevant energy data
            energy_data = self._get_relevant_data(insight, user_id)
            
            # Create context for AI
            context = self._create_ai_context(insight, energy_data)
            
            # Generate AI response
            prompt = self._create_analysis_prompt(context)
            response = self.model.generate_content(prompt)
            
            # Parse and save recommendations
            ai_data = self._parse_ai_response(response.text, insight.id, user_id)
            
            return {
                'analysis': ai_data.get('analysis', response.text),
                'root_cause': ai_data.get('root_cause'),
                'business_impact': ai_data.get('business_impact'),
                'recommendations': ai_data.get('recommendations', []),
                'timeline': ai_data.get('timeline', {}),
                'context': context,
                'source': 'gemini'
            }
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            error_msg = str(e)
            
            # Retry logic for Quota/Model issues
            if ("429" in error_msg or "404" in error_msg) and not hasattr(self, '_retry_attempted'):
                self._retry_attempted = True
                try:
                    # Try a standard Pro model as fallback
                    fallback_model = genai.GenerativeModel('gemini-pro-latest')
                    response = fallback_model.generate_content(prompt)
                    
                    # If successful, parse and return
                    ai_data = self._parse_ai_response(response.text, insight.id, user_id)
                    self._retry_attempted = False # Reset
                    return {
                        'analysis': ai_data.get('analysis', response.text),
                        'root_cause': ai_data.get('root_cause'),
                        'business_impact': ai_data.get('business_impact'),
                        'recommendations': ai_data.get('recommendations', []),
                        'timeline': ai_data.get('timeline', {}),
                        'context': context,
                        'source': 'gemini-pro'
                    }
                except Exception as retry_error:
                    logger.error(f"Retry failed: {str(retry_error)}")
            
            if hasattr(self, '_retry_attempted'):
                self._retry_attempted = False
                
            if "429" in error_msg or "quota" in error_msg.lower():
                 error_msg = "AI Usage Limit Exceeded. Please wait a minute."
                 
            return self._fallback_analysis(insight, error_msg)
    
    def _get_relevant_data(self, insight, user_id):
        """Get energy data relevant to the insight"""
        query = EnergyData.query.filter_by(user_id=user_id)
        
        if insight.department:
            query = query.filter_by(department=insight.department)
        
        if insight.equipment:
            query = query.filter_by(equipment=insight.equipment)
        
        # Get data from the last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        query = query.filter(EnergyData.timestamp >= thirty_days_ago)
        
        return query.order_by(EnergyData.timestamp.desc()).limit(100).all()
    
    def _create_ai_context(self, insight, energy_data):
        """Create context information for AI analysis"""
        context = {
            'insight_type': insight.insight_type,
            'title': insight.title,
            'description': insight.description,
            'department': insight.department,
            'equipment': insight.equipment,
            'severity': insight.severity,
            'potential_savings_inr': insight.potential_savings_inr,
            'data_points': len(energy_data),
            'total_consumption': sum(d.energy_kwh for d in energy_data),
            'total_cost': sum(d.cost_inr or 0 for d in energy_data),
            'anomaly_count': sum(1 for d in energy_data if d.is_anomaly)
        }
        
        # Add recent consumption patterns
        if energy_data:
            recent_data = energy_data[:10]  # Last 10 data points
            context['recent_consumption'] = [
                {
                    'timestamp': d.timestamp.strftime('%Y-%m-%d %H:%M'),
                    'energy_kwh': d.energy_kwh,
                    'cost_inr': d.cost_inr,
                    'is_anomaly': d.is_anomaly
                }
                for d in recent_data
            ]
        
        return context
    
    def _create_analysis_prompt(self, context):
        """Create a comprehensive prompt for AI analysis"""
        prompt = f"""
You are an expert Energy Optimization Consultant for Indian industries. Analyze the following energy insight and provide professional, actionable recommendations.

INSIGHT DETAILS:
- Type: {context['insight_type']}
- Title: {context['title']}
- Description: {context['description']}
- Department: {context['department']}
- Equipment: {context['equipment']}
- Severity: {context['severity']}
- Potential Savings: ₹{context['potential_savings_inr']:.2f}

ENERGY DATA SUMMARY:
- Total Data Points: {context['data_points']}
- Total Consumption: {context['total_consumption']:.2f} kWh
- Total Cost: ₹{context['total_cost']:.2f}
- Anomalies Detected: {context['anomaly_count']}

RECENT CONSUMPTION PATTERNS:
{chr(10).join([f"- {d['timestamp']}: {d['energy_kwh']:.2f} kWh (₹{d['cost_inr']:.2f})" + (" [ANOMALY]" if d['is_anomaly'] else "") for d in context.get('recent_consumption', [])])}

Please provide a valid JSON response with the following structure:
{{
    "root_cause": "Detailed explanation of why this energy pattern occurred (use HTML like <ul>, <li>, <b> if needed).",
    "business_impact": "Financial and operational consequences (use HTML if needed).",
    "recommendations": [
        {{
            "text": "Specific actionable recommendation",
            "priority": "high/medium/low",
            "estimated_savings_inr": 1000.0,
            "difficulty": "low/medium/high"
        }}
    ],
    "timeline": {{
        "quick_wins": ["List of specific tasks to implement within 1-2 weeks"],
        "medium_term": ["List of specific tasks to implement within 1-3 months"],
        "long_term": ["List of specific tasks to implement within 3-6 months"]
    }}
}}

GUIDELINES:
- Use calm, professional tone suitable for Indian business executives
- Focus on practical solutions that can be implemented quickly
- Consider Indian industrial context and electricity rates (₹8.50/kWh average)
- Avoid technical jargon; explain concepts simply
- Include both cost savings and sustainability benefits
- Provide realistic implementation timelines
- ENSURE OUTPUT IS VALID JSON. Do not include markdown formatting '```json' at the start.
"""
        return prompt
    
    def _parse_ai_response(self, response_text, insight_id, user_id):
        """Parse AI response and save recommendations"""
        import json
        import re
        
        # Default structure
        result = {
            'analysis': response_text,
            'recommendations': [],
            'timeline': {
                'quick_wins': [],
                'medium_term': [],
                'long_term': []
            }
        }
        
        try:
            # meaningful cleaning of the response text to ensure JSON parsing
            clean_text = re.sub(r'```json\s*|\s*```', '', response_text).strip()
            # If there's extra text before/after JSON, try to find the JSON object
            json_match = re.search(r'\{.*\}', clean_text, re.DOTALL)
            if json_match:
                clean_text = json_match.group(0)
            
            data = json.loads(clean_text)
            
            # Extract structured analysis components
            result['root_cause'] = data.get('root_cause', '')
            result['business_impact'] = data.get('business_impact', '')
            
            # Identify analysis content (fallback to concatenated root cause + impact if 'analysis' is missing)
            if 'analysis' in data:
                 result['analysis'] = data['analysis']
            elif result['root_cause'] or result['business_impact']:
                 # Create a combined analysis string for backward compatibility
                 result['analysis'] = f"<b>Root Cause:</b><br>{result['root_cause']}<br><br><b>Business Impact:</b><br>{result['business_impact']}"
            else:
                 result['analysis'] = response_text
                 
            result['timeline'] = data.get('timeline', result['timeline'])
            
            # Clear existing recommendations for this insight to avoid duplicates
            AIRecommendation.query.filter_by(insight_id=insight_id).delete()
            
            recommendations_data = data.get('recommendations', [])
            saved_recommendations = []
            
            for rec in recommendations_data:
                # Validate/Default values
                rec_text = rec.get('text', 'Energy optimization recommendation')
                priority = rec.get('priority', 'medium').lower()
                if priority not in ['high', 'medium', 'low']: priority = 'medium'
                
                difficulty = rec.get('difficulty', 'medium').lower()
                if difficulty not in ['low', 'medium', 'high']: difficulty = 'medium'
                
                savings = rec.get('estimated_savings_inr')
                if isinstance(savings, (int, float)):
                    savings = float(savings)
                else:
                    savings = None
                
                # Save to DB
                recommendation = AIRecommendation(
                    user_id=user_id,
                    insight_id=insight_id,
                    recommendation=rec_text,
                    priority=priority,
                    estimated_savings_inr=savings,
                    implementation_difficulty=difficulty
                )
                
                db.session.add(recommendation)
                
                saved_recommendations.append({
                    'text': rec_text,
                    'priority': priority,
                    'estimated_savings': savings,
                    'difficulty': difficulty
                })
            
            db.session.commit()
            result['recommendations'] = saved_recommendations
            return result
            
        except Exception as e:
            logger.error(f"Error parsing AI JSON response: {str(e)}")
            # Fallback to old parsing method if JSON fails
            logger.info("Falling back to text parsing")
            return self._parse_text_response_fallback(response_text, insight_id, user_id)

    def _parse_text_response_fallback(self, response_text, insight_id, user_id):
        """Fallback for parsing unstructured text response"""
        recommendations = []
        
        try:
            # Split response into sections
            sections = response_text.split('\n\n')
            
            # Extract recommendations (look for numbered lists or bullet points)
            for section in sections:
                if 'recommendation' in section.lower() or 'action' in section.lower():
                    lines = section.split('\n')
                    for line in lines:
                        if line.strip() and (line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '-', '•', '*'))):
                            # Clean up the recommendation text
                            rec_text = line.strip()
                            rec_text = rec_text[2:] if rec_text.startswith(('1.', '2.', '3.', '4.', '5.')) else rec_text[1:].strip()
                            
                            # Determine priority based on content
                            priority = 'medium'
                            if any(word in rec_text.lower() for word in ['urgent', 'immediate', 'critical']):
                                priority = 'high'
                            elif any(word in rec_text.lower() for word in ['long-term', 'consider', 'evaluate']):
                                priority = 'low'
                            
                            # Estimate savings (simplified calculation)
                            estimated_savings = None
                            if '₹' in rec_text or 'savings' in rec_text.lower():
                                # Extract any mentioned savings amount
                                import re
                                amount_match = re.search(r'₹[\d,]+\.?\d*', rec_text)
                                if amount_match:
                                    estimated_savings = float(amount_match.group().replace('₹', '').replace(',', ''))
                            
                            # Determine implementation difficulty
                            difficulty = 'medium'
                            if any(word in rec_text.lower() for word in ['simple', 'easy', 'quick']):
                                difficulty = 'low'
                            elif any(word in rec_text.lower() for word in ['complex', 'major', 'comprehensive']):
                                difficulty = 'high'
                            
                            # Save recommendation
                            # Check if exists to avoid duplicates in fallback mode
                            exists = AIRecommendation.query.filter_by(insight_id=insight_id, recommendation=rec_text).first()
                            if not exists:
                                recommendation = AIRecommendation(
                                    user_id=user_id,
                                    insight_id=insight_id,
                                    recommendation=rec_text,
                                    priority=priority,
                                    estimated_savings_inr=estimated_savings,
                                    implementation_difficulty=difficulty
                                )
                                db.session.add(recommendation)
                            
                            recommendations.append({
                                'text': rec_text,
                                'priority': priority,
                                'estimated_savings': estimated_savings,
                                'difficulty': difficulty
                            })
            
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
        
        # Generate timeline from recommendations
        timeline = {
            'quick_wins': [],
            'medium_term': [],
            'long_term': []
        }
        
        for r in recommendations:
            if r['difficulty'] == 'low' or r['priority'] == 'high':
                timeline['quick_wins'].append(r['text'])
            elif r['difficulty'] == 'medium':
                timeline['medium_term'].append(r['text'])
            else:
                timeline['long_term'].append(r['text'])
        
        return {
            'analysis': response_text,
            'recommendations': recommendations,
            'timeline': timeline
        }
    
    def _fallback_analysis(self, insight, error_message=None):
        """Provide fallback analysis when AI is not available"""
        
        # Generate specific recommendations based on insight type and department
        specific_recommendations = self._generate_specific_recommendations(insight)
        
        # Save recommendations (unchanged logic)
        for rec in specific_recommendations:
            # Check for duplicates first
            exists = AIRecommendation.query.filter_by(insight_id=insight.id, recommendation=rec['text']).first()
            if not exists:
                recommendation = AIRecommendation(
                    user_id=insight.user_id,
                    insight_id=insight.id,
                    recommendation=rec['text'],
                    priority=rec['priority'],
                    estimated_savings_inr=rec['estimated_savings'],
                    implementation_difficulty=rec['difficulty']
                )
                db.session.add(recommendation)
        
        db.session.commit()
        
        return {
            'analysis': f"""
Energy Analysis Report for {insight.title}

Overview:
{insight.description}

Key Findings:
- Energy consumption pattern in {insight.department} department indicates potential optimization opportunities
- Equipment: {insight.equipment}
- Estimated potential savings: ₹{insight.potential_savings_inr:.2f}
- Severity level: {insight.severity}

Department-Specific Analysis:
{self._get_department_analysis(insight)}

Recommendations:
{self._format_recommendations(specific_recommendations)}

Next Steps:
- Schedule department-specific audit within 2 weeks
- Implement quick wins within 1 month
- Plan long-term improvements within 3 months
""",
            'recommendations': specific_recommendations,
            'timeline': {
                'quick_wins': [r['text'] for r in specific_recommendations if r['difficulty'] == 'low' or r['priority'] == 'high'][:3],
                'medium_term': [r['text'] for r in specific_recommendations if r['difficulty'] == 'medium'][:3],
                'long_term': [r['text'] for r in specific_recommendations if r['difficulty'] == 'high'][:3]
            },
            'context': {'fallback': True, 'department': insight.department, 'equipment': insight.equipment},
            'source': 'automated',
            'error': error_message
        }
    
    def _generate_specific_recommendations(self, insight):
        """Generate specific recommendations based on insight type and department"""
        recommendations = []
        
        if insight.insight_type == 'spike':
            recommendations.extend(self._get_spike_recommendations(insight))
        elif insight.insight_type == 'high_consumption':
            recommendations.extend(self._get_high_consumption_recommendations(insight))
        elif insight.insight_type == 'trend':
            recommendations.extend(self._get_trend_recommendations(insight))
        
        return recommendations
    
    def _get_spike_recommendations(self, insight):
        """Recommendations for energy spikes"""
        dept = insight.department.lower() if insight.department else ''
        equipment = insight.equipment.lower() if insight.equipment else 'equipment'
        
        recommendations = [
            {
                'text': f'Investigate {insight.equipment} in {insight.department} for potential malfunction or unusual usage patterns during spike periods.',
                'priority': 'high',
                'estimated_savings': insight.potential_savings_inr * 0.4 if insight.potential_savings_inr else 6000,
                'difficulty': 'low'
            }
        ]
        
        if 'data center' in dept or 'server' in equipment:
            recommendations.extend([
                {
                    'text': 'Check server cooling systems and optimize airflow in data center to prevent energy spikes.',
                    'priority': 'high',
                    'estimated_savings': insight.potential_savings_inr * 0.3 if insight.potential_savings_inr else 4000,
                    'difficulty': 'medium'
                },
                {
                    'text': 'Implement server virtualization to reduce number of physical machines causing spikes.',
                    'priority': 'medium',
                    'estimated_savings': insight.potential_savings_inr * 0.2 if insight.potential_savings_inr else 3000,
                    'difficulty': 'high'
                }
            ])
        elif 'production' in dept or 'manufacturing' in dept:
            recommendations.extend([
                {
                    'text': 'Review production schedules to avoid simultaneous equipment startup causing energy spikes.',
                    'priority': 'high',
                    'estimated_savings': insight.potential_savings_inr * 0.3 if insight.potential_savings_inr else 4000,
                    'difficulty': 'low'
                },
                {
                    'text': 'Install soft starters on heavy machinery to reduce startup energy consumption.',
                    'priority': 'medium',
                    'estimated_savings': insight.potential_savings_inr * 0.2 if insight.potential_savings_inr else 3000,
                    'difficulty': 'medium'
                }
            ])
        elif 'hvac' in equipment:
            recommendations.extend([
                {
                    'text': 'Calibrate HVAC thermostat controls and check for faulty sensors causing system overruns.',
                    'priority': 'high',
                    'estimated_savings': insight.potential_savings_inr * 0.3 if insight.potential_savings_inr else 4000,
                    'difficulty': 'low'
                },
                {
                    'text': 'Implement HVAC demand control ventilation to adjust airflow based on occupancy.',
                    'priority': 'medium',
                    'estimated_savings': insight.potential_savings_inr * 0.2 if insight.potential_savings_inr else 3000,
                    'difficulty': 'medium'
                }
            ])
        
        return recommendations
    
    def _get_high_consumption_recommendations(self, insight):
        """Recommendations for high energy consumption"""
        dept = insight.department.lower() if insight.department else ''
        equipment = insight.equipment.lower() if insight.equipment else 'equipment'
        
        recommendations = [
            {
                'text': f'Conduct detailed energy audit of {insight.equipment} in {insight.department} to identify optimization opportunities.',
                'priority': 'high',
                'estimated_savings': insight.potential_savings_inr * 0.3 if insight.potential_savings_inr else 5000,
                'difficulty': 'medium'
            }
        ]
        
        if 'data center' in dept or 'server' in equipment:
            recommendations.extend([
                {
                    'text': 'Upgrade to energy-efficient servers and implement hot aisle/cold aisle containment in data center.',
                    'priority': 'high',
                    'estimated_savings': insight.potential_savings_inr * 0.4 if insight.potential_savings_inr else 6000,
                    'difficulty': 'high'
                },
                {
                    'text': 'Implement dynamic power management for servers based on workload demands.',
                    'priority': 'medium',
                    'estimated_savings': insight.potential_savings_inr * 0.2 if insight.potential_savings_inr else 3000,
                    'difficulty': 'medium'
                }
            ])
        elif 'production' in dept or 'manufacturing' in dept:
            recommendations.extend([
                {
                    'text': 'Replace old motors with high-efficiency models in production equipment.',
                    'priority': 'high',
                    'estimated_savings': insight.potential_savings_inr * 0.3 if insight.potential_savings_inr else 5000,
                    'difficulty': 'high'
                },
                {
                    'text': 'Optimize production schedules to run equipment during off-peak hours when possible.',
                    'priority': 'medium',
                    'estimated_savings': insight.potential_savings_inr * 0.2 if insight.potential_savings_inr else 3000,
                    'difficulty': 'low'
                }
            ])
        elif 'lighting' in equipment:
            recommendations.extend([
                {
                    'text': 'Replace existing lighting with LED fixtures and install occupancy sensors.',
                    'priority': 'high',
                    'estimated_savings': insight.potential_savings_inr * 0.4 if insight.potential_savings_inr else 6000,
                    'difficulty': 'medium'
                },
                {
                    'text': 'Implement daylight harvesting systems to reduce artificial lighting during daytime.',
                    'priority': 'medium',
                    'estimated_savings': insight.potential_savings_inr * 0.2 if insight.potential_savings_inr else 3000,
                    'difficulty': 'low'
                }
            ])
        
        return recommendations
    
    def _get_trend_recommendations(self, insight):
        """Recommendations for energy consumption trends"""
        recommendations = [
            {
                'text': f'Analyze historical consumption patterns in {insight.department} to identify root causes of increasing energy usage.',
                'priority': 'high',
                'estimated_savings': insight.potential_savings_inr * 0.3 if insight.potential_savings_inr else 4000,
                'difficulty': 'low'
            },
            {
                'text': f'Implement continuous energy monitoring for {insight.equipment} to detect anomalies early.',
                'priority': 'medium',
                'estimated_savings': insight.potential_savings_inr * 0.2 if insight.potential_savings_inr else 3000,
                'difficulty': 'medium'
            },
            {
                'text': f'Set up automated alerts for unusual consumption patterns in {insight.department}.',
                'priority': 'medium',
                'estimated_savings': insight.potential_savings_inr * 0.1 if insight.potential_savings_inr else 2000,
                'difficulty': 'low'
            }
        ]
        
        return recommendations
    
    def _get_department_analysis(self, insight):
        """Get department-specific analysis"""
        dept = insight.department.lower()
        
        if 'data center' in dept:
            return """
Data Center Specific Analysis:
- High energy consumption is typical for data centers due to 24/7 operations
- Focus on cooling efficiency and server optimization
- Consider implementing hot aisle/cold aisle containment
- Evaluate server utilization and consolidation opportunities
"""
        elif 'production' in dept or 'manufacturing' in dept:
            return """
Production Department Analysis:
- Manufacturing equipment typically consumes significant energy
- Focus on motor efficiency and process optimization
- Consider variable frequency drives for equipment
- Evaluate production scheduling for energy efficiency
"""
        elif 'hvac' in dept:
            return """
HVAC Department Analysis:
- HVAC systems are major energy consumers in most facilities
- Focus on thermostat settings and maintenance schedules
- Consider building automation systems
- Evaluate filter replacement and duct cleaning schedules
"""
        else:
            return f"""
{insight.department} Department Analysis:
- Analyze specific equipment usage patterns
- Focus on operational efficiency improvements
- Consider department-specific energy conservation measures
- Evaluate staff training requirements for energy management
"""
    
    def _format_recommendations(self, recommendations):
        """Format recommendations for analysis text"""
        formatted = []
        for i, rec in enumerate(recommendations, 1):
            formatted.append(f"{i}. {rec['text']} (Priority: {rec['priority']}, Estimated Savings: ₹{rec['estimated_savings']:.2f})")
        return '\n'.join(formatted)
