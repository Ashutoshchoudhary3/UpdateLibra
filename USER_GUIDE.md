# AI Research Assistant for Writers - User Guide

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
