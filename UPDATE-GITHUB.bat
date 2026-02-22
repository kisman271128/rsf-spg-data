@echo off
REM ========================================
REM SUPER SIMPLE - EXCEL TO GITHUB
REM Double-click to update GitHub
REM ========================================

echo.
echo ========================================
echo  EXCEL TO GITHUB - SUPER SIMPLE
echo ========================================
echo.

REM Navigate to repository
cd /d C:\rsf-spg-app\rsf-spg-data

REM Check Python (install if needed)
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not installed!
    echo Please install from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check pandas (install if needed)
python -c "import pandas" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing dependencies...
    pip install pandas pyxlsb
)

echo [1/3] Converting Excel to JSON...
python excel_to_json_simple.py

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Conversion failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Adding to Git...
git add data/*.json

echo.
echo [3/3] Pushing to GitHub...
git commit -m "Auto-update from DSourceSPGApp.xlsb - %date% %time:~0,5%"
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  ✅ SUCCESS! Data uploaded to GitHub
    echo ========================================
    echo.
) else (
    echo.
    echo ❌ Push failed! Check internet connection
    echo.
)

timeout /t 3
