from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import pandas as pd
import os
from datetime import datetime
from app.models import EnergyData, EnergyInsight, AIRecommendation
from app.energy_analyzer import EnergyAnalyzer
from app.ai_consultant import AIConsultant
from app.forms import SettingsForm, UploadForm
from app import db
from . import bp

@bp.route('/')
def index():
    return render_template('index.html', title='WattWise AI - Energy Optimization Platform')

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's energy data
    energy_data = EnergyData.query.filter_by(user_id=current_user.id).order_by(EnergyData.timestamp.desc()).limit(100).all()
    insights = EnergyInsight.query.filter_by(user_id=current_user.id).order_by(EnergyInsight.created_at.desc()).limit(10).all()
    
    # Calculate summary statistics
    total_consumption = sum(data.energy_kwh for data in energy_data)
    total_cost = sum(data.cost_inr or 0 for data in energy_data)
    anomaly_count = sum(1 for data in energy_data if data.is_anomaly)
    
    stats = {
        'total_consumption_kwh': round(total_consumption, 2),
        'total_cost_inr': round(total_cost, 2),
        'anomaly_count': anomaly_count,
        'data_points': len(energy_data)
    }
    
    return render_template('dashboard.html', 
                         title='Energy Dashboard',
                         energy_data=energy_data,
                         insights=insights,
                         stats=stats)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_data():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and file.filename.endswith('.csv'):
            try:
                # Save file
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Process CSV
                df = pd.read_csv(filepath)
                
                # Add file name and upload date to all records for tracking
                df['file_name'] = filename
                df['upload_date'] = datetime.utcnow()
                
                # Validate required columns
                required_columns = ['timestamp', 'energy_kwh', 'department', 'equipment']
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    flash(f'Missing required columns: {", ".join(missing_columns)}', 'error')
                    return render_template('upload.html', form=form, title='Upload Energy Data')
                
                # Process data
                analyzer = EnergyAnalyzer()
                insights_generated = analyzer.process_energy_data(df, current_user.id)
                
                flash(f'Successfully uploaded and analyzed {len(df)} energy records. Generated {insights_generated} insights.', 'success')
                return redirect(url_for('main.dashboard'))
                
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'error')
                return render_template('upload.html', form=form, title='Upload Energy Data')
        else:
            flash('Please upload a CSV file', 'error')
            return render_template('upload.html', form=form, title='Upload Energy Data')
    
    return render_template('upload.html', form=form, title='Upload Energy Data')

@bp.route('/upload-sample-data', methods=['POST'])
@login_required
def upload_sample_data():
    """Upload sample IT company energy data for testing"""
    try:
        # Simple CSRF validation using Flask-WTF's built-in validation
        from flask_wtf.csrf import validate_csrf
        
        csrf_token = request.form.get('csrf_token')
        if not csrf_token:
            return jsonify({
                'success': False,
                'message': 'CSRF token missing'
            })
        
        try:
            validate_csrf(csrf_token)
        except Exception as csrf_error:
            return jsonify({
                'success': False,
                'message': 'Invalid CSRF token'
            })
        
        import pandas as pd
        import os
        from datetime import datetime
        
        # Path to sample data file
        sample_file_path = os.path.join(current_app.root_path, '..', 'sample_data', 'it_company_energy_data.csv')
        
        if not os.path.exists(sample_file_path):
            return jsonify({
                'success': False,
                'message': 'Sample data file not found'
            })
        
        # Read the sample CSV
        df = pd.read_csv(sample_file_path)
        
        # Add file name and upload date for tracking
        df['file_name'] = 'it_company_energy_data.csv'
        df['upload_date'] = datetime.utcnow()
        
        # Process the data using the existing analyzer
        analyzer = EnergyAnalyzer()
        insights_generated = analyzer.process_energy_data(df, current_user.id)
        
        return jsonify({
            'success': True,
            'message': f'Successfully uploaded and analyzed {len(df)} IT company energy records. Generated {insights_generated} insights.'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error uploading sample data: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error processing sample data: {str(e)}'
        })

