from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///wattwise.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 Starting WattWise AI")
    logger.info(f"📊 Database: {app.config['SQLALCHEMY_DATABASE_URI'][:20]}...")
    
    # Initialize extensions
    try:
        db.init_app(app)
        login_manager.init_app(app)
        csrf.init_app(app)
        logger.info("✅ Extensions initialized successfully")
    except Exception as e:
        logger.error(f"❌ Error initializing extensions: {str(e)}")
        raise
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Create upload directory
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        logger.info(f"✅ Upload folder created: {app.config['UPLOAD_FOLDER']}")
    except Exception as e:
        logger.warning(f"⚠️ Could not create upload folder: {str(e)}")
    
    # Register blueprints
    try:
        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        
        from app.main import bp as main_bp
        app.register_blueprint(main_bp)
        
        from app.api import bp as api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        logger.info("✅ Blueprints registered successfully")
    except Exception as e:
        logger.error(f"❌ Error registering blueprints: {str(e)}")
        raise
    
    # Custom Jinja filters
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """Convert newlines to <br> tags"""
        if text is None:
            return ''
        return str(text).replace('\n', '<br>\n')
    
    # Error handlers
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"❌ Internal Server Error: {str(error)}")
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    # Create database tables
    with app.app_context():
        try:
            logger.info("🔧 Checking database schema...")
            db.create_all()
            
            # AUTOMATIC MIGRATION: Fix password_hash column size
            # This is safe to run multiple times on PostgreSQL
            if 'postgresql' in str(db.engine.url).lower():
                try:
                    from sqlalchemy import text
                    db.session.execute(text('ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(256);'))
                    db.session.commit()
                    logger.info("✅ Database migration: password_hash column ensured to be 256 chars")
                except Exception as mig_err:
                    logger.warning(f"⚠️ Auto-migration skipped/failed: {str(mig_err)}")
                    db.session.rollback()
            
            # Verify tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            logger.info(f"✅ Database tables verified: {', '.join(tables)}")
        except Exception as e:
            logger.error(f"❌ Error during database initialization: {str(e)}")
            logger.error("⚠️ Application will continue, but database operations may fail")
    
    logger.info("🎉 WattWise AI initialized successfully")
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
