
# AI Research Assistant for Writers - Windows Launcher

## Overview
This Windows launcher provides an easy way to start, monitor, and manage all services for the AI Research Assistant for Writers project.

## Files Included
- `start_windows.bat` - Main startup launcher
- `status_check.bat` - Service status checker and management utility
- `stop_services.bat` - Clean shutdown utility

## Prerequisites
- **Node.js** (v14 or higher) - Download from https://nodejs.org/
- **Python** (v3.8 or higher) - Download from https://python.org/
- **Windows** (Windows 10 or higher recommended)

## Quick Start

### 1. First Time Setup
1. Ensure Node.js and Python are installed and in your system PATH
2. Navigate to the project folder in Command Prompt or File Explorer
3. Double-click `start_windows.bat`

### 2. Daily Usage
- **Start Everything**: Run `start_windows.bat`
- **Check Status**: Run `status_check.bat`
- **Stop Everything**: Run `stop_services.bat`

## Detailed Usage

### start_windows.bat
This is your main launcher that:
- ✅ Checks prerequisites (Node.js, Python)
- ✅ Installs dependencies automatically
- ✅ Starts all three services in separate windows
- ✅ Creates log files for debugging
- ✅ Opens your browser to the application
- ✅ Provides status updates

**What it starts:**
- **Scraper Service** (Port 3000) - Node.js service for web scraping
- **AI Engine** (Port 8000) - Python FastAPI backend
- **Frontend** (Port 48404) - Web interface

### status_check.bat
Comprehensive status monitoring tool that shows:
- 🔍 Service status (running/stopped)
- 📝 Recent log entries
- 🌐 Quick access to application and API docs
- 🧪 API endpoint testing
- 📊 Process details

**Interactive Menu:**
1. Open Application in Browser
2. Open API Documentation  
3. View Full Logs
4. Test API Endpoint
5. Exit

### stop_services.bat
Clean shutdown utility that:
- 🛑 Stops all services gracefully
- 🔒 Kills processes on all ports
- 🧹 Closes console windows
- 📋 Shows final status report

## Service Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   AI Engine     │    │ Scraper Service │
│   (Port 48404)  │◄──►│   (Port 8000)   │◄──►│   (Port 3000)   │
│  User Interface │    │   FastAPI       │    │   Node.js       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Access Points
- **Application**: http://localhost:48404
- **API Documentation**: http://localhost:8000/docs
- **API Base URL**: http://localhost:8000

## Log Files
All logs are stored in the `logs/` directory:
- `ai_engine.log` - Python backend activity
- `scraper.log` - Web scraping service activity  
- `frontend.log` - Frontend server activity
- `pip_install.log` - Python dependency installation
- `npm_install.log` - Node.js dependency installation

## Troubleshooting

### Port Already in Use
The launcher automatically kills existing processes on ports 3000, 8000, and 48404. If you still get port conflicts, run `stop_services.bat` first.

### Dependencies Fail to Install
1. Check internet connection
2. Run `pip install -r ai_engine/requirements.txt` manually
3. Run `npm install` in the `scraper_service` folder
4. Check the log files in `logs/` directory

### Services Don't Start
1. Check if Python and Node.js are in your PATH
2. Run `status_check.bat` to see what's running
3. Check log files for error messages
4. Ensure no antivirus is blocking the services

### Browser Doesn't Open
The application should be available at http://localhost:48404 even if the auto-open fails.

## Advanced Usage

### Manual Service Control
You can also run services manually in separate terminals:

**Scraper Service:**
```cmd
cd scraper_service
node server.js
```

**AI Engine:**
```cmd
cd ai_engine
python main_mock.py
```

**Frontend:**
```cmd
python -m http.server 48404 --directory frontend_app
```

### Environment Variables
Create a `.env` file in the `ai_engine` folder with:
```
GEMINI_API_KEY=your_api_key_here
```

## Support
If you encounter issues:
1. Check the troubleshooting section above
2. Review log files in `logs/` directory
3. Run `status_check.bat` for diagnostic information
4. Ensure all prerequisites are properly installed

