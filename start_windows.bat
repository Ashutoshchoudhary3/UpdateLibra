@echo off
echo ========================================
echo AI Research Assistant for Writers
echo Startup Launcher for Windows
echo ========================================
echo.

:: Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)

:: Set working directory
cd /d "%~dp0"
echo Working directory: %CD%

:: Create logs directory if it doesn't exist
if not exist "logs" mkdir logs
echo Created logs directory

:: Kill any existing processes on our ports
echo.
echo Cleaning up existing processes...
netstat -ano | findstr ":8000" | findstr "LISTENING" >nul && (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
        taskkill /F /PID %%a >nul 2>nul
        echo Killed process on port 8000 (PID: %%a)
    )
)

netstat -ano | findstr ":3000" | findstr "LISTENING" >nul && (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000" ^| findstr "LISTENING"') do (
        taskkill /F /PID %%a >nul 2>nul
        echo Killed process on port 3000 (PID: %%a)
    )
)

netstat -ano | findstr ":48404" | findstr "LISTENING" >nul && (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":48404" ^| findstr "LISTENING"') do (
        taskkill /F /PID %%a >nul 2>nul
        echo Killed process on port 48404 (PID: %%a)
    )
)

:: Install dependencies if needed
echo.
echo Installing dependencies...
echo Installing Python dependencies...
cd ai_engine
python -m pip install -r requirements.txt > ..\logs\pip_install.log 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Some Python dependencies may have failed. Check logs\pip_install.log
)
cd ..

echo Installing Node.js dependencies...
cd scraper_service
call npm install > ..\logs\npm_install.log 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Some Node.js dependencies may have failed. Check logs\npm_install.log
)
cd ..

:: Start services
echo.
echo ========================================
echo Starting AI Research Assistant Services
echo ========================================
echo.

:: Start Scraper Service
echo Starting Scraper Service on port 3000...
start "Scraper Service" cmd /k "cd scraper_service && node server.js > ..\logs\scraper.log 2>&1 && echo Scraper Service started. Press any key to close... && pause >nul"
timeout /t 3 /nobreak >nul

:: Start AI Engine
echo Starting AI Engine on port 8000...
start "AI Engine" cmd /k "cd ai_engine && python main_mock.py > ..\logs\ai_engine.log 2>&1 && echo AI Engine started. Press any key to close... && pause >nul"
timeout /t 3 /nobreak >nul

:: Start Frontend
echo Starting Frontend on port 48404...
start "Frontend Server" cmd /k "python -m http.server 48404 --directory frontend_app > logs\frontend.log 2>&1 && echo Frontend started. Press any key to close... && pause >nul"
timeout /t 3 /nobreak >nul

:: Create status check script
echo Creating status check utility...
(
echo @echo off
echo echo ========================================
echo echo AI Research Assistant - Service Status
echo echo ========================================
echo echo.
echo echo Checking services on expected ports:
echo echo.
echo echo Port 3000 ^(Scraper Service^):
echo netstat -ano ^| findstr ":3000" ^| findstr "LISTENING" ^>nul ^&^& echo   ✅ Scraper Service is running ^|^| echo   ❌ Scraper Service is not running
echo echo.
echo echo Port 8000 ^(AI Engine^):
echo netstat -ano ^| findstr ":8000" ^| findstr "LISTENING" ^>nul ^&^& echo   ✅ AI Engine is running ^|^| echo   ❌ AI Engine is not running
echo echo.
echo echo Port 48404 ^(Frontend^):
echo netstat -ano ^| findstr ":48404" ^| findstr "LISTENING" ^>nul ^&^& echo   ✅ Frontend is running ^|^| echo   ❌ Frontend is not running
echo echo.
echo echo ========================================
echo echo Access your application at:
echo echo http://localhost:48404
echo echo ========================================
echo echo.
echo echo API Documentation at:
echo echo http://localhost:8000/docs
echo echo ========================================
echo pause
) > status_check.bat

echo.
echo ========================================
echo Startup Complete!
echo ========================================
echo.
echo Services starting in background windows...
echo.
echo To check status: run status_check.bat
echo To access application: http://localhost:48404
echo API Documentation: http://localhost:8000/docs
echo.
echo Log files available in: logs\
echo.
echo Press any key to open the application in your browser...
pause >nul

:: Open browser
start http://localhost:48404

echo.
echo Startup launcher finished. You can close this window.
pause
