#!/usr/bin/env python3
"""
Add file_name column to EnergyInsight table and update existing records
"""

from app import create_app, db
from app.models import EnergyInsight, EnergyData

def add_insight_file_tracking():
    """Add file_name column and update existing insights"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('energy_insight')]
            
            if 'file_name' not in columns:
                print("Adding file_name column to energy_insight table...")
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE energy_insight ADD COLUMN file_name VARCHAR(255)'))
            
            # Update existing insights with file names from energy data
            insights_without_filename = EnergyInsight.query.filter(
                (EnergyInsight.file_name.is_(None)) | (EnergyInsight.file_name == '')
            ).all()
            
            print(f"Found {len(insights_without_filename)} insights without file names")
            
            if insights_without_filename:
                for insight in insights_without_filename:
                    # Find energy data with same department and equipment from same user
                    matching_data = EnergyData.query.filter_by(
                        user_id=insight.user_id,
                        department=insight.department,
                        equipment=insight.equipment
                    ).first()
                    
                    if matching_data and matching_data.file_name:
                        insight.file_name = matching_data.file_name
                        print(f"Updated insight {insight.id} with file_name: {matching_data.file_name}")
                
                # Commit changes
                db.session.commit()
                print("Successfully updated existing insights!")
            
            else:
                print("No insights need updating")
                
        except Exception as e:
            print(f"Error updating insights: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    add_insight_file_tracking()
