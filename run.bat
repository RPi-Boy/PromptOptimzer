@echo off
REM Prompt Optimizer - Startup Script for Windows

echo Starting Prompt Optimizer...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed
    echo.
)

REM Check if .env file exists
if not exist ".env" (
    echo .env file not found!
    echo Copying .env.example to .env...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your API keys!
    echo    - OPENROUTER_API_KEY
    echo    - SECRET_KEY
    echo    - JWT_SECRET_KEY
    echo.
    pause
)

REM Start the application
echo Starting server...
echo Application will be available at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python -m app.main
