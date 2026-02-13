#!/usr/bin/env python3
"""
Database initialization script for WattWise AI
Run this to create all database tables
"""

from app import create_app, db
from app.models import User, EnergyData, EnergyInsight, AIRecommendation

def init_database():
    """Initialize the database with all tables"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Creating database tables...")
        
        # Drop all tables (use with caution in production!)
        # db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("✅ Database tables created successfully!")
        print("\nTables created:")
        print("  - user")
        print("  - energy_data")
        print("  - energy_insight")
        print("  - ai_recommendation")
        
        # Verify tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n📊 Total tables in database: {len(tables)}")
        for table in tables:
            print(f"  ✓ {table}")

if __name__ == '__main__':
    init_database()
