#!/usr/bin/env python3
"""
Add gemini_api_key column to users table
"""

from app import create_app, db

def add_api_key_column():
    """Add gemini_api_key column to users table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('user')]
            
            if 'gemini_api_key' not in columns:
                print("Adding gemini_api_key column to user table...")
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE user ADD COLUMN gemini_api_key VARCHAR(255)'))
                print("Successfully added gemini_api_key column!")
            else:
                print("gemini_api_key column already exists!")
                
        except Exception as e:
            print(f"Error adding column: {e}")
            raise

if __name__ == '__main__':
    add_api_key_column()
