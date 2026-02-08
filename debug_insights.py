#!/usr/bin/env python3
"""
Debug script to check insights in database
"""

from app import create_app, db
from app.models import EnergyInsight, EnergyData

def debug_insights():
    """Debug insights in database"""
    app = create_app()
    
    with app.app_context():
        # Check all insights
        all_insights = EnergyInsight.query.all()
        print(f"Total insights in database: {len(all_insights)}")
        
        for insight in all_insights:
            print(f"Insight {insight.id}: {insight.file_name} - {insight.title}")
        
        # Check specific files
        files_to_check = ['it_company_energy_data.csv', 'manufacturing_energy_data.csv']
        
        for file_name in files_to_check:
            insights = EnergyInsight.query.filter_by(file_name=file_name).all()
            print(f"\n{file_name}: {len(insights)} insights")
            for insight in insights:
                print(f"  - {insight.insight_type}: {insight.title}")

if __name__ == '__main__':
    debug_insights()
