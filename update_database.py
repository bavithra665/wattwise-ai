#!/usr/bin/env python3
"""
Database migration script to add file tracking columns
"""

from app import create_app, db
from app.models import EnergyData

def add_file_tracking_columns():
    """Add file_name and upload_date columns to EnergyData table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('energy_data')]
            
            if 'file_name' not in columns:
                print("Adding file_name column...")
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE energy_data ADD COLUMN file_name VARCHAR(255)'))
            
            if 'upload_date' not in columns:
                print("Adding upload_date column...")
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE energy_data ADD COLUMN upload_date DATETIME'))
            
            # Commit changes
            db.session.commit()
            print("Database migration completed successfully!")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    add_file_tracking_columns()
