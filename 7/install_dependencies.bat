@echo off
REM install_dependencies.bat - Install Python packages on Windows

echo Installing Python dependencies from requirements.txt...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies
    exit /b 1
) else (
    echo.
    echo Installed packages:
    python -m pip list | findstr "Flask gunicorn Werkzeug"
    echo.
    echo Dependencies installed successfully!
)
