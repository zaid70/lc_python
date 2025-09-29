@echo off
echo Starting Ladies Collections Flask Application...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install requirements
echo Installing/updating requirements...
pip install -r requirements.txt
echo.

REM Start the Flask application
echo Starting Flask development server...
echo.
echo ==========================================
echo Ladies Collections Flask Application
echo ==========================================
echo.
echo Server will start at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
pause