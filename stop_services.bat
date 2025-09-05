


@echo off
echo ========================================
echo AI Research Assistant - Service Shutdown
echo ========================================
echo.
echo Stopping all services...

:: Kill processes on our ports
echo.
echo Killing processes on port 3000 (Scraper Service)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    echo   Killed process PID: %%a
)

echo.
echo Killing processes on port 8000 (AI Engine)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    echo   Killed process PID: %%a
)

echo.
echo Killing processes on port 48404 (Frontend)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":48404" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    echo   Killed process PID: %%a
)

:: Kill Python processes that might be running our services
echo.
echo Killing Python processes associated with our services...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq AI Engine" >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Frontend Server" >nul 2>&1
taskkill /F /IM python.exe /FI "COMMANDLINE eq *main_mock.py*" >nul 2>&1
taskkill /F /IM python.exe /FI "COMMANDLINE eq *http.server*" >nul 2>&1

:: Kill Node.js processes
echo.
echo Killing Node.js processes associated with our services...
taskkill /F /IM node.exe /FI "COMMANDLINE eq *server.js*" >nul 2>&1

:: Close console windows
echo.
echo Closing service console windows...
taskkill /F /FI "WINDOWTITLE eq Scraper Service" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq AI Engine" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Frontend Server" >nul 2>&1

echo.
echo ========================================
echo Service shutdown complete!
echo ========================================
echo.
echo Remaining processes:
echo.
echo Python processes:
tasklist /FI "IMAGENAME eq python.exe" 2>nul | findstr /V "INFO:" || echo   No Python processes found

echo.
echo Node.js processes:
tasklist /FI "IMAGENAME eq node.exe" 2>nul | findstr /V "INFO:" || echo   No Node.js processes found

echo.
echo Port status:
netstat -ano | findstr ":3000" >nul && echo   Port 3000: OCCUPIED || echo   Port 3000: FREE
netstat -ano | findstr ":8000" >nul && echo   Port 8000: OCCUPIED || echo   Port 8000: FREE
netstat -ano | findstr ":48404" >nul && echo   Port 48404: OCCUPIED || echo   Port 48404: FREE

echo.
echo ========================================
pause


