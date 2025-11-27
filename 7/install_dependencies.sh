#!/bin/bash
# install_dependencies.sh - Install required Python packages

echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

echo ""
echo "Installed packages:"
pip list | grep -E "Flask|gunicorn|Werkzeug"
