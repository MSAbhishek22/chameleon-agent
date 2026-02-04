@echo off
echo ========================================
echo Chameleon Agent - Quick Setup
echo ========================================
echo.

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Downloading spaCy model...
python -m spacy download en_core_web_sm

echo [5/5] Setup complete!
echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo 1. Edit .env file and add your API keys:
echo    - GOOGLE_API_KEY (get from https://makersuite.google.com/app/apikey)
echo    - GROQ_API_KEY (optional, get from https://console.groq.com)
echo.
echo 2. Run the server:
echo    uvicorn main:app --reload
echo.
echo 3. Test the API:
echo    Open http://localhost:8000/docs
echo ========================================
pause
