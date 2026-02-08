#!/usr/bin/env python3
"""
Reset all uploads to start fresh with Upload #1
"""

from app import create_app, db
from app.models import EnergyData, EnergyInsight

def reset_all_uploads():
    """Delete all energy data and insights to start fresh"""
    app = create_app()
    
    with app.app_context():
        try:
            # Delete all energy insights first (due to potential foreign key constraints)
            insights_count = EnergyInsight.query.count()
            print(f"Deleting {insights_count} energy insights...")
            EnergyInsight.query.delete()
            
            # Delete all energy data
            data_count = EnergyData.query.count()
            print(f"Deleting {data_count} energy data records...")
            EnergyData.query.delete()
            
            # Commit changes
            db.session.commit()
            print("Successfully reset all uploads!")
            print("You can now start fresh with Upload #1")
            
        except Exception as e:
            print(f"Error resetting uploads: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    reset_all_uploads()
