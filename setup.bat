@echo off
REM ============================================================
REM  Smart File Organizer — Windows Setup
REM  Run this once to install everything.
REM  Double-click OR run from PowerShell / Command Prompt.
REM ============================================================

echo.
echo =============================================
echo   Smart File Organizer — Setup
echo =============================================
echo.

REM ---- Check Python ----
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found.
    echo         Download it from https://www.python.org/downloads/
    echo         Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)
echo [OK] Python found:
python --version
echo.

REM ---- Create virtual environment ----
if exist venv (
    echo [INFO] Virtual environment already exists, skipping creation.
) else (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
)
echo.

REM ---- Activate venv and install packages ----
echo [INFO] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip --quiet
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Dependency installation failed.
    pause
    exit /b 1
)
echo [OK] Dependencies installed.
echo.

REM ---- Create required directories ----
if not exist logs        mkdir logs
if not exist reports     mkdir reports
if not exist organized_files mkdir organized_files
echo [OK] Folders created: logs, reports, organized_files
echo.

echo =============================================
echo   Setup Complete!
echo =============================================
echo.
echo   HOW TO RUN:
echo.
echo   Option A — Double-click "run.bat" (easiest)
echo.
echo   Option B — PowerShell / Command Prompt:
echo     1. venv\Scripts\activate
echo     2. python organizer.py
echo.
echo   Option C — Run immediately (no menu):
echo     python organizer.py --now
echo.
echo   Option D — Custom source folder:
echo     python organizer.py --now --source "C:\Users\You\Desktop"
echo.
pause
