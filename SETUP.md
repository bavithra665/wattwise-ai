# WattWise AI - Setup & Launch Instructions

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Git (optional)

### 1. Get Your Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 2. Configure Backend
1. Open `backend/app.py`
2. Replace `YOUR_GEMINI_API_KEY_HERE` with your actual API key:
   ```python
   genai.configure(api_key="your_actual_api_key_here")
   ```

### 3. Install Dependencies

**Option A: Use Setup Script (Windows)**
```bash
setup.bat
```

**Option B: Manual Installation**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 4. Launch Application

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```
Backend will run on: http://localhost:5000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```
Frontend will run on: http://localhost:3000

### 5. Test the Application

1. **Register Account**: Create a new company account
2. **Login**: Sign in with your credentials
3. **Upload Data**: Use the provided `sample_energy_data.csv`
4. **View Analytics**: Explore energy consumption insights
5. **Ask AI**: Chat with the AI consultant about your energy usage

## 📊 Sample Data

The project includes realistic Indian industrial energy data:
- **Location**: `backend/sample_energy_data.csv`
- **Format**: Manufacturing, Office, Warehouse departments
- **Equipment**: CNC machines, HVAC, furnaces, etc.
- **Time Range**: 24-hour consumption patterns

## 🔧 Configuration

### Database
- **Type**: SQLite (automatically created)
- **Location**: `backend/wattwise.db`
- **Tables**: users, energy_data

### API Endpoints
- `POST /api/register` - User registration
- `POST /api/login` - User authentication
- `POST /api/upload-energy-data` - CSV data upload
- `GET /api/dashboard-data` - Analytics data
- `POST /api/ask-ai` - AI chat interface

### Energy Cost Calculation
- **Rate**: ₹6.5 per kWh (Indian industrial average)
- **Currency**: Indian Rupees (INR)
- **Automatic**: Cost calculated on data upload

## 🎯 Key Features Implemented

### ✅ Authentication System
- User registration with company name
- Secure password hashing
- Session management
- Protected routes

### ✅ Energy Analytics Engine
- Statistical anomaly detection
- Department-wise consumption analysis
- Equipment performance tracking
- Hourly pattern recognition
- Cost analysis in INR

### ✅ AI Integration (Gemini 3)
- Intelligent energy insights
- Business-friendly explanations
- Actionable recommendations
- Interactive chat interface

### ✅ Professional Dashboard
- Enterprise-grade UI design
- Real-time KPI display
- Interactive charts (Recharts)
- Responsive design
- Clean, minimal aesthetics

### ✅ Data Processing
- CSV validation and parsing
- Error handling and feedback
- Real-time upload status
- Data persistence

## 🏭 Production Deployment

### Environment Variables
```bash
# Backend
FLASK_ENV=production
SECRET_KEY=your_production_secret_key
GEMINI_API_KEY=your_gemini_api_key

# Database
DATABASE_URL=postgresql://... (for production)
```

### Docker Deployment (Optional)
```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# Frontend Dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

## 🔍 Testing Checklist

### Backend Testing
- [ ] API endpoints respond correctly
- [ ] Database tables created
- [ ] CSV upload and processing works
- [ ] Energy analytics calculations accurate
- [ ] AI integration functional (with API key)

### Frontend Testing
- [ ] Landing page loads properly
- [ ] Registration/login flow works
- [ ] Dashboard displays after login
- [ ] File upload interface functional
- [ ] Charts render correctly
- [ ] AI chat interface responsive

### Integration Testing
- [ ] Frontend-backend communication
- [ ] Authentication flow end-to-end
- [ ] Data upload and visualization
- [ ] AI insights generation
- [ ] Error handling and user feedback

## 🚨 Troubleshooting

### Common Issues

**Backend won't start:**
- Check Python version (3.8+)
- Verify all dependencies installed
- Ensure port 5000 is available

**Frontend won't start:**
- Check Node.js version (16+)
- Run `npm install` again
- Clear npm cache: `npm cache clean --force`

**AI not working:**
- Verify Gemini API key is correct
- Check internet connection
- Ensure API key has proper permissions

**Database errors:**
- Delete `wattwise.db` and restart backend
- Check file permissions in backend directory

**CSV upload fails:**
- Verify CSV format matches requirements
- Check file size (should be reasonable)
- Ensure all required columns present

## 📈 Performance Optimization

### Backend
- Use PostgreSQL for production
- Implement caching for analytics
- Add API rate limiting
- Optimize database queries

### Frontend
- Implement lazy loading
- Add data pagination
- Optimize chart rendering
- Use React.memo for components

## 🔐 Security Considerations

### Implemented
- Password hashing (Werkzeug)
- Session management
- Input validation
- CORS configuration
- SQL injection prevention

### Production Additions
- HTTPS enforcement
- API rate limiting
- File upload restrictions
- Environment variable security
- Database encryption

## 📞 Support

For technical issues:
1. Check this documentation
2. Verify API key configuration
3. Test with sample data
4. Check browser console for errors
5. Review backend logs

---

**WattWise AI** is now ready for enterprise energy optimization! 🌟