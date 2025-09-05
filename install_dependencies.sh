#!/bin/bash
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
