@echo off
title Modern Penetration Testing Toolkit
color 0a

echo ========================================
echo Modern Penetration Testing Toolkit
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found. Checking dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo WARNING: Some dependencies may not be installed properly
    echo Continuing anyway...
)

echo.
echo Starting Modern Penetration Testing Toolkit...
echo.
echo IMPORTANT: This tool is for EDUCATIONAL PURPOSES ONLY
echo Only use on systems you own or have permission to test
echo.
echo Press any key to continue...
pause >nul

python penetration_toolkit.py

echo.
echo Toolkit closed.
pause