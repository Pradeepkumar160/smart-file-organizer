@echo off
REM ============================================================
REM  Smart File Organizer — Quick Launcher
REM  Double-click this after running setup.bat once.
REM ============================================================

if not exist venv (
    echo [ERROR] Virtual environment not found.
    echo         Please run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python organizer.py
pause
