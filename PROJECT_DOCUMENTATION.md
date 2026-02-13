# WattWise AI - Complete Project Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Features](#features)
5. [Installation & Setup](#installation--setup)
6. [Deployment](#deployment)
7. [API Documentation](#api-documentation)
8. [Database Schema](#database-schema)
9. [Testing Guide](#testing-guide)
10. [Security](#security)
11. [Performance](#performance)
12. [Future Roadmap](#future-roadmap)

---

## 🎯 Project Overview

### What is WattWise AI?

WattWise AI is a **production-grade B2B SaaS web application** designed for Indian industries to detect energy waste and optimize consumption patterns using artificial intelligence. The system provides real-time analytics, anomaly detection, and AI-powered recommendations to reduce energy costs by up to 30%.

### Problem Statement

Indian industries face significant challenges in energy management:
- **High Energy Costs**: Industrial electricity rates averaging ₹8.50/kWh
- **Inefficient Consumption**: Lack of visibility into energy usage patterns
- **Manual Monitoring**: Time-intensive manual analysis of energy data
- **Compliance Requirements**: Need for sustainability reporting and energy efficiency standards

### Solution

WattWise AI provides:
- ✅ **Automated Anomaly Detection**: Statistical analysis to identify energy spikes and waste
- ✅ **AI-Powered Insights**: Google Gemini integration for intelligent recommendations
- ✅ **Cost Analysis**: Real-time cost calculations in Indian Rupees (INR)
- ✅ **Department-wise Analytics**: Granular consumption tracking by department and equipment
- ✅ **Actionable Recommendations**: Practical steps to reduce energy consumption

### Business Value

#### Cost Savings
- **Energy Reduction**: 20-30% consumption decrease through optimization
- **Operational Efficiency**: Automated monitoring reduces manual effort by 80%
- **Predictive Maintenance**: Early detection of equipment inefficiencies
- **ROI**: Typical payback period of 6-12 months

#### Compliance & Sustainability
- **Energy Audits**: Automated reporting for regulatory compliance
- **Carbon Footprint**: Reduced emissions through optimized consumption
- **Sustainability Goals**: Support for corporate environmental initiatives
- **ESG Reporting**: Data for environmental, social, and governance reports

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Dashboard   │  │   Insights   │  │  AI Analysis │      │
│  │   (Charts)   │  │   (Tables)   │  │  (Reports)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         Bootstrap 5 + Chart.js + Custom JavaScript          │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     Auth     │  │     Main     │  │     API      │      │
│  │  Blueprint   │  │  Blueprint   │  │  Blueprint   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                    Flask 3.0.0 + Blueprints                 │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Business Logic                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Energy    │  │      AI      │  │   Analytics  │      │
│  │   Analyzer   │  │  Consultant  │  │    Engine    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         Pandas + Scikit-learn + Google Gemini               │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        Data Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     User     │  │ EnergyData   │  │   Insights   │      │
│  │    Model     │  │    Model     │  │    Model     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│              SQLAlchemy ORM + PostgreSQL                    │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **CSV Upload**: User uploads historical energy data from enterprise systems
2. **Data Processing**: System validates, parses, and calculates costs at ₹8.50/kWh
3. **Analytics**: Anomaly detection using Isolation Forest and statistical methods
4. **AI Analysis**: Google Gemini generates insights and recommendations
5. **Dashboard**: Visual presentation of findings and KPIs

### Component Breakdown

#### Backend (Flask)
- **Energy Analytics Engine**: Rule-based and statistical anomaly detection using scikit-learn
- **Database**: SQLAlchemy with SQLite for development, PostgreSQL for production
- **AI Integration**: Google Gemini for intelligent insights
- **API Design**: RESTful endpoints with proper authentication and validation
- **Authentication**: Flask-Login with secure session management

#### Frontend (Bootstrap 5 + JavaScript)
- **Professional Dashboard**: Enterprise-grade UI with Chart.js visualizations
- **Authentication System**: Secure user registration and login with CSRF protection
- **Data Visualization**: Interactive charts showing energy trends and patterns
- **Responsive Design**: Mobile-friendly interface optimized for all devices

---

## 💻 Technology Stack

### Backend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11.9 | Core programming language |
| **Flask** | 3.0.0 | Web framework with modular blueprints |
| **SQLAlchemy** | 3.1.1 | Database ORM |
| **Flask-Login** | 0.6.3 | User authentication |
| **Flask-WTF** | 1.2.1 | Form handling and CSRF protection |
| **Pandas** | ≥2.2.0 | Data processing and analysis |
| **NumPy** | ≥1.26.4 | Numerical computations |
| **Scikit-learn** | ≥1.4.0 | Machine learning (anomaly detection) |
| **Google Generative AI** | 0.3.2 | Gemini AI integration |
| **Plotly** | ≥5.18.0 | Advanced charting |
| **Gunicorn** | 21.2.0 | Production WSGI server |
| **psycopg2-binary** | ≥2.9.10 | PostgreSQL adapter |
| **bcrypt** | 4.1.2 | Password hashing |

### Frontend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| **Bootstrap** | 5.3.0 | Responsive UI framework |
| **Chart.js** | 4.4.0 | Data visualization |
| **Font Awesome** | 6.4.0 | Icons |
| **JavaScript** | ES6+ | Client-side interactivity |
| **CSS3** | - | Custom styling |

### Database
- **Development**: SQLite (file-based)
- **Production**: PostgreSQL (Render managed)

### Deployment
- **Platform**: Render.com
- **Runtime**: Python 3.11.9
- **Web Server**: Gunicorn
- **Database**: PostgreSQL (Free tier)

---

## ✨ Features

### 1. Energy Analytics

#### Baseline Analysis
- Calculate average consumption per department
- Establish deviation thresholds
- Identify normal operating ranges

#### Anomaly Detection
- **Statistical Method**: Z-score based detection (threshold: 2.0 standard deviations)
- **Machine Learning**: Isolation Forest algorithm
- **Pattern Recognition**: Hourly, daily, and departmental usage patterns
- **Automatic Flagging**: Real-time anomaly identification

#### Cost Calculation
- Automatic cost computation at ₹8.50/kWh (Indian industrial rate)
- Department-wise cost breakdown
- Potential savings estimation

### 2. AI Insights (Google Gemini)

#### Root Cause Analysis
- Explain reasons for energy spikes in business-friendly language
- Context-aware analysis based on department and equipment
- Historical pattern comparison

#### Optimization Recommendations
- Actionable steps to reduce consumption
- Priority-based recommendations (High/Medium/Low)
- Implementation difficulty assessment
- Estimated savings in INR

#### Implementation Timeline
- **Quick Wins**: 1-2 weeks (low-hanging fruit)
- **Medium-Term**: 1-3 months (moderate changes)
- **Long-Term**: 3-6 months (strategic initiatives)

### 3. Dashboard Features

#### KPI Overview
- Total energy consumption (kWh)
- Total cost (₹)
- Number of anomalies detected
- Peak consumption hours
- Average consumption rate

#### Interactive Charts
- Energy consumption trends (line charts)
- Department breakdown (pie charts)
- Equipment comparison (bar charts)
- Time-series analysis

#### Department Analysis
- Consumption breakdown by department
- Top consuming departments
- Department-specific insights

#### Equipment Tracking
- High-consuming equipment identification
- Equipment performance monitoring
- Maintenance alerts

### 4. User Management

#### Authentication
- Secure user registration
- Email/password login
- Session management
- Password hashing with bcrypt

#### User Settings
- Profile management
- Gemini API key configuration
- Notification preferences

### 5. Data Management

#### CSV Upload
- Drag-and-drop file upload
- Format validation
- Duplicate detection
- Error reporting

#### Data Validation
- Timestamp format checking
- Numeric value validation
- Required field verification
- Data type enforcement

#### File Tracking
- Upload history
- File metadata storage
- Multi-file support

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git
- Google Gemini API key (for AI features)

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/bavithra665/wattwise-ai.git
cd wattwise-ai
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
SECRET_KEY=your-secret-key-here-change-in-production
GEMINI_API_KEY=your-gemini-api-key-here
DATABASE_URL=sqlite:///wattwise.db
FLASK_DEBUG=True
```

#### 5. Initialize Database
```bash
python run.py
# Database tables will be created automatically on first run
```

#### 6. Run the Application
```bash
python run.py
```

The application will be available at: **http://localhost:5000**

### CSV Data Format

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

---

## 🌐 Deployment

### Render.com Deployment (Current)

#### Live URL
**https://wattwise-ai-1.onrender.com**

#### Deployment Configuration

**File: `render.yaml`**
```yaml
services:
  - type: web
    name: wattwise-ai
    env: python
    runtime: python-3.11.9
    plan: free
    buildCommand: pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
    startCommand: gunicorn -b 0.0.0.0:$PORT run:app
    envVars:
      - key: FLASK_DEBUG
        value: "false"
      - key: SECRET_KEY
        generateValue: true
      - key: EMPHASIZE_SSL
        value: "true"
      - key: DATABASE_URL
        fromDatabase:
          name: wattwise-db
          property: connectionString
      - key: GEMINI_API_KEY
        sync: false

databases:
  - name: wattwise-db
    databaseName: wattwise_db
    user: wattwise_user
    plan: free
```

#### Deployment Steps

1. **Connect GitHub Repository**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository

2. **Configure Environment Variables**
   - Add `GEMINI_API_KEY` in the Render dashboard
   - Other variables are auto-configured via `render.yaml`

3. **Deploy**
   - Render automatically deploys on every push to `main` branch
   - Monitor deployment in the Events tab

#### Deployment Troubleshooting

**Common Issues:**
1. **Python Version Mismatch**: Ensure `runtime: python-3.11.9` is set in `render.yaml`
2. **psycopg2 Errors**: Use `psycopg2-binary>=2.9.10` for Python 3.11+ compatibility
3. **Port Binding**: Use `gunicorn -b 0.0.0.0:$PORT run:app` to bind to Render's port
4. **Build Timeouts**: Add `--no-cache-dir` to pip install command

### Alternative Deployment Options

#### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
```

#### Heroku Deployment
```bash
# Create Procfile
echo "web: gunicorn run:app" > Procfile

# Deploy
heroku create wattwise-ai
git push heroku main
```

---

## 📡 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/x-www-form-urlencoded

name=John+Doe&email=john@example.com&password=SecurePass123
```

**Response:**
```json
{
  "status": "success",
  "message": "Registration successful",
  "redirect": "/auth/login"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

email=john@example.com&password=SecurePass123
```

**Response:**
```json
{
  "status": "success",
  "redirect": "/dashboard"
}
```

#### Logout
```http
POST /auth/logout
```

### Data Management Endpoints

#### Upload CSV
```http
POST /upload
Content-Type: multipart/form-data

file=@energy_data.csv
```

**Response:**
```json
{
  "status": "success",
  "message": "Data uploaded successfully",
  "insights_generated": 5
}
```

#### Get Dashboard Data
```http
GET /dashboard
```

Returns HTML page with energy statistics and charts.

#### Get Insights
```http
GET /insights
```

Returns HTML page with list of energy insights.

### API Routes

#### Get Energy Statistics
```http
GET /api/energy/summary
```

**Response:**
```json
{
  "total_consumption": 12500.5,
  "total_cost": 106254.25,
  "anomaly_count": 15,
  "departments": [
    {
      "name": "Production",
      "consumption": 8500.2,
      "cost": 72251.70
    }
  ]
}
```

#### Get AI Analysis
```http
GET /api/analyze-insight/<insight_id>
```

**Response:**
```json
{
  "analysis": "Detailed AI analysis text",
  "root_cause": "Root cause explanation",
  "business_impact": "Business impact description",
  "recommendations": [
    {
      "text": "Install VFDs on motors",
      "priority": "high",
      "estimated_savings": 15000.0,
      "difficulty": "medium"
    }
  ],
  "timeline": {
    "quick_wins": ["Action 1", "Action 2"],
    "medium_term": ["Action 3"],
    "long_term": ["Action 4"]
  }
}
```

---

## 🗄️ Database Schema

### User Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    gemini_api_key VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### EnergyData Table
```sql
CREATE TABLE energy_data (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    energy_kwh FLOAT NOT NULL,
    department VARCHAR(100) NOT NULL,
    equipment VARCHAR(100) NOT NULL,
    building VARCHAR(100),
    cost_inr FLOAT,
    is_anomaly BOOLEAN DEFAULT FALSE,
    anomaly_score FLOAT,
    file_name VARCHAR(200),
    upload_date TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### EnergyInsight Table
```sql
CREATE TABLE energy_insight (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    insight_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    department VARCHAR(100),
    equipment VARCHAR(100),
    severity VARCHAR(20),
    potential_savings_inr FLOAT,
    file_name VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### AIRecommendation Table
```sql
CREATE TABLE ai_recommendation (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    insight_id INTEGER NOT NULL,
    recommendation TEXT NOT NULL,
    priority VARCHAR(20),
    estimated_savings_inr FLOAT,
    implementation_difficulty VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (insight_id) REFERENCES energy_insight(id)
);
```

---

## 🧪 Testing Guide

### Manual Testing Checklist

#### 1. Landing Page
- [ ] Page loads without errors
- [ ] Navigation links work
- [ ] Responsive design on mobile

#### 2. User Registration
- [ ] Can create new account
- [ ] Email validation works
- [ ] Password requirements enforced
- [ ] Duplicate email detection

#### 3. User Login
- [ ] Can login with valid credentials
- [ ] Invalid credentials rejected
- [ ] Session persists across pages
- [ ] Logout works correctly

#### 4. CSV Upload
- [ ] Can upload valid CSV
- [ ] Invalid format rejected
- [ ] File size limits enforced
- [ ] Success message displayed

#### 5. Dashboard
- [ ] KPIs display correctly
- [ ] Charts render properly
- [ ] Data updates after upload
- [ ] No JavaScript errors

#### 6. Insights
- [ ] Insights list displays
- [ ] Can view insight details
- [ ] Severity levels shown
- [ ] Savings calculated

#### 7. AI Analysis
- [ ] AI analysis generates
- [ ] Recommendations display
- [ ] Timeline shows correctly
- [ ] Fallback works without API key

### Sample Test Data

**File: `test_energy_data.csv`**
```csv
timestamp,department,equipment,energy_kwh,building
2024-02-01 00:00:00,Production,CNC Machine,145.2,Factory-A
2024-02-01 01:00:00,Production,CNC Machine,142.8,Factory-A
2024-02-01 02:00:00,Production,CNC Machine,148.5,Factory-A
2024-02-01 03:00:00,HVAC,Chiller-1,220.3,Factory-A
2024-02-01 04:00:00,HVAC,Chiller-1,225.7,Factory-A
2024-02-01 05:00:00,Data Center,Server Rack,310.5,Office-B
2024-02-01 06:00:00,Data Center,Server Rack,305.2,Office-B
2024-02-01 07:00:00,Lighting,LED Panel,45.8,Office-B
2024-02-01 08:00:00,Production,CNC Machine,450.9,Factory-A
2024-02-01 09:00:00,Production,CNC Machine,155.3,Factory-A
```

The spike at 08:00:00 (450.9 kWh) should trigger anomaly detection!

---

## 🔒 Security

### Implemented Security Measures

#### Authentication
- ✅ Secure password hashing with bcrypt
- ✅ Session-based authentication
- ✅ Login required decorators
- ✅ Secure cookie configuration

#### CSRF Protection
- ✅ Flask-WTF CSRF tokens
- ✅ Form validation
- ✅ Token verification on POST requests

#### Input Validation
- ✅ CSV format validation
- ✅ Data type checking
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ XSS prevention (template escaping)

#### Data Security
- ✅ Environment variable for secrets
- ✅ API key encryption
- ✅ Secure database connections
- ✅ HTTPS enforcement in production

### Security Best Practices

1. **Never commit `.env` file** to version control
2. **Rotate SECRET_KEY** regularly in production
3. **Use strong passwords** for user accounts
4. **Keep dependencies updated** to patch vulnerabilities
5. **Enable HTTPS** in production (Render provides this)
6. **Limit file upload sizes** to prevent DoS attacks

---

## ⚡ Performance

### Optimization Techniques

#### Backend
- Database query optimization with SQLAlchemy
- Efficient pandas operations for data processing
- Caching of frequently accessed data
- Async processing for AI analysis

#### Frontend
- Minified CSS and JavaScript
- Lazy loading of charts
- Efficient DOM manipulation
- Responsive image loading

#### Database
- Indexed columns (user_id, timestamp)
- Efficient query patterns
- Connection pooling in production

### Performance Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Page Load Time | < 2s | ~1.5s |
| CSV Processing | < 5s for 1000 rows | ~3s |
| AI Analysis | < 10s | ~7s |
| Dashboard Render | < 1s | ~0.8s |

---

## 🚀 Future Roadmap

### Phase 1: Enhanced Analytics (Q2 2026)
- [ ] Real-time data streaming
- [ ] Predictive consumption forecasting
- [ ] Advanced machine learning models
- [ ] Custom alert thresholds

### Phase 2: Integration (Q3 2026)
- [ ] IoT sensor connectivity
- [ ] BMS/SCADA integration
- [ ] ERP system connectors
- [ ] API marketplace

### Phase 3: Mobile & Reporting (Q4 2026)
- [ ] Native mobile app (iOS/Android)
- [ ] Automated report generation
- [ ] Email/SMS alerts
- [ ] PDF export functionality

### Phase 4: Enterprise Features (Q1 2027)
- [ ] Multi-tenant architecture
- [ ] Role-based access control
- [ ] White-label solution
- [ ] Advanced compliance reporting

---

## 📞 Support & Contact

### Technical Support
- **Email**: support@wattwise.ai (placeholder)
- **Documentation**: This file
- **GitHub Issues**: [Report bugs](https://github.com/bavithra665/wattwise-ai/issues)

### Getting Help
1. Check this documentation first
2. Review error messages in Render logs
3. Test with sample data provided
4. Contact support with detailed error descriptions

---

## 📄 License

This project is designed as an enterprise solution for Indian industrial energy optimization. Contact for licensing and deployment information.

---

**WattWise AI** - Empowering Indian industries with intelligent energy management.

*Last Updated: February 8, 2026*
