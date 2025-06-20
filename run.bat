@echo off
echo SignalWire AI Tutor Bot Demo Launcher
echo =====================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Please run: python setup.py
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

REM Run the tutor bot
echo Starting Tutor Bot service...
python tutor_bot_demo.py

REM Deactivate on exit
deactivate 