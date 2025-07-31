@echo off
title Brute Force Tool - Difai Team
color 0a

echo.
echo ========================================
echo    BRUTE FORCE TOOL - DIFAI TEAM
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Brute Force Tool...
echo.

python brute_force_tool.py

pause