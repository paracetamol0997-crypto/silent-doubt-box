@echo off
title Silent Classroom Doubt Box - College Portal
color 0B

:: Ensure we are in the folder where this batch script lives
cd /d "%~dp0"

echo ==============================================================================
echo                 SILENT CLASSROOM DOUBT BOX - COLLEGE PORTAL
echo           "Ask without fear. Learn without hesitation."
echo ==============================================================================
echo.

:: 1. Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python is not installed or not added to your system PATH!
    echo.
    echo Please download and install Python from: https://www.python.org/downloads/
    echo IMPORTANT: Make sure to check the box: "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo [OK] Found %%i
echo.

:: 2. Check and Install Requirements
echo [2/5] Checking and installing dependencies (Django)...
python -c "import django" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Django is not detected. Installing dependencies from requirements.txt...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        color 0C
        echo [ERROR] Failed to install dependencies via pip.
        pause
        exit /b 1
    )
) else (
    echo [OK] Django is already installed.
)
echo.

:: 3. Apply Database Migrations
echo [3/5] Setting up database tables...
python manage.py migrate --noinput
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Failed to run database migrations.
    pause
    exit /b 1
)
echo [OK] Database schema is ready.
echo.

:: 4. Seed Demo Data (Students, Teachers, Subjects, Sample Doubts)
echo [4/5] Populating demo accounts and college subjects...
python manage.py seed_data
echo.

:: 5. Launch Browser & Start Server
echo [5/5] Launching Silent Classroom Doubt Box...
echo.
echo ==============================================================================
echo                          DEMO LOGIN CREDENTIALS
echo ==============================================================================
echo   STUDENT 1:   Reg No: 23CSE101  ^| Name: Rahul Kumar   ^| Pass: rahul@123
echo   STUDENT 2:   Reg No: 23CSE102  ^| Name: Priya Sharma  ^| Pass: priya@123
echo   TEACHER 1:   Teacher ID: T101  ^| Dr. Ramesh Sharma   ^| Pass: teacher@123
echo   TEACHER 2:   Teacher ID: T102  ^| Prof. Anjali Verma  ^| Pass: teacher@123
echo ==============================================================================
echo.
echo Opening portal in your web browser...
echo Server running at: http://127.0.0.1:8000/
echo (Press CTRL+C in this terminal window to stop the server)
echo.

:: Open default browser after a short delay
start "" http://127.0.0.1:8000/

:: Start Django development server
python manage.py runserver 127.0.0.1:8000

pause
