#!/usr/bin/env python3
"""
Fix existing data to have proper file names and upload dates
"""

from app import create_app, db
from app.models import EnergyData
from datetime import datetime

def fix_existing_data():
    """Update existing records with proper file names and upload dates"""
    app = create_app()
    
    with app.app_context():
        try:
            # Get all records that don't have file_name
            records_without_filename = EnergyData.query.filter(
                (EnergyData.file_name.is_(None)) | (EnergyData.file_name == '')
            ).all()
            
            print(f"Found {len(records_without_filename)} records without file names")
            
            if records_without_filename:
                # Group records by user and upload date to assign filenames
                user_uploads = {}
                
                for record in records_without_filename:
                    user_id = record.user_id
                    
                    if user_id not in user_uploads:
                        user_uploads[user_id] = []
                    
                    user_uploads[user_id].append(record)
                
                # Update each user's records
                for user_id, records in user_uploads.items():
                    # Group by created_at to identify different uploads
                    upload_groups = {}
                    
                    for record in records:
                        # Use created_at as upload identifier (rounded to nearest hour)
                        upload_key = record.created_at.replace(minute=0, second=0, microsecond=0)
                        
                        if upload_key not in upload_groups:
                            upload_groups[upload_key] = []
                        
                        upload_groups[upload_key].append(record)
                    
                    # Assign filenames to each upload group
                    upload_num = 1
                    for upload_key, group_records in upload_groups.items():
                        filename = f"energy_data_upload_{upload_num}.csv"
                        upload_date = upload_key
                        
                        print(f"Updating {len(group_records)} records with filename: {filename}")
                        
                        for record in group_records:
                            record.file_name = filename
                            record.upload_date = upload_date
                        
                        upload_num += 1
                
                # Commit changes
                db.session.commit()
                print("Successfully updated existing records!")
            
            else:
                print("No records need updating")
                
        except Exception as e:
            print(f"Error updating data: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    fix_existing_data()
