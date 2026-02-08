# WattWise AI - Enterprise Energy Optimization System

## Overview

WattWise AI is a production-grade B2B SaaS web application designed for Indian industries to detect energy waste and optimize consumption patterns using artificial intelligence. The system provides real-time analytics, anomaly detection, and AI-powered recommendations to reduce energy costs by up to 30%.

## Problem Statement

Indian industries face significant challenges in energy management:
- **High Energy Costs**: Industrial electricity rates averaging ₹8.50/kWh
- **Inefficient Consumption**: Lack of visibility into energy usage patterns
- **Manual Monitoring**: Time-intensive manual analysis of energy data
- **Compliance Requirements**: Need for sustainability reporting and energy efficiency standards

## Solution

WattWise AI provides:
- **Automated Anomaly Detection**: Statistical analysis to identify energy spikes and waste
- **AI-Powered Insights**: Gemini 3 integration for intelligent recommendations
- **Cost Analysis**: Real-time cost calculations in Indian Rupees (INR)
- **Department-wise Analytics**: Granular consumption tracking by department and equipment
- **Actionable Recommendations**: Practical steps to reduce energy consumption

## Architecture

### Backend (Flask)
- **Energy Analytics Engine**: Rule-based and statistical anomaly detection using scikit-learn
- **Database**: SQLAlchemy with SQLite for development, PostgreSQL for production
- **AI Integration**: Google Gemini 3 for intelligent insights
- **API Design**: RESTful endpoints with proper authentication and validation
- **Authentication**: Flask-Login with secure session management

### Frontend (Bootstrap 5 + JavaScript)
- **Professional Dashboard**: Enterprise-grade UI with Chart.js visualizations
- **Authentication System**: Secure user registration and login with CSRF protection
- **Data Visualization**: Interactive charts showing energy trends and patterns
- **Responsive Design**: Mobile-friendly interface optimized for all devices

### Data Flow
1. **CSV Upload**: Historical energy data from enterprise systems
2. **Data Processing**: Validation, parsing, and cost calculation at ₹8.50/kWh
3. **Analytics**: Anomaly detection using Isolation Forest and statistical methods
4. **AI Analysis**: Gemini 3 generates insights and recommendations
5. **Dashboard**: Visual presentation of findings and KPIs

## CSV Data Format

The system accepts CSV files with the following structure:

```csv
timestamp,energy_kwh,department,equipment,building
2024-01-15 08:00:00,125.5,Production,Injection-Molding-Machine-A,Factory-1
2024-01-15 09:00:00,142.8,Production,Injection-Molding-Machine-A,Factory-1
2024-01-15 10:00:00,98.3,HVAC,Cooling-System,Main-Office
```

**Required Columns:**
- `timestamp`: Date and time (YYYY-MM-DD HH:MM:SS)
- `energy_kwh`: Energy consumption in kilowatt-hours (numeric)
- `department`: Department or area name (text)
- `equipment`: Equipment or source type (text)

**Optional Columns:**
- `building`: Building or facility name (text)

## Production Integration

While this system uses CSV upload for demonstration and historical data analysis, production deployments would integrate with:

- **Smart Meters**: Real-time data via IoT sensors and APIs
- **Building Management Systems (BMS)**: Direct API integration
- **SCADA Systems**: Industrial control system data feeds
- **Energy Management Platforms**: Third-party system APIs
- **Enterprise Resource Planning (ERP)**: Integration with business systems

## Key Features

### Energy Analytics
- **Baseline Analysis**: Calculate average consumption and deviation thresholds
- **Anomaly Detection**: Identify consumption spikes using Isolation Forest and statistical methods
- **Pattern Recognition**: Hourly, daily, and departmental usage patterns
- **Cost Calculation**: Automatic cost computation at ₹8.50/kWh (Indian industrial rate)

### AI Insights (Gemini 3)
- **Root Cause Analysis**: Explain reasons for energy spikes in business-friendly language
- **Optimization Recommendations**: Actionable steps to reduce consumption
- **Business Language**: Plain English explanations for management
- **ROI Focus**: Cost savings and sustainability benefits in INR

