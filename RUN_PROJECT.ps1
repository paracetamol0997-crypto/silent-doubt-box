# Silent Classroom Doubt Box - PowerShell Launcher
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "                 SILENT CLASSROOM DOUBT BOX - COLLEGE PORTAL                  " -ForegroundColor Cyan
Write-Host "           ""Ask without fear. Learn without hesitation.""                     " -ForegroundColor Yellow
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Gray
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCheck) {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/ and check 'Add Python to PATH'." -ForegroundColor Yellow
    Pause
    Exit
}
python --version
Write-Host ""

# Check & Install requirements
Write-Host "[2/5] Checking dependencies..." -ForegroundColor Gray
python -c "import django" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[INFO] Installing Django from requirements.txt..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
} else {
    Write-Host "[OK] Dependencies are ready." -ForegroundColor Green
}
Write-Host ""

# Migrations
Write-Host "[3/5] Setting up database..." -ForegroundColor Gray
python manage.py migrate --noinput
Write-Host ""

# Seed Data
Write-Host "[4/5] Populating demo data..." -ForegroundColor Gray
python manage.py seed_data
Write-Host ""

# Launch
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "                          DEMO LOGIN CREDENTIALS                              " -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "  STUDENT 1:   Reg No: 23CSE101  | Name: Rahul Kumar   | Pass: rahul@123"
Write-Host "  STUDENT 2:   Reg No: 23CSE102  | Name: Priya Sharma  | Pass: priya@123"
Write-Host "  TEACHER 1:   Teacher ID: T101  | Dr. Ramesh Sharma   | Pass: teacher@123"
Write-Host "  TEACHER 2:   Teacher ID: T102  | Prof. Anjali Verma  | Pass: teacher@123"
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening web browser at http://127.0.0.1:8000/ ..." -ForegroundColor Yellow
Start-Process "http://127.0.0.1:8000/"

Write-Host "Server running. Press CTRL+C to stop." -ForegroundColor White
python manage.py runserver 127.0.0.1:8000
