#!/usr/bin/env python3
"""
Database migration script to fix password_hash column size
This fixes the "value too long for type character varying(128)" error
"""

from app import create_app, db
from sqlalchemy import text

def migrate_password_hash_column():
    """Increase password_hash column size from 128 to 256"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Starting database migration...")
            print("📊 Altering password_hash column size...")
            
            # For PostgreSQL
            db.session.execute(text(
                'ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(256);'
            ))
            
            db.session.commit()
            
            print("✅ Migration completed successfully!")
            print("   password_hash column is now VARCHAR(256)")
            
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            print("\nNote: If you're using SQLite, you may need to recreate the database.")
            print("For PostgreSQL, this should work automatically.")
            db.session.rollback()
            raise

if __name__ == '__main__':
    migrate_password_hash_column()
