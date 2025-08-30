@echo off
echo Starting Mini RAG Application...
echo.
echo Starting Backend...
start "Backend" cmd /k "cd backend && start.bat"
timeout /t 3 /nobreak >nul
echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && start.bat"
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs