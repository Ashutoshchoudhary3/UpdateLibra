

#!/usr/bin/env python3
"""
Desktop Launcher for AI Research Assistant for Writers
Creates desktop shortcuts and provides easy launch options.
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
import json

def create_desktop_shortcut():
    """Create desktop shortcut for the writing assistant"""
    project_root = Path(__file__).parent
    desktop_dir = Path.home() / "Desktop"
    
    # Ensure desktop directory exists
    desktop_dir.mkdir(exist_ok=True)
    
    if platform.system() == "Windows":
        # Windows batch file
        shortcut_path = desktop_dir / "AI Writing Assistant.bat"
        with open(shortcut_path, "w") as f:
            f.write(f'''@echo off
echo Starting AI Research Assistant for Writers...
cd /d "{project_root}"
python start_mock_system.py
pause
''')
        print(f"✅ Windows shortcut created: {shortcut_path}")
        
    elif platform.system() == "Darwin":  # macOS
        # macOS app bundle
        app_path = desktop_dir / "AI Writing Assistant.app"
        app_path.mkdir(exist_ok=True)
        
        # Create Info.plist
        info_plist = app_path / "Contents" / "Info.plist"
        info_plist.parent.mkdir(exist_ok=True)
        
        plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launch_script</string>
    <key>CFBundleIdentifier</key>
    <string>com.ai.writing.assistant</string>
    <key>CFBundleName</key>
    <string>AI Writing Assistant</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>'''
        
        with open(info_plist, "w") as f:
            f.write(plist_content)
        
        # Create launch script
        macos_dir = app_path / "Contents" / "MacOS"
        macos_dir.mkdir(exist_ok=True)
        
        launch_script = macos_dir / "launch_script"
        with open(launch_script, "w") as f:
            f.write(f'''#!/bin/bash
cd "{project_root}"
python3 start_mock_system.py
''')
        
        # Make script executable
        os.chmod(launch_script, 0o755)
        
        print(f"✅ macOS app created: {app_path}")
        
    else:  # Linux
        # Linux desktop file
        desktop_file = desktop_dir / "ai-writing-assistant.desktop"
        
        desktop_content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=AI Writing Assistant
Comment=AI Research Assistant for Writers
Exec=python3 {project_root}/start_mock_system.py
Icon=text-editor
Path={project_root}
Terminal=true
Categories=Office;TextEditor;
'''
        
        with open(desktop_file, "w") as f:
            f.write(desktop_content)
        
        # Make desktop file executable
        os.chmod(desktop_file, 0o755)
        
        print(f"✅ Linux desktop shortcut created: {desktop_file}")

def create_install_script():
    """Create installation script for dependencies"""
    project_root = Path(__file__).parent
    
    if platform.system() == "Windows":
        install_script = project_root / "install_dependencies.bat"
        with open(install_script, "w") as f:
            f.write('''@echo off
echo Installing dependencies for AI Research Assistant...
echo Installing Python packages...
pip install fastapi uvicorn pydantic httpx python-dotenv aiofiles requests
echo Python packages installed!
echo.
echo Note: Node.js is required for the scraper service.
echo Please install Node.js from https://nodejs.org/
echo.
pause
''')
    else:
        install_script = project_root / "install_dependencies.sh"
        with open(install_script, "w") as f:
            f.write('''#!/bin/bash
echo "Installing dependencies for AI Research Assistant..."

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    echo "Installing Python packages..."
    python3 -m pip install fastapi uvicorn pydantic httpx python-dotenv aiofiles requests
    echo "Python packages installed!"
else
    echo "Python 3 not found. Please install Python 3.8 or higher."
fi

# Check if Node.js is available
if command -v node &> /dev/null; then
    echo "Node.js found: $(node --version)"
else
    echo "Node.js not found. Please install Node.js for full functionality."
    echo "Visit: https://nodejs.org/"
fi

echo "Installation complete!"
read -p "Press Enter to continue..."
''')
        
        # Make script executable on Unix systems
        if platform.system() != "Windows":
            os.chmod(install_script, 0o755)
    
    print(f"✅ Install script created: {install_script}")

def create_readme():
    """Create user-friendly README"""
    project_root = Path(__file__).parent
    readme_path = project_root / "USER_GUIDE.md"
    
    readme_content = '''# AI Research Assistant for Writers - User Guide

## 🚀 Quick Start

### Option 1: Desktop Shortcut (Recommended)
1. Look for "AI Writing Assistant" on your desktop
2. Double-click to launch
3. The system will open automatically in your browser

### Option 2: Manual Launch
1. Open terminal/command prompt
2. Navigate to the project folder
3. Run: `python start_mock_system.py`

## 📋 System Requirements

- **Python 3.8+** (Required)
- **Node.js** (Optional - for web scraping features)
- **Web Browser** (Chrome, Firefox, Safari, Edge)

## 🎯 Features

✅ **Mock AI System** - Complete functionality without API keys
✅ **Automatic Setup** - Dependencies install automatically
✅ **Test Stories** - Pre-loaded with sample content
✅ **Web Interface** - Easy-to-use browser interface
✅ **Chapter Generation** - Full chapter creation workflow

## 🧪 Test Mode

This is a **demonstration version** that uses mock AI responses to show how the system works without requiring actual AI API keys.

### What You Can Test:
- Complete chapter generation workflow
- All AI agent interactions
- Web interface functionality
- Story creation process

### Sample Test Story:
- **Genre**: Noir Detective
- **Plot**: Detective investigates lighthouse keeper disappearance
- **Setting**: Foggy coastal town with dark secrets
- **Mystery**: Pattern of disappearances every decade

## 🔧 Troubleshooting

### If the system doesn't start:
1. Check Python version: `python --version` (needs 3.8+)
2. Install dependencies: Run `install_dependencies.bat` (Windows) or `install_dependencies.sh` (Mac/Linux)
3. Check if ports 8000 and 3000 are available

### If you see errors:
- Mock mode will show "Gemini API error" messages - this is normal for testing
- The system will continue working with mock responses

## 📖 How It Works

1. **Input Your Story**: Enter a summary and select genre
2. **AI Processing**: System analyzes intent, scouts scenes, researches style
3. **Chapter Generation**: AI weaves plot points into a complete chapter
4. **Results**: View your generated chapter with character and lore information

## 🎨 Customization

To use real AI instead of mock responses:
1. Get Gemini AI API key
2. Replace `main_mock.py` with original `main.py`
3. Configure environment variables

## 📞 Support

For issues or questions:
1. Check the logs in the `logs/` folder
2. Review the troubleshooting section above
3. Ensure all requirements are met

---

**Enjoy writing with your AI Research Assistant!** 🎉
'''
    
    with open(readme_path, "w") as f:
        f.write(readme_content)
    
    print(f"✅ User guide created: {readme_path}")

def main():
    """Main setup function"""
    print("🚀 Setting up AI Research Assistant for Writers...")
    print("=" * 50)
    
    # Create desktop shortcut
    print("1. Creating desktop shortcut...")
    create_desktop_shortcut()
    
    # Create install script
    print("2. Creating dependency installer...")
    create_install_script()
    
    # Create user guide
    print("3. Creating user guide...")
    create_readme()
    
    print("=" * 50)
    print("✅ Setup complete!")
    print("\n🎯 Next steps:")
    print("1. Double-click 'AI Writing Assistant' on your desktop")
    print("2. Or run: python start_mock_system.py")
    print("3. Follow the on-screen instructions")
    print("\n📖 For help, see USER_GUIDE.md")
    print("🎉 Enjoy your AI Writing Assistant!")

if __name__ == "__main__":
    main()


