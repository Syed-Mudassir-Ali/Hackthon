@echo off
REM Frontend Startup Script for Windows
REM This script will open the frontend in your default browser

echo.
echo ========================================
echo  Safety Equipment Detection Frontend
echo ========================================
echo.

REM Check if the index.html exists
if not exist "index.html" (
    echo ERROR: index.html not found in current directory
    echo Please run this script from the frontend directory
    pause
    exit /b 1
)

REM Get the full path of index.html
set "filepath=%cd%\index.html"

REM Convert to URL format (file:/// for Windows)
set "url=file:///%filepath:\=/%"

echo Opening frontend in browser...
echo URL: %url%
echo.
echo Make sure the backend server is running (python app.py in Backend folder)
echo.

REM Open in default browser
start "" "%filepath%"

echo Frontend opened successfully!
pause
