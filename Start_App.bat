@echo off
title KCS Report Generator

echo ========================================================
echo        Starting KCS Report Generator...
echo ========================================================
echo.

echo Checking and installing missing dependencies (this might take a few seconds on the first run)...
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Failed to install packages using 'python'. Trying 'py' instead...
    py -m pip install -r requirements.txt --quiet
)

echo.
echo Launching the web application...
python app.py
if %errorlevel% neq 0 (
    py app.py
)

pause
