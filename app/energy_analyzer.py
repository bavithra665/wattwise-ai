import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from app.models import EnergyData, EnergyInsight, db
import logging

logger = logging.getLogger(__name__)

class EnergyAnalyzer:
    def __init__(self):
        self.industrial_energy_rate = 8.50  # INR per kWh for Indian industries
        self.anomaly_threshold = 2.0  # Standard deviations for anomaly detection
        
    def process_energy_data(self, df, user_id):
        """Process uploaded CSV data and generate insights"""
        try:
            # Extract file name from dataframe if available
            file_name = df['file_name'].iloc[0] if 'file_name' in df.columns else None
            
            # Clean and validate data
            df = self._clean_data(df)
            
            # Calculate costs
            df['cost_inr'] = df['energy_kwh'] * self.industrial_energy_rate
            
            # Detect anomalies
            df = self._detect_anomalies(df)
            
            # Save to database
            records_saved = self._save_energy_data(df, user_id)
            
            # Generate insights
            insights_generated = self._generate_insights(df, user_id, file_name)
            
            return insights_generated
            
        except Exception as e:
            logger.error(f"Error processing energy data: {str(e)}")
            raise
    
    def _clean_data(self, df):
        """Clean and validate the energy data"""
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['timestamp', 'department', 'equipment'])
        
        # Handle missing values
        df = df.dropna(subset=['energy_kwh', 'department', 'equipment'])
        
        # Filter out unrealistic values (negative or extremely high consumption)
        df = df[(df['energy_kwh'] > 0) & (df['energy_kwh'] < 10000)]
        
        # Sort by timestamp
        df = df.sort_values('timestamp')
        
        return df
    
    def _detect_anomalies(self, df):
        """Detect energy consumption anomalies using statistical methods"""
        # Calculate baseline statistics for each department
        dept_stats = {}
        
        for dept in df['department'].unique():
            dept_data = df[df['department'] == dept]['energy_kwh']
            dept_stats[dept] = {
                'mean': dept_data.mean(),
                'std': dept_data.std(),
                'median': dept_data.median()
            }
        
        # Detect anomalies based on department baselines
        anomalies = []
        for idx, row in df.iterrows():
            dept = row['department']
            consumption = row['energy_kwh']
            
            if dept in dept_stats:
                stats = dept_stats[dept]
                z_score = abs(consumption - stats['mean']) / stats['std'] if stats['std'] > 0 else 0
                
                # Mark as anomaly if significantly different from baseline
                is_anomaly = z_score > self.anomaly_threshold
                anomalies.append(is_anomaly)
            else:
                anomalies.append(False)
        
        df['is_anomaly'] = anomalies
        df['anomaly_score'] = [abs(row['energy_kwh'] - dept_stats.get(row['department'], {}).get('mean', row['energy_kwh'])) 
                               for idx, row in df.iterrows()]
        
        return df
    
    def _save_energy_data(self, df, user_id):
        """Save energy data to database"""
        records_saved = 0
        
        for _, row in df.iterrows():
            energy_record = EnergyData(
                user_id=user_id,
                timestamp=row['timestamp'],
                energy_kwh=row['energy_kwh'],
                department=row['department'],
                equipment=row['equipment'],
                building=row.get('building', ''),
                cost_inr=row['cost_inr'],
                is_anomaly=row['is_anomaly'],
                anomaly_score=row['anomaly_score'],
                file_name=row.get('file_name'),
                upload_date=row.get('upload_date')
            )
            
            db.session.add(energy_record)
            records_saved += 1
        
        db.session.commit()
        return records_saved
    
    def _generate_insights(self, df, user_id, file_name=None):
        """Generate energy insights from the data"""
        insights_generated = 0
        
        # 1. Detect significant spikes
        spike_insights = self._detect_energy_spikes(df, user_id, file_name)
        insights_generated += len(spike_insights)
        
        # 2. Identify high consumption departments
        high_consumption_insights = self._identify_high_consumption(df, user_id, file_name)
        insights_generated += len(high_consumption_insights)
        
        # 3. Analyze trends
        trend_insights = self._analyze_trends(df, user_id, file_name)
        insights_generated += len(trend_insights)
        
        return insights_generated
    
    def _detect_energy_spikes(self, df, user_id, file_name=None):
        """Detect and create insights for energy spikes"""
        insights = []
        
        # Find significant anomalies
        anomalies = df[df['is_anomaly'] == True]
        
        for _, row in anomalies.iterrows():
            # Calculate potential savings (assuming 30% reduction possible)
            potential_savings = row['energy_kwh'] * 0.3 * self.industrial_energy_rate
            
            insight = EnergyInsight(
                user_id=user_id,
                insight_type='spike',
                title=f'Energy Spike Detected - {row["department"]}',
                description=f'Unusual energy consumption of {row["energy_kwh"]:.2f} kWh detected in {row["department"]} department on {row["timestamp"].strftime("%Y-%m-%d %H:%M")}. This is significantly higher than the normal consumption pattern.',
                department=row['department'],
                equipment=row['equipment'],
                severity='high' if row['anomaly_score'] > 100 else 'medium',
                potential_savings_inr=potential_savings,
                file_name=file_name
            )
            
            db.session.add(insight)
            insights.append(insight)
        
        db.session.commit()
        return insights
    
    def _identify_high_consumption(self, df, user_id, file_name=None):
        """Identify departments with high energy consumption"""
        insights = []
        
        # Calculate total consumption by department
        dept_consumption = df.groupby('department')['energy_kwh'].sum().sort_values(ascending=False)
        
        # Get top 3 consuming departments
        top_departments = dept_consumption.head(3)
        
        for dept, consumption in top_departments.items():
            # Calculate potential savings (assuming 15% reduction possible through optimization)
            potential_savings = consumption * 0.15 * self.industrial_energy_rate
            
            insight = EnergyInsight(
                user_id=user_id,
                insight_type='high_consumption',
                title=f'High Energy Consumption - {dept}',
                description=f'The {dept} department has consumed {consumption:.2f} kWh, which is among the highest in your facility. Consider implementing energy-saving measures in this area.',
                department=dept,
                severity='medium',
                potential_savings_inr=potential_savings,
                file_name=file_name
            )
            
            db.session.add(insight)
            insights.append(insight)
        
        db.session.commit()
        return insights
    
    def _analyze_trends(self, df, user_id, file_name=None):
        """Analyze energy consumption trends"""
        insights = []
        
        # Group by day to analyze daily trends
        daily_consumption = df.groupby(df['timestamp'].dt.date)['energy_kwh'].sum()
        
        if len(daily_consumption) >= 7:
            # Calculate 7-day moving average
            moving_avg = daily_consumption.rolling(window=7).mean()
            
            # Check for increasing trend
            if len(moving_avg) >= 2 and moving_avg.iloc[-1] > moving_avg.iloc[-2] * 1.1:
                latest_consumption = daily_consumption.iloc[-1]
                avg_consumption = daily_consumption.mean()
                
                if latest_consumption > avg_consumption * 1.2:
                    potential_savings = (latest_consumption - avg_consumption) * 0.5 * self.industrial_energy_rate
                    
                    insight = EnergyInsight(
                        user_id=user_id,
                        insight_type='trend',
                        title='Increasing Energy Consumption Trend',
                        description=f'Energy consumption has been increasing over the past week. Latest daily consumption ({latest_consumption:.2f} kWh) is {((latest_consumption/avg_consumption)-1)*100:.1f}% higher than the average.',
                        severity='medium',
                        potential_savings_inr=potential_savings,
                        file_name=file_name
                    )
                    
                    db.session.add(insight)
                    insights.append(insight)
        
        db.session.commit()
        return insights
