@echo off
REM run_flask.bat - Start Flask application with Gunicorn on Windows

if not exist logs mkdir logs

echo Starting Flask application with Gunicorn...
echo.
echo === Process Information ===
echo User: %USERNAME%
echo Current Directory: %cd%
echo.
echo === Gunicorn Configuration ===
echo Binding: 127.0.0.1:8000
echo.

REM Start Gunicorn with the Flask application
python -m gunicorn -c wsgi_config.py app:app

pause
