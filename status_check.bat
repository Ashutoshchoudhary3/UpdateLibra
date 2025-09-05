
@echo off
echo ========================================
echo AI Research Assistant - Service Status
echo ========================================
echo.
echo Checking services on expected ports:
echo.
echo Port 3000 (Scraper Service):
netstat -ano | findstr ":3000" | findstr "LISTENING" >nul && echo   ✅ Scraper Service is running || echo   ❌ Scraper Service is not running

echo.
echo Port 8000 (AI Engine):
netstat -ano | findstr ":8000" | findstr "LISTENING" >nul && echo   ✅ AI Engine is running || echo   ❌ AI Engine is not running

echo.
echo Port 48404 (Frontend):
netstat -ano | findstr ":48404" | findstr "LISTENING" >nul && echo   ✅ Frontend is running || echo   ❌ Frontend is not running

echo.
echo ========================================
echo Access your application at:
echo http://localhost:48404
echo ========================================
echo.
echo API Documentation at:
echo http://localhost:8000/docs
echo ========================================
echo.
echo Process details:
echo.
echo Scraper Service processes:
tasklist /FI "WINDOWTITLE eq Scraper Service" 2>nul | findstr "cmd.exe" >nul && echo   ✅ Scraper Service console is open || echo   ❌ Scraper Service console is closed

echo.
echo AI Engine processes:
tasklist /FI "WINDOWTITLE eq AI Engine" 2>nul | findstr "cmd.exe" >nul && echo   ✅ AI Engine console is open || echo   ❌ AI Engine console is closed

echo.
echo Frontend processes:
tasklist /FI "WINDOWTITLE eq Frontend Server" 2>nul | findstr "cmd.exe" >nul && echo   ✅ Frontend console is open || echo   ❌ Frontend console is closed

echo.
echo Recent log entries:
echo.
echo --- AI Engine Log (last 5 lines) ---
if exist "logs\ai_engine.log" (
    powershell -Command "Get-Content 'logs\ai_engine.log' -Tail 5 | ForEach-Object {Write-Host '   ' $_}"
) else (
    echo    No AI Engine log found
)

echo.
echo --- Scraper Log (last 5 lines) ---
if exist "logs\scraper.log" (
    powershell -Command "Get-Content 'logs\scraper.log' -Tail 5 | ForEach-Object {Write-Host '   ' $_}"
) else (
    echo    No Scraper log found
)

echo.
echo ========================================
echo.
echo Quick Actions:
echo [1] Open Application in Browser
echo [2] Open API Documentation
echo [3] View Full Logs
echo [4] Test API Endpoint
echo [5] Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" start http://localhost:48404
if "%choice%"=="2" start http://localhost:8000/docs
if "%choice%"=="3" (
    if exist "logs\ai_engine.log" (
        echo.
        echo === AI Engine Log ===
        type logs\ai_engine.log
    )
    if exist "logs\scraper.log" (
        echo.
        echo === Scraper Log ===
        type logs\scraper.log
    )
    pause
)
if "%choice%"=="4" (
    echo.
    echo Testing API endpoint...
    powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/generate-chapter' -Method Post -Body '{\"summary\":\"Test story\",\"genre\":\"noir_detective\",\"previous_chapter_id\":null}' -ContentType 'application/json' | ConvertTo-Json -Depth 10"
    pause
)

