#!/bin/bash
# Databricks Mosaic AI Demo - TUI Launcher

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
else
    source venv/bin/activate
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Please copy .env.sample to .env and configure your credentials:"
    echo "  cp .env.sample .env"
    echo "  # Edit .env with your DATABRICKS_HOST and DATABRICKS_TOKEN"
    exit 1
fi

# Run the CLI
python3 cli.py

# Deactivate virtual environment
deactivate