### Dashboard Features
- **KPI Overview**: Total consumption, costs, anomalies, peak hours
- **Interactive Charts**: Energy consumption trends using Chart.js
- **Department Analysis**: Consumption breakdown by department
- **Equipment Tracking**: High-consuming equipment identification
- **AI Analysis Panel**: Professional energy consulting reports

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+ (for development tools)
- Google Gemini API key

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd wattwise-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run the application
python run.py
```

### Environment Configuration
Create a `.env` file based on `.env.example`:

```bash
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key-here
DATABASE_URL=sqlite:///wattwise.db
INDUSTRIAL_ENERGY_RATE=8.50
```

### Production Deployment
```bash
# Set production environment
export FLASK_ENV=production

# Use Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Or use Docker
docker build -t wattwise-ai .
docker run -p 5000:5000 wattwise-ai
```

## Sample Data

The project includes realistic sample datasets in `sample_data/`:

1. **manufacturing_energy_data.csv**: Manufacturing plant with production equipment, HVAC, lighting
2. **it_company_energy_data.csv**: IT company with data centers, office systems, network equipment

Both datasets contain:
- Realistic Indian industrial consumption patterns
- Energy spikes and anomalies for testing
- Department and equipment breakdown
- Timestamps covering multiple days

## Business Value

### Cost Savings
- **Energy Reduction**: 20-30% consumption decrease through optimization
- **Operational Efficiency**: Automated monitoring reduces manual effort by 80%
- **Predictive Maintenance**: Early detection of equipment inefficiencies
- **ROI**: Typical payback period of 6-12 months

### Compliance & Sustainability
- **Energy Audits**: Automated reporting for regulatory compliance
- **Carbon Footprint**: Reduced emissions through optimized consumption
- **Sustainability Goals**: Support for corporate environmental initiatives
- **ESG Reporting**: Data for environmental, social, and governance reports

### Scalability
- **Multi-facility**: Support for multiple plant locations
- **Department Granularity**: Detailed breakdown by operational areas
- **Equipment Monitoring**: Individual machine-level tracking
- **User Management**: Role-based access control

## Technology Stack

**Backend:**
- Flask 3.0.0 with modular blueprint architecture
- SQLAlchemy 3.1.1 for database ORM
- Flask-Login for authentication
- Pandas 2.1.4 for data processing
- Scikit-learn 1.3.2 for machine learning
- Google Generative AI (Gemini 3)
- Plotly 5.17.0 for charts

**Frontend:**
- Bootstrap 5.3.0 for responsive design
- Chart.js for data visualization
- Font Awesome 6.4.0 for icons
- Custom JavaScript with ES6 features
- CSS3 with modern design patterns

**Database:**
- SQLite for development
- PostgreSQL for production
- SQLAlchemy migrations for schema management

## Security Features

- **Authentication**: Secure login/logout with session management
- **CSRF Protection**: Flask-WTF for form security
- **Input Validation**: Comprehensive CSV format and data validation
- **Password Security**: bcrypt hashing for user passwords
- **Session Security**: Secure cookie configuration
- **Error Handling**: Comprehensive error management without information leakage

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Data Management
- `POST /upload` - Upload energy data CSV
- `GET /dashboard` - Main dashboard view
- `GET /insights` - Energy insights list
- `GET /ai-analysis` - AI analysis for specific insight

### API Routes
- `GET /api/energy-stats` - Energy statistics for dashboard
- `GET /api/analyze-insight/<id>` - AI analysis for insight

## Testing

```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=app tests/

# Test CSV upload functionality
python -m pytest tests/test_upload.py
```

## Monitoring & Logging

- **Application Logging**: Structured logging with different levels
- **Error Tracking**: Comprehensive error reporting
- **Performance Monitoring**: Request timing and database query monitoring
- **User Activity**: Audit trail for important actions

## Future Enhancements

1. **Real-time Integration**: IoT sensor connectivity and live data streaming
2. **Machine Learning**: Predictive analytics for consumption forecasting
3. **Mobile App**: Native mobile application for facility managers
4. **Advanced Reporting**: Automated report generation and scheduling
5. **Multi-tenant**: Support for multiple companies on single platform
6. **Integration Marketplace**: Pre-built connectors for popular energy systems

## Support & Documentation

For technical support or feature requests:
- Comprehensive error messages and validation feedback
- Sample data for testing and onboarding
- AI-powered recommendations through the analysis interface
- Detailed API documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is designed as an enterprise solution for Indian industrial energy optimization. Contact for licensing and deployment information.

---

**WattWise AI** - Empowering Indian industries with intelligent energy management.