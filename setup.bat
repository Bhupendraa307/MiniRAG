@echo off
echo Setting up Mini RAG Full-Stack Application...
echo.

echo 1. Setting up Backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
echo Backend setup complete!
echo.

echo 2. Setting up Frontend...
cd ..\frontend
npm install
echo Frontend setup complete!
echo.

echo 3. Setup Instructions:
echo - Copy backend\.env.example to backend\.env and add your API keys
echo - Copy frontend\.env.example to frontend\.env (optional)
echo - Run 'cd backend && venv\Scripts\activate && uvicorn app.main:app --reload' for backend
echo - Run 'cd frontend && npm start' for frontend
echo.
echo Setup complete! Check README.md for detailed instructions.
pause