from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import os
import google.generativeai as genai
from werkzeug.utils import secure_filename
import json
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wattwise-ai-energy-optimization-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
CORS(app, supports_credentials=True)

# Configure Gemini AI - Replace with your actual API key
genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")
model = genai.GenerativeModel('gemini-pro')

def init_db():
    conn = sqlite3.connect('wattwise.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            company_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS energy_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp TEXT,
            energy_kwh REAL,
            department TEXT,
            equipment TEXT,
            cost_inr REAL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

class EnergyAnalytics:
    @staticmethod
    def detect_anomalies(df):
        df['energy_kwh'] = pd.to_numeric(df['energy_kwh'], errors='coerce')
        
        mean_consumption = df['energy_kwh'].mean()
        std_consumption = df['energy_kwh'].std()
        threshold = mean_consumption + (2 * std_consumption)
        
        anomalies = df[df['energy_kwh'] > threshold].copy()
        dept_consumption = df.groupby('department')['energy_kwh'].agg(['sum', 'mean', 'count']).round(2)
        equipment_consumption = df.groupby('equipment')['energy_kwh'].agg(['sum', 'mean', 'count']).round(2)
        
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        hourly_pattern = df.groupby('hour')['energy_kwh'].mean().round(2)
        
        return {
            'total_consumption': float(df['energy_kwh'].sum()),
            'average_consumption': float(mean_consumption),
            'anomalies_count': len(anomalies),
            'anomalies': anomalies.to_dict('records'),
            'department_analysis': dept_consumption.to_dict('index'),
            'equipment_analysis': equipment_consumption.to_dict('index'),
            'hourly_pattern': hourly_pattern.to_dict(),
            'peak_hour': int(hourly_pattern.idxmax()),
            'total_cost_inr': float(df['cost_inr'].sum()) if 'cost_inr' in df.columns else 0
        }
    
    @staticmethod
    def generate_insights(analytics_data):
        prompt = f"""
        As an Energy Optimization Consultant for Indian industries, analyze this energy consumption data:

        Total Consumption: {analytics_data['total_consumption']} kWh
        Total Cost: ₹{analytics_data['total_cost_inr']:,.2f}
        Anomalies: {analytics_data['anomalies_count']}
        Peak Hour: {analytics_data['peak_hour']}:00

        Provide:
        1. Key findings in business language
        2. Cost-saving recommendations for Indian industrial context
        3. Implementation priority

        Keep response professional and actionable.
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "AI analysis temporarily unavailable. Manual insights: High consumption detected in peak hours. Consider load balancing and equipment optimization."

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    conn = sqlite3.connect('wattwise.db')
    cursor = conn.cursor()
    
    try:
        hashed_password = generate_password_hash(data['password'])
        cursor.execute(
            'INSERT INTO users (email, password, company_name) VALUES (?, ?, ?)',
            (data['email'], hashed_password, data['company_name'])
        )
        conn.commit()
        return jsonify({'message': 'Registration successful'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already registered'}), 400
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    conn = sqlite3.connect('wattwise.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, password, company_name FROM users WHERE email = ?', (data['email'],))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[1], data['password']):
        session['user_id'] = user[0]
        session['company_name'] = user[2]
        return jsonify({
            'message': 'Login successful',
            'user': {'id': user[0], 'company_name': user[2]}
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/upload-energy-data', methods=['POST'])
@login_required
def upload_energy_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.csv'):
        return jsonify({'error': 'Please upload a CSV file'}), 400
    
    try:
        df = pd.read_csv(file)
        required_columns = ['timestamp', 'energy_kwh', 'department', 'equipment']
        
        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': f'CSV must contain columns: {required_columns}'}), 400
        
        # Add cost calculation (₹6.5 per kWh - Indian industrial rate)
        df['cost_inr'] = df['energy_kwh'] * 6.5
        
        conn = sqlite3.connect('wattwise.db')
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO energy_data (user_id, timestamp, energy_kwh, department, equipment, cost_inr)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (session['user_id'], row['timestamp'], row['energy_kwh'], 
                  row['department'], row['equipment'], row['cost_inr']))
        
        conn.commit()
        conn.close()
        
        analytics = EnergyAnalytics.detect_anomalies(df)
        ai_insights = EnergyAnalytics.generate_insights(analytics)
        
        return jsonify({
            'message': f'Successfully processed {len(df)} energy records',
            'analytics': analytics,
            'ai_insights': ai_insights
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/api/dashboard-data', methods=['GET'])
@login_required
def get_dashboard_data():
    conn = sqlite3.connect('wattwise.db')
    
    df = pd.read_sql_query('''
        SELECT * FROM energy_data 
        WHERE user_id = ? 
        ORDER BY uploaded_at DESC 
        LIMIT 1000
    ''', conn, params=(session['user_id'],))
    
    conn.close()
    
    if df.empty:
        return jsonify({'message': 'No energy data found. Please upload your first dataset.'}), 200
    
    analytics = EnergyAnalytics.detect_anomalies(df)
    return jsonify(analytics), 200

@app.route('/api/ask-ai', methods=['POST'])
@login_required
def ask_ai():
    data = request.get_json()
    question = data.get('question', '')
    
    conn = sqlite3.connect('wattwise.db')
    df = pd.read_sql_query('''
        SELECT * FROM energy_data 
        WHERE user_id = ? 
        ORDER BY uploaded_at DESC 
        LIMIT 500
    ''', conn, params=(session['user_id'],))
    conn.close()
    
    if df.empty:
        return jsonify({'answer': 'Please upload energy data first to get AI insights.'}), 200
    
    analytics = EnergyAnalytics.detect_anomalies(df)
    
    prompt = f"""
    As WattWise AI Energy Consultant, answer: {question}
    
    Current Energy Context:
    - Total Consumption: {analytics['total_consumption']} kWh
    - Total Cost: ₹{analytics['total_cost_inr']:,.2f}
    - Anomalies: {analytics['anomalies_count']}
    
    Provide actionable answer for Indian industrial context.
    """
    
    try:
        response = model.generate_content(prompt)
        return jsonify({'answer': response.text}), 200
    except Exception as e:
        return jsonify({'answer': 'AI service temporarily unavailable. Please try again later.'}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    init_db()
    app.run(debug=True, port=5000)