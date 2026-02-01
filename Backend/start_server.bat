@echo off
REM Backend Startup Script for Windows
REM This script will start the FastAPI server

echo.
echo ========================================
echo  Safety Equipment Detection Backend
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
pip list | findstr fastapi >nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if model exists
if not exist "models\best.pt" (
    echo.
    echo WARNING: Model file not found at models\best.pt
    echo Please download your trained model from Google Colab and place it here:
    echo   - Create folder: Backend\models\
    echo   - Download best.pt from Colab
    echo   - Place best.pt in Backend\models\
    echo.
    echo For now, starting backend anyway (will fail when making predictions)
    echo.
)

REM Start the server
echo.
echo Starting FastAPI server on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
