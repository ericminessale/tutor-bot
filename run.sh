#!/bin/bash

echo "SignalWire AI Tutor Bot Demo Launcher"
echo "====================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run: python setup.py"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the tutor bot
echo "Starting Tutor Bot service..."
python tutor_bot_demo.py

# Note: deactivate is handled by the subshell exit 