#!/usr/bin/env python3
"""
AI Research Assistant for Writers - Auto-Launcher
This script automatically sets up and launches the entire writing assistant system.
"""

import os
import sys
import subprocess
import time
import json
import platform
import shutil
from pathlib import Path
from typing import List, Dict, Any

class WritingAssistantLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.ai_engine_dir = self.project_root / "ai_engine"
        self.scraper_dir = self.project_root / "scraper_service"
        self.frontend_dir = self.project_root / "frontend_app"
        self.logs_dir = self.project_root / "logs"
        
        # Create logs directory
        self.logs_dir.mkdir(exist_ok=True)
        
        # Service ports
        self.ai_engine_port = 8000
        self.scraper_port = 3001
        self.frontend_port = 3000
        
        # Process tracking
        self.processes = {}
        
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        # Also write to log file
        with open(self.logs_dir / "launcher.log", "a") as f:
            f.write(log_message + "\n")
    
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.log(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
            return False
        self.log(f"✅ Python {version.major}.{version.minor} detected")
        return True
    
    def check_node_version(self) -> bool:
        """Check if Node.js is available"""
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log(f"✅ Node.js {version} detected")
                return True
            else:
                self.log("❌ Node.js not found")
                return False
        except FileNotFoundError:
            self.log("❌ Node.js not found")
            return False
    
    def install_python_dependencies(self):
        """Install Python dependencies for AI Engine"""
        self.log("📦 Installing Python dependencies for AI Engine...")
        
        requirements_file = self.ai_engine_dir / "requirements.txt"
        if not requirements_file.exists():
            # Create requirements.txt if it doesn't exist
            requirements = [
                "fastapi==0.104.1",
                "uvicorn==0.24.0",
                "pydantic==2.5.0",
                "httpx==0.25.2",
                "python-dotenv==1.0.0",
                "aiofiles==23.2.1",
                "sqlite3",  # Usually built-in
            ]
            with open(requirements_file, "w") as f:
                f.write("\n".join(requirements))
            self.log("Created requirements.txt")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True, capture_output=True, text=True)
            self.log("✅ Python dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Failed to install Python dependencies: {e}")
            return False
    
    def install_node_dependencies(self):
        """Install Node.js dependencies for Scraper Service"""
        self.log("📦 Installing Node.js dependencies for Scraper Service...")
        
        package_json = self.scraper_dir / "package.json"
        if not package_json.exists():
            # Create package.json if it doesn't exist
            package_data = {
                "name": "scraper-service",
                "version": "1.0.0",
                "description": "Web scraping service for AI Research Assistant",
                "main": "server.js",
                "scripts": {
                    "start": "node server.js",
                    "dev": "nodemon server.js"
                },
                "dependencies": {
                    "express": "^4.18.2",
                    "cors": "^2.8.5",
                    "playwright": "^1.40.0",
                    "dotenv": "^16.3.1"
                },
                "devDependencies": {
                    "nodemon": "^3.0.1"
                }
            }
            with open(package_json, "w") as f:
                json.dump(package_data, f, indent=2)
            self.log("Created package.json")
        
        try:
            subprocess.run([
                "npm", "install"
            ], cwd=self.scraper_dir, check=True, capture_output=True, text=True)
            self.log("✅ Node.js dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Failed to install Node.js dependencies: {e}")
            return False
    
    def create_environment_files(self):
        """Create environment files with default settings"""
        self.log("📝 Creating environment files...")
        
        # AI Engine .env
        ai_env = self.ai_engine_dir / ".env"
        if not ai_env.exists():
            env_content = f"""# AI Research Assistant Configuration
SCRAPER_SERVICE_URL=http://localhost:{self.scraper_port}
DATABASE_URL=sqlite:///writing_assistant.db
LOG_LEVEL=INFO
"""
            with open(ai_env, "w") as f:
                f.write(env_content)
            self.log("Created ai_engine/.env")
        
        # Scraper Service .env
        scraper_env = self.scraper_dir / ".env"
        if not scraper_env.exists():
            env_content = f"""# Scraper Service Configuration
PORT={self.scraper_port}
LOG_LEVEL=INFO
"""
            with open(scraper_env, "w") as f:
                f.write(env_content)
            self.log("Created scraper_service/.env")
    
    def start_ai_engine(self) -> bool:
        """Start the AI Engine service"""
        self.log("🚀 Starting AI Engine...")
        
        try:
            process = subprocess.Popen([
                sys.executable, "main.py"
            ], cwd=self.ai_engine_dir, 
            stdout=open(self.logs_dir / "ai_engine.log", "w"),
            stderr=subprocess.STDOUT)
            
            self.processes['ai_engine'] = process
            self.log("✅ AI Engine started")
            
            # Wait a moment for it to start
            time.sleep(3)
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to start AI Engine: {e}")
            return False
    
    def start_scraper_service(self) -> bool:
        """Start the Scraper Service"""
        self.log("🚀 Starting Scraper Service...")
        
        try:
            process = subprocess.Popen([
                "node", "server.js"
            ], cwd=self.scraper_dir,
            stdout=open(self.logs_dir / "scraper_service.log", "w"),
            stderr=subprocess.STDOUT)
            
            self.processes['scraper_service'] = process
            self.log("✅ Scraper Service started")
            
            # Wait a moment for it to start
            time.sleep(3)
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to start Scraper Service: {e}")
            return False
    
    def start_frontend(self) -> bool:
        """Start the frontend"""
        self.log("🚀 Starting Frontend...")
        
        # Create simple frontend if it doesn't exist
        frontend_html = self.project_root / "index.html"
        if not frontend_html.exists():
            self.create_frontend()
        
        try:
            process = subprocess.Popen([
                sys.executable, "-m", "http.server", str(self.frontend_port)
            ], cwd=self.project_root,
            stdout=open(self.logs_dir / "frontend.log", "w"),
            stderr=subprocess.STDOUT)
            
            self.processes['frontend'] = process
            self.log("✅ Frontend started")
            
            # Wait a moment for it to start
            time.sleep(2)
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to start Frontend: {e}")
            return False
    
    def create_frontend(self):
        """Create a simple frontend HTML file"""
        self.log("🎨 Creating frontend...")
        
        frontend_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Research Assistant for Writers</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Georgia', serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            padding: 20px; 
        }
        .container { 
            background: white; 
            border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
            padding: 40px; 
            max-width: 800px; 
            width: 100%; 
        }
        h1 { 
            color: #333; 
            text-align: center; 
            margin-bottom: 10px; 
            font-size: 2.5em; 
        }
        .subtitle { 
            text-align: center; 
            color: #666; 
            margin-bottom: 30px; 
            font-style: italic; 
        }
        .form-group { margin-bottom: 25px; }
        label { 
            display: block; 
            margin-bottom: 8px; 
            color: #333; 
            font-weight: bold; 
            font-size: 1.1em; 
        }
        textarea, select { 
            width: 100%; 
            padding: 15px; 
            border: 2px solid #e0e0e0; 
            border-radius: 10px; 
            font-size: 16px; 
            font-family: 'Georgia', serif; 
            resize: vertical; 
            min-height: 120px; 
        }
        .button { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            border: none; 
            padding: 15px 30px; 
            border-radius: 10px; 
            font-size: 18px; 
            font-weight: bold; 
            cursor: pointer; 
            width: 100%; 
            transition: transform 0.3s, box-shadow 0.3s; 
        }
        .button:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 10px 20px rgba(0,0,0,0.2); 
        }
        .result { 
            display: none; 
            margin-top: 30px; 
            padding: 20px; 
            background: #f8f9fa; 
            border-radius: 10px; 
            border-left: 4px solid #667eea; 
        }
        .loading { 
            display: none; 
            text-align: center; 
            margin-top: 20px; 
        }
        .spinner { 
            border: 4px solid #f3f3f3; 
            border-top: 4px solid #667eea; 
            border-radius: 50%; 
            width: 40px; 
            height: 40px; 
            animation: spin 1s linear infinite; 
            margin: 0 auto 10px; 
        }
        @keyframes spin { 
            0% { transform: rotate(0deg); } 
            100% { transform: rotate(360deg); } 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Research Assistant</h1>
        <p class="subtitle">For Writers Who Want Authentic Human Voices</p>

        <form id="storyForm">
            <div class="form-group">
                <label for="summary">Story Summary</label>
                <textarea id="summary" name="summary" placeholder="Enter your story summary here..." required></textarea>
            </div>

            <div class="form-group">
                <label for="genre">Genre</label>
                <select id="genre" name="genre" required>
                    <option value="">Select a genre</option>
                    <option value="noir_detective">Noir Detective</option>
                    <option value="fantasy_epic">Fantasy Epic</option>
                    <option value="modern_high_school">Modern High School</option>
                    <option value="sci_fi_space">Sci-Fi Space Opera</option>
                </select>
            </div>

            <button type="submit" class="button">Generate Chapter</button>
        </form>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Our AI agents are researching and weaving your chapter...</p>
        </div>

        <div class="result" id="result">
            <h3>Your Generated Chapter</h3>
            <div class="result-content" id="chapterContent"></div>
        </div>
    </div>

    <script>
        document.getElementById('storyForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            
            const formData = {
                summary: document.getElementById('summary').value,
                genre: document.getElementById('genre').value,
                previous_chapter_id: null
            };

            try {
                const response = await fetch('http://localhost:8000/generate-chapter', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();
                
                document.getElementById('loading').style.display = 'none';
                document.getElementById('result').style.display = 'block';
                document.getElementById('chapterContent').textContent = data.content;
                
            } catch (err) {
                document.getElementById('loading').style.display = 'none';
                alert('Error generating chapter: ' + err.message);
            }
        });
    </script>
</body>
</html>'''
        
        with open(frontend_html, "w") as f:
            f.write(frontend_content)
        self.log("Created index.html")
    
    def create_test_story(self):
        """Create a test story and chapter"""
        self.log("📝 Creating test story...")
        
        test_story = {
            "summary": "A detective investigates a mysterious disappearance in a small coastal town during a foggy winter. The missing person is a local lighthouse keeper who was last seen three days ago. As the detective digs deeper, they uncover secrets about the town's past and realize this might be connected to similar disappearances that have occurred every decade for the past 50 years.",
            "genre": "noir_detective",
            "previous_chapter_id": None
        }
        
        # Save test story
        test_file = self.project_root / "test_story.json"
        with open(test_file, "w") as f:
            json.dump(test_story, f, indent=2)
        
        self.log("✅ Test story created: test_story.json")
        return test_story
    
    def test_system(self):
        """Test the complete system"""
        self.log("🧪 Testing system...")
        
        try:
            import requests
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", "requests"])
            import requests
        
        # Test health endpoints
        services = {
            "AI Engine": f"http://localhost:{self.ai_engine_port}/health",
            "Scraper Service": f"http://localhost:{self.scraper_port}/health"
        }
        
        for service, url in services.items():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    self.log(f"✅ {service} is healthy")
                else:
                    self.log(f"❌ {service} returned status {response.status_code}")
            except Exception as e:
                self.log(f"❌ {service} is not responding: {e}")
        
        # Test chapter generation
        self.log("📝 Testing chapter generation...")
        test_story = self.create_test_story()
        
        try:
            response = requests.post(
                f"http://localhost:{self.ai_engine_port}/generate-chapter",
                json=test_story,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                self.log(f"✅ Chapter generated successfully!")
                self.log(f"   Chapter ID: {result['chapter_id']}")
                self.log(f"   Word Count: {result['word_count']}")
                self.log(f"   Content Preview: {result['content'][:100]}...")
                
                # Save the generated chapter
                chapter_file = self.project_root / "generated_chapter.json"
                with open(chapter_file, "w") as f:
                    json.dump(result, f, indent=2)
                self.log(f"✅ Generated chapter saved to: generated_chapter.json")
                
            else:
                self.log(f"❌ Chapter generation failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.log(f"❌ Chapter generation test failed: {e}")
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut"""
        self.log("🖥️ Creating desktop shortcut...")
        
        desktop_dir = Path.home() / "Desktop"
        if not desktop_dir.exists():
            desktop_dir = Path.home() / "Desktop"  # Try different path for different OS
        
        if platform.system() == "Windows":
            # Windows shortcut (batch file)
            shortcut_path = desktop_dir / "AI Writing Assistant.bat"
            with open(shortcut_path, "w") as f:
                f.write(f'cd /d "{self.project_root}"\n')
                f.write(f'"{sys.executable}" launch_writing_assistant.py\n')
            self.log(f"✅ Desktop shortcut created: {shortcut_path}")
            
        elif platform.system() == "Darwin":  # macOS
            # macOS AppleScript app
            app_path = desktop_dir / "AI Writing Assistant.app"
            app_path.mkdir(exist_ok=True)
            
            # Info.plist
            info_plist = app_path / "Contents" / "Info.plist"
            info_plist.parent.mkdir(exist_ok=True)
            with open(info_plist, "w") as f:
                f.write('''<?xml version="1.0" encoding="UTF-8"?>
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
</dict>
</plist>''')
            
            # Launch script
            macos_script = app_path / "Contents" / "MacOS" / "launch_script"
            macos_script.parent.mkdir(exist_ok=True)
            with open(macos_script, "w") as f:
                f.write(f'''#!/bin/bash
cd "{self.project_root}"
"{sys.executable}" launch_writing_assistant.py
''')
            macos_script.chmod(0o755)
            self.log(f"✅ Desktop shortcut created: {app_path}")
            
        else:  # Linux
            # Linux desktop file
            desktop_file = desktop_dir / "ai-writing-assistant.desktop"
            with open(desktop_file, "w") as f:
                f.write(f'''[Desktop Entry]
Version=1.0
Type=Application
Name=AI Writing Assistant
Comment=AI Research Assistant for Writers
Exec={sys.executable} {self.project_root}/launch_writing_assistant.py
Icon=text-editor
Path={self.project_root}
Terminal=true
Categories=Office;TextEditor;
''')
            desktop_file.chmod(0o755)
            self.log(f"✅ Desktop shortcut created: {desktop_file}")
    
    def run(self):
        """Main execution"""
        self.log("🚀 Starting AI Research Assistant for Writers Setup...")
        
        # Check prerequisites
        if not self.check_python_version():
            return False
        
        if not self.check_node_version():
            self.log("⚠️  Node.js not found. Scraper service may not work properly.")
        
        # Install dependencies
        if not self.install_python_dependencies():
            return False
        
        if not self.install_node_dependencies():
            self.log("⚠️  Node.js dependencies installation failed.")
        
        # Setup environment
        self.create_environment_files()
        
        # Start services
        if not self.start_ai_engine():
            return False
        
        if not self.start_scraper_service():
            self.log("⚠️  Scraper service failed to start. Continuing without it.")
        
        if not self.start_frontend():
            return False
        
        # Test the system
        self.test_system()
        
        # Create desktop shortcut
        self.create_desktop_shortcut()
        
        self.log("\n🎉 Setup complete! Your AI Writing Assistant is ready!")
        self.log(f"📖 Frontend: http://localhost:{self.frontend_port}")
        self.log(f"🔧 AI Engine API: http://localhost:{self.ai_engine_port}")
        self.log(f"🔍 API Docs: http://localhost:{self.ai_engine_port}/docs")
        self.log("\nPress Ctrl+C to stop all services")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.log("\n🛑 Shutting down services...")
            for name, process in self.processes.items():
                if process:
                    process.terminate()
                    self.log(f"Stopped {name}")
            self.log("✅ All services stopped")
        
        return True

if __name__ == "__main__":
    launcher = WritingAssistantLauncher()
    success = launcher.run()
    sys.exit(0 if success else 1)
