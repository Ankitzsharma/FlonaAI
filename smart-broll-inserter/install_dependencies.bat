@echo off
echo ============================================
echo Smart B-Roll Inserter - One-Click Start
echo ============================================

echo.
echo [1/2] Installing Backend Dependencies...
pip install -r backend/requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install backend dependencies.
    pause
    exit /b
)

echo.
echo [2/2] Installing Frontend Dependencies...
cd frontend
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install frontend dependencies.
    pause
    exit /b
)
cd ..

echo.
echo All dependencies installed!
echo.
echo Please run 'run_backend.bat' in one terminal
echo and 'run_frontend.bat' in another terminal.
echo.
pause
