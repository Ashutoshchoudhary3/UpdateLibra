

# AI Research Assistant for Writers - PowerShell Launcher
# Run this script to start all services

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Research Assistant for Writers" -ForegroundColor Cyan
Write-Host "PowerShell Startup Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
function Test-CommandExists {
    param($command)
    try {
        if (Get-Command $command -ErrorAction SilentlyContinue) {
            return $true
        }
    } catch {
        return $false
    }
    return $false
}

Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Node.js
if (-not (Test-CommandExists "node")) {
    Write-Host "❌ ERROR: Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
} else {
    $nodeVersion = node --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
}

# Check Python
if (-not (Test-CommandExists "python")) {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org/" -ForegroundColor Red
    exit 1
} else {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
}

# Set working directory
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot
Write-Host "Working directory: $projectRoot" -ForegroundColor Green

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "✅ Created logs directory" -ForegroundColor Green
}

# Function to kill processes on specific ports
function Stop-ProcessesOnPort {
    param($port)
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    foreach ($conn in $connections) {
        try {
            $process = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
            if ($process) {
                Stop-Process -Id $process.Id -Force
                Write-Host "🛑 Killed process '$($process.Name)' (PID: $($process.Id)) on port $port" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "Warning: Could not kill process on port $port" -ForegroundColor Yellow
        }
    }
}

# Clean up existing processes
Write-Host ""
Write-Host "Cleaning up existing processes..." -ForegroundColor Yellow
Stop-ProcessesOnPort -port 3000
Stop-ProcessesOnPort -port 8000  
Stop-ProcessesOnPort -port 48404

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow

# Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
Set-Location "$projectRoot\ai_engine"
try {
    python -m pip install -r requirements.txt > "$projectRoot\logs\pip_install.log" 2>&1
    Write-Host "✅ Python dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Warning: Some Python dependencies may have failed. Check logs\pip_install.log" -ForegroundColor Yellow
}

# Node.js dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Cyan
Set-Location "$projectRoot\scraper_service"
try {
    npm install > "$projectRoot\logs\npm_install.log" 2>&1
    Write-Host "✅ Node.js dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Warning: Some Node.js dependencies may have failed. Check logs\npm_install.log" -ForegroundColor Yellow
}

Set-Location $projectRoot

# Start services
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting AI Research Assistant Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start Scraper Service
Write-Host "Starting Scraper Service on port 3000..." -ForegroundColor Cyan
$scraperJob = Start-Job -ScriptBlock {
    Set-Location $using:projectRoot\scraper_service
    node server.js > "$using:projectRoot\logs\scraper.log" 2>&1
}
Start-Sleep -Seconds 3

# Start AI Engine
Write-Host "Starting AI Engine on port 8000..." -ForegroundColor Cyan
$aiEngineJob = Start-Job -ScriptBlock {
    Set-Location $using:projectRoot\ai_engine
    python main_mock.py > "$using:projectRoot\logs\ai_engine.log" 2>&1
}
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "Starting Frontend on port 48404..." -ForegroundColor Cyan
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:projectRoot
    python -m http.server 48404 --directory frontend_app > "$using:projectRoot\logs\frontend.log" 2>&1
}
Start-Sleep -Seconds 3

# Create status check function
function Show-Status {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Service Status Check" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Check ports
    $scraperRunning = $null -ne (Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue)
    $aiEngineRunning = $null -ne (Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue)
    $frontendRunning = $null -ne (Get-NetTCPConnection -LocalPort 48404 -ErrorAction SilentlyContinue)
    
    Write-Host "Port 3000 (Scraper Service): " -NoNewline
    if ($scraperRunning) { Write-Host "✅ Running" -ForegroundColor Green } else { Write-Host "❌ Not running" -ForegroundColor Red }
    
    Write-Host "Port 8000 (AI Engine): " -NoNewline
    if ($aiEngineRunning) { Write-Host "✅ Running" -ForegroundColor Green } else { Write-Host "❌ Not running" -ForegroundColor Red }
    
    Write-Host "Port 48404 (Frontend): " -NoNewline
    if ($frontendRunning) { Write-Host "✅ Running" -ForegroundColor Green } else { Write-Host "❌ Not running" -ForegroundColor Red }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Access your application at:" -ForegroundColor Yellow
    Write-Host "http://localhost:48404" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "API Documentation at:" -ForegroundColor Yellow
    Write-Host "http://localhost:8000/docs" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
}

# Show initial status
Show-Status

# Create menu
function Show-Menu {
    Write-Host ""
    Write-Host "Quick Actions:" -ForegroundColor Yellow
    Write-Host "[1] Check Status Again" -ForegroundColor White
    Write-Host "[2] Open Application in Browser" -ForegroundColor White
    Write-Host "[3] Open API Documentation" -ForegroundColor White
    Write-Host "[4] Test API Endpoint" -ForegroundColor White
    Write-Host "[5] View Logs" -ForegroundColor White
    Write-Host "[6] Stop All Services" -ForegroundColor White
    Write-Host "[7] Exit" -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "Enter your choice (1-7)"
    
    switch ($choice) {
        "1" { Show-Status; Show-Menu }
        "2" { Start-Process "http://localhost:48404"; Show-Menu }
        "3" { Start-Process "http://localhost:8000/docs"; Show-Menu }
        "4" {
            Write-Host "Testing API endpoint..." -ForegroundColor Yellow
            try {
                $response = Invoke-RestMethod -Uri "http://localhost:8000/generate-chapter" -Method Post -Body '{"summary":"Test story","genre":"noir_detective","previous_chapter_id":null}' -ContentType "application/json"
                Write-Host "✅ API test successful!" -ForegroundColor Green
                Write-Host "Response: $($response.title)" -ForegroundColor Cyan
            } catch {
                Write-Host "❌ API test failed: $($_.Exception.Message)" -ForegroundColor Red
            }
            Show-Menu
        }
        "5" {
            Write-Host ""
            Write-Host "=== Recent AI Engine Log ===" -ForegroundColor Cyan
            if (Test-Path "logs\ai_engine.log") {
                Get-Content "logs\ai_engine.log" -Tail 10 | ForEach-Object { Write-Host "  $_" }
            } else {
                Write-Host "  No AI Engine log found" -ForegroundColor Yellow
            }
            
            Write-Host ""
            Write-Host "=== Recent Scraper Log ===" -ForegroundColor Cyan
            if (Test-Path "logs\scraper.log") {
                Get-Content "logs\scraper.log" -Tail 10 | ForEach-Object { Write-Host "  $_" }
            } else {
                Write-Host "  No Scraper log found" -ForegroundColor Yellow
            }
            Show-Menu
        }
        "6" {
            Write-Host "Stopping all services..." -ForegroundColor Yellow
            Get-Job | Remove-Job -Force
            Stop-ProcessesOnPort -port 3000
            Stop-ProcessesOnPort -port 8000
            Stop-ProcessesOnPort -port 48404
            Write-Host "✅ All services stopped" -ForegroundColor Green
        }
        "7" { 
            Write-Host "Services will continue running in background." -ForegroundColor Yellow
            Write-Host "Run this script again to manage them, or use Stop-Job cmdlet to stop them." -ForegroundColor Yellow
            return
        }
        default { 
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
            Show-Menu 
        }
    }
}

Write-Host ""
Write-Host "Services are running in background jobs." -ForegroundColor Green
Write-Host "Use the menu below to manage them:" -ForegroundColor Yellow

# Show menu
Show-Menu