@bp.route('/insights')
@login_required
def insights():
    # Get filter parameters
    file_filter = request.args.get('file')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Base query for insights
    insights_query = EnergyInsight.query.filter_by(user_id=current_user.id)
    
    # Apply file filter if provided
    if file_filter:
        # Filter insights directly by file_name
        insights_query = insights_query.filter(EnergyInsight.file_name == file_filter)
    
    # Apply date range filter if provided
    if start_date:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        insights_query = insights_query.filter(EnergyInsight.created_at >= start_date_obj)
    
    if end_date:
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        insights_query = insights_query.filter(EnergyInsight.created_at <= end_date_obj)
    
    # Get filtered insights
    all_insights = insights_query.order_by(EnergyInsight.created_at.desc()).all()
    
    # Get upload history with sequential numbering (oldest first)
    upload_history_query = db.session.query(
        EnergyData.file_name, 
        EnergyData.upload_date,
        db.func.count(EnergyData.id).label('record_count'),
        db.func.min(EnergyData.id).label('min_id'),
        db.func.max(EnergyData.id).label('max_id')
    ).filter_by(user_id=current_user.id)\
    .group_by(EnergyData.file_name, EnergyData.upload_date)\
    .order_by(EnergyData.upload_date.asc())\
    .distinct()
    
    upload_history = []
    upload_number = 1
    for upload in upload_history_query:
        upload_history.append({
            'file_name': upload.file_name,
            'upload_date': upload.upload_date,
            'record_count': upload.record_count,
            'upload_number': upload_number,
            'min_id': upload.min_id,
            'max_id': upload.max_id
        })
        upload_number += 1
    
    # Reverse the list to show newest first but keep correct numbering
    upload_history = list(reversed(upload_history))
    
    return render_template('insights.html', 
                     title='Energy Insights', 
                     insights=all_insights,
                     upload_history=upload_history,
                     current_file_filter=file_filter,
                     current_start_date=start_date,
                     current_end_date=end_date)

@bp.route('/compare-uploads')
@login_required
def compare_uploads():
    """Compare two different uploads"""
    upload1 = request.args.get('upload1')
    upload2 = request.args.get('upload2')
    
    if not upload1 or not upload2:
        flash('Please select two uploads to compare', 'error')
        return redirect(url_for('main.insights'))
    
    # Get data for both uploads
    upload1_data = EnergyData.query.filter_by(user_id=current_user.id, file_name=upload1).all()
    upload2_data = EnergyData.query.filter_by(user_id=current_user.id, file_name=upload2).all()
    
    # Get insights for both uploads
    upload1_insights = EnergyInsight.query.filter_by(user_id=current_user.id, file_name=upload1).all()
    upload2_insights = EnergyInsight.query.filter_by(user_id=current_user.id, file_name=upload2).all()
    
    # Calculate comparison metrics
    upload1_total = sum(d.energy_kwh for d in upload1_data)
    upload2_total = sum(d.energy_kwh for d in upload2_data)
    upload1_cost = sum(d.cost_inr for d in upload1_data)
    upload2_cost = sum(d.cost_inr for d in upload2_data)
    
    comparison_data = {
        'upload1': {
            'file_name': upload1,
            'total_energy': upload1_total,
            'total_cost': upload1_cost,
            'record_count': len(upload1_data),
            'insight_count': len(upload1_insights),
            'insights': upload1_insights
        },
        'upload2': {
            'file_name': upload2,
            'total_energy': upload2_total,
            'total_cost': upload2_cost,
            'record_count': len(upload2_data),
            'insight_count': len(upload2_insights),
            'insights': upload2_insights
        },
        'differences': {
            'energy_change': upload2_total - upload1_total,
            'cost_change': upload2_cost - upload1_cost,
            'energy_percent': ((upload2_total - upload1_total) / upload1_total * 100) if upload1_total > 0 else 0,
            'cost_percent': ((upload2_cost - upload1_cost) / upload1_cost * 100) if upload1_cost > 0 else 0,
            'insight_change': len(upload2_insights) - len(upload1_insights)
        }
    }
    
    return render_template('compare_uploads.html', 
                     title='Upload Comparison', 
                     comparison=comparison_data)

@bp.route('/ai-analysis')
@login_required
def ai_analysis():
    insight_id = request.args.get('insight_id')
    if not insight_id:
        flash('Please select an insight to analyze', 'error')
        return redirect(url_for('main.insights'))
    
    insight = EnergyInsight.query.filter_by(id=insight_id, user_id=current_user.id).first()
    if not insight:
        flash('Insight not found', 'error')
        return redirect(url_for('main.insights'))
    
    # Get AI analysis
    consultant = AIConsultant(user=current_user)
    analysis = consultant.get_insight_analysis(insight, current_user.id)
    
    return render_template('ai_analysis.html', title='AI Energy Analysis', insight=insight, analysis=analysis)

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    
    if form.validate_on_submit():
        # Update user's API key
        current_user.gemini_api_key = form.gemini_api_key.data
        db.session.commit()
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('main.settings'))
    
    # Handle Cancel action
    if request.args.get('action') == 'cancel':
        current_user.gemini_api_key = None
        db.session.commit()
        flash('API key disconnected successfully!', 'info')
        return redirect(url_for('main.settings'))
    
    # Pre-fill form with current API key
    form.gemini_api_key.data = current_user.gemini_api_key or ''
    
    return render_template('settings.html', title='Settings', form=form)
