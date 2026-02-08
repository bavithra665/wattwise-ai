@echo off
echo Setting up WattWise AI - Enterprise Energy Optimization System
echo.

echo Installing Backend Dependencies...
cd backend
pip install -r requirements.txt
echo Backend setup complete!
echo.

echo Installing Frontend Dependencies...
cd ..\frontend
npm install
echo Frontend setup complete!
echo.

echo Setup Instructions:
echo 1. Replace YOUR_GEMINI_API_KEY_HERE in backend/app.py with your actual Gemini API key
echo 2. Start backend: cd backend && python app.py
echo 3. Start frontend: cd frontend && npm start
echo 4. Open http://localhost:3000 in your browser
echo.

echo Sample CSV file available at: backend/sample_energy_data.csv
echo.

pause