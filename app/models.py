from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    company_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # API Configuration
    gemini_api_key = db.Column(db.String(255))
    
    energy_data = db.relationship('EnergyData', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class EnergyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    energy_kwh = db.Column(db.Float, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    equipment = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(100))
    cost_inr = db.Column(db.Float)
    is_anomaly = db.Column(db.Boolean, default=False)
    anomaly_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # File tracking
    file_name = db.Column(db.String(255))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EnergyData {self.timestamp} - {self.energy_kwh} kWh>'

class EnergyInsight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    insight_type = db.Column(db.String(50), nullable=False)  # 'spike', 'trend', 'high_consumption'
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(100))
    equipment = db.Column(db.String(100))
    severity = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high'
    potential_savings_inr = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # File tracking
    file_name = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<EnergyInsight {self.insight_type} - {self.title}>'

class AIRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    insight_id = db.Column(db.Integer, db.ForeignKey('energy_insight.id'), nullable=False)
    recommendation = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium')
    estimated_savings_inr = db.Column(db.Float)
    implementation_difficulty = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    insight = db.relationship('EnergyInsight', backref='recommendations')
    
    def __repr__(self):
        return f'<AIRecommendation {self.priority} priority>'
