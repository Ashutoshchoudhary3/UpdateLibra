



#!/usr/bin/env python3
"""
Setup script for AI Research Assistant for Writers
"""

import os
import subprocess
import sys
import time

def run_command(command, cwd=None, shell=True):
    """Run a command and return success status"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=shell, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        print(f"Success: {result.stdout}")
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return False

def setup_ai_engine():
    """Set up the AI Engine service"""
    print("\n🤖 Setting up AI Engine...")
    
    ai_engine_dir = os.path.join(os.path.dirname(__file__), "ai_engine")
    
    # Create virtual environment
    if not run_command(f"cd {ai_engine_dir} && python -m venv venv"):
        return False
    
    # Activate virtual environment and install requirements
    if sys.platform == "win32":
        pip_cmd = f"cd {ai_engine_dir} && venv\\Scripts\\pip install -r requirements.txt"
    else:
        pip_cmd = f"cd {ai_engine_dir} && source venv/bin/activate && pip install -r requirements.txt"
    
    if not run_command(pip_cmd):
        return False
    
    print("✅ AI Engine setup complete")
    return True

def setup_scraper_service():
    """Set up the Scraper Service"""
    print("\n🕷️ Setting up Scraper Service...")
    
    scraper_dir = os.path.join(os.path.dirname(__file__), "scraper_service")
    
    # Install Node.js dependencies
    if not run_command(f"cd {scraper_dir} && npm install"):
        return False
    
    print("✅ Scraper Service setup complete")
    return True

def create_env_files():
    """Create environment files from examples"""
    print("\n📝 Creating environment files...")
    
    # Create ai_engine .env file
    ai_env_example = os.path.join(os.path.dirname(__file__), "ai_engine", ".env.example")
    ai_env_file = os.path.join(os.path.dirname(__file__), "ai_engine", ".env")
    
    if os.path.exists(ai_env_example) and not os.path.exists(ai_env_file):
        with open(ai_env_example, 'r') as f:
            content = f.read()
        with open(ai_env_file, 'w') as f:
            f.write(content)
        print("Created ai_engine/.env file")
    
    print("✅ Environment files created")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up AI Research Assistant for Writers...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    # Check Node.js
    if not run_command("node --version"):
        print("❌ Node.js is required but not installed")
        sys.exit(1)
    
    # Check npm
    if not run_command("npm --version"):
        print("❌ npm is required but not installed")
        sys.exit(1)
    
    # Setup services
    success = True
    
    success &= create_env_files()
    success &= setup_ai_engine()
    success &= setup_scraper_service()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 Setup complete!")
        print("\nNext steps:")
        print("1. Set up your OpenAI API key in ai_engine/.env")
        print("2. Start the services:")
        print("   - AI Engine: cd ai_engine && source venv/bin/activate && python main.py")
        print("   - Scraper Service: cd scraper_service && npm start")
        print("   - Frontend: Open frontend_app/index.html in a browser")
        print("\n3. Access the application at http://localhost:43598")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()



