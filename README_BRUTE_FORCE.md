# 🔐 Brute Force Tool - Difai Team

Modern GUI brute force tool for testing passwords against web targets.

## 🚀 Features

- **Modern GUI Interface**: Dark theme with emojis and professional design
- **Real HTTP Requests**: Actually tests passwords against the target URL
- **Character Set**: Uses all symbols (A-Z, a-z, 0-9, special characters)
- **Configurable**: Set min/max password length and delay between attempts
- **Real-time Monitoring**: Live status updates and progress tracking
- **Threading**: Non-blocking UI with background attack processing

## 📋 Requirements

- Python 3.7+
- Windows OS (designed for Windows GUI)
- Internet connection

## 🛠️ Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the tool:**
   ```bash
   python brute_force_tool.py
   ```

## 🎯 Target Configuration

The tool is configured to attack: `https://difai-team:2096`

## ⚙️ Configuration Options

- **Min Length**: Minimum password length to test (1-10)
- **Max Length**: Maximum password length to test (1-10)
- **Delay**: Milliseconds between attempts (0-5000ms)

## 🔧 How It Works

1. **Character Generation**: Systematically generates all possible character combinations
2. **HTTP Testing**: Makes real HTTP requests to test each password
3. **Authentication Methods**: Tries both Basic Auth and form-based login
4. **Success Detection**: Monitors response codes and content for successful authentication

## ⚠️ Important Notes

- This is a **REAL** tool that makes actual HTTP requests
- Use responsibly and only against systems you own or have permission to test
- The tool will systematically try all character combinations
- Found passwords are displayed immediately when discovered
- You can stop the attack at any time using the STOP button

## 🎨 GUI Features

- **Dark Theme**: Professional dark interface
- **Emojis**: Visual indicators for different functions
- **Real-time Log**: Live attack progress and results
- **Status Panel**: Current attempt, total attempts, elapsed time
- **Progress Bar**: Visual indication of ongoing attack

## 🔒 Security Disclaimer

This tool is for educational and authorized testing purposes only. Always ensure you have proper authorization before testing any system. The authors are not responsible for any misuse of this tool.

## 📱 Windows Compatibility

- Designed specifically for Windows GUI
- Uses tkinter for cross-platform compatibility
- Optimized for Windows display and interaction patterns