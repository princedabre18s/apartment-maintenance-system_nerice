@echo off
echo ========================================
echo Apartment Maintenance Request System
echo Starting Demo...
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo ERROR: backend folder not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERROR: frontend folder not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Start Backend Server
echo [1/3] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && echo Backend Starting... && uvicorn app.main:app --reload"

REM Wait for backend to initialize
echo [2/3] Waiting for backend to initialize...
timeout /t 8 /nobreak > nul

REM Start Frontend Server
echo [3/3] Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && echo Frontend Starting... && npm run dev"

REM Wait for frontend to initialize
echo.
echo Waiting for frontend to initialize...
timeout /t 10 /nobreak > nul

REM Open browser
echo.
echo Opening browser...
start http://localhost:5173

echo.
echo ========================================
echo ✅ Demo Started Successfully!
echo ========================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Dashboard opens automatically - No login required!
echo.
echo To stop servers: Close both terminal windows
echo ========================================
echo.
pause
