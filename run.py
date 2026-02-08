#!/usr/bin/env python3
"""
WattWise AI - Energy Optimization Platform
Production-ready B2B SaaS application for Indian industries
"""

import os
from app import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Development server configuration
    debug_mode = True  # Force debug mode for development
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 Starting WattWise AI - Energy Optimization Platform")
    print(f"📊 Environment: {'Development' if debug_mode else 'Production'}")
    print(f"🌐 Server running on: http://localhost:{port}")
    print("💡 AI-Powered Energy Waste Detection and Optimization")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
