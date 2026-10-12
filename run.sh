#!/usr/bin/env bash

# Silent Classroom Doubt Box - Linux/macOS Launcher
cd "$(dirname "$0")"

echo "=============================================================================="
echo "                 SILENT CLASSROOM DOUBT BOX - COLLEGE PORTAL"
echo "           \"Ask without fear. Learn without hesitation.\""
echo "=============================================================================="
echo ""

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 is not installed or not in your PATH."
    echo "Please install Python 3 (e.g., brew install python or sudo apt install python3 python3-pip)"
    exit 1
fi

echo "[OK] Found $(python3 --version)"
echo ""

# 2. Check/Install dependencies
echo "[2/5] Checking and installing dependencies..."
python3 -c "import django" &> /dev/null
if [ $? -ne 0 ]; then
    echo "[INFO] Installing dependencies via pip..."
    python3 -m pip install -r requirements.txt
fi
echo "[OK] Dependencies ready."
echo ""

# 3. Migrations
echo "[3/5] Setting up database tables..."
python3 manage.py migrate --noinput
echo ""

# 4. Seed Data
echo "[4/5] Populating demo data..."
python3 manage.py seed_data
echo ""

# 5. Launch
echo "=============================================================================="
echo "                          DEMO LOGIN CREDENTIALS"
echo "=============================================================================="
echo "  STUDENT 1:   Reg No: 23CSE101  | Name: Rahul Kumar   | Pass: rahul@123"
echo "  STUDENT 2:   Reg No: 23CSE102  | Name: Priya Sharma  | Pass: priya@123"
echo "  TEACHER 1:   Teacher ID: T101  | Dr. Ramesh Sharma   | Pass: teacher@123"
echo "  TEACHER 2:   Teacher ID: T102  | Prof. Anjali Verma  | Pass: teacher@123"
echo "=============================================================================="
echo ""
echo "Server running at: http://127.0.0.1:8000/"
echo "Opening browser..."

# Open browser based on OS
if which xdg-open > /dev/null; then
    xdg-open http://127.0.0.1:8000/ &
elif which open > /dev/null; then
    open http://127.0.0.1:8000/ &
fi

python3 manage.py runserver 127.0.0.1:8000
